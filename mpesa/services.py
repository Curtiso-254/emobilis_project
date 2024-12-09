import base64
import requests
import logging
import decimal
from datetime import datetime
from django.conf import settings
from .models import MpesaTransaction

logger = logging.getLogger(__name__)

class MpesaService:
    def __init__(self):
        """Initialize the Mpesa service with an access token"""
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """Obtain OAuth access token from Daraja API"""
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        # Define the STK push URL as a class or method constant
        self.stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        
        auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        try:
            response = requests.get(
                auth_url, 
                auth=(consumer_key, consumer_secret)
            )
            response.raise_for_status()
            access_token = response.json().get('access_token')
            logger.info(f"Successfully obtained access token: {access_token[:10]}...")
            return access_token
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obtaining access token: {e}")
            return None

    def generate_password(self):
        """Generate base64 encoded password"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        encoded_password = base64.b64encode(password_string.encode('utf-8')).decode('utf-8')
        return encoded_password, timestamp

    def validate_phone_number(self, phone_number):
        """Validate and format phone number"""
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, str(phone_number)))
        
        # Ensure it starts with 254 and is 12 digits long
        if not phone.startswith('254') or len(phone) != 12:
            raise ValueError(f"Invalid phone number format: {phone_number}. Must be in format 254XXXXXXXXX")
        
        return phone

    def validate_amount(self, amount):
        """Validate payment amount"""
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number")
            return amount
        except ValueError:
            raise ValueError(f"Invalid amount: {amount}. Must be a positive number")

    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate STK Push for online payment"""
        # Validate inputs
        try:
            formatted_phone = self.validate_phone_number(phone_number)
            validated_amount = self.validate_amount(amount)
        except ValueError as e:
            logger.error(f"Input validation error: {e}")
            return {"error": str(e)}

        # Check access token
        if not self.access_token:
            logger.error("Could not obtain access token")
            return {"error": "Could not obtain access token"}
        
        # Generate password and timestamp
        password, timestamp = self.generate_password()

        # Prepare headers with access token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        # Prepare payload with validated inputs
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": validated_amount,
            "PartyA": formatted_phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": formatted_phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": account_reference[:12],  # Limit to 12 characters
            "TransactionDesc": transaction_desc[:13]  # Limit to 13 characters
        }

        try:
            # Log payload for debugging (be careful with sensitive info)
            logger.info(f"STK Push Payload: {payload}")

            # Use the class-level stk_push_url
            response = requests.post(self.stk_push_url, headers=headers, json=payload)
            
            # Log full response for debugging
            logger.info(f"Full Response Status: {response.status_code}")
            logger.info(f"Full Response Content: {response.text}")

            response.raise_for_status()
            
            response_data = response.json()
            
            # Create transaction record
            transaction = MpesaTransaction.objects.create(
                phone_number=formatted_phone,
                amount=validated_amount,
                transaction_id=response_data.get('CheckoutRequestID', 'N/A'),
                status='pending'
            )
            
            logger.info(f"STK Push Response: {response_data}")
            return response_data
        
        except requests.exceptions.RequestException as e:
            # More detailed error logging
            logger.error(f"Error initiating STK push: {e}")
            logger.error(f"Response Content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            return {"error": str(e), "details": e.response.text if hasattr(e, 'response') else 'No additional details'}