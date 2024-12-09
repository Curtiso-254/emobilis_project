from django.shortcuts import render
from django.http import JsonResponse
from .services import MpesaService
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import MpesaTransaction
import json
from .forms import MpesaPaymentForm
# Create your views here.

@require_http_methods(['POST'])
def initiate_payment(request):
    """
    View to initiate Mpesa-Payment
    """
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        mpesa_service = MpesaService
        result = mpesa_service.initiate_stk_push(
            phone_number,
            amount,
            'Invoice Payment',
            'Payment for services rendered'
        )
        return JsonResponse(result)
    

@csrf_exempt
@require_http_methods(["POST"])
def mpesa_callback(request):
    """
    Callback endpoint to receive M-pesa transaction results
    """
  #  if request.method == 'POST':
        # PRocess and validate M-Pesa callback data
        # Log Transaction details
        # Update Payment status in your system

   #     return JsonResponse({"status": "success"})

    try:
        callback_data = json.loads(request.body)
        
        # Extract relevant transaction details
        result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        
        # Update transaction status
        transaction = MpesaTransaction.objects.filter(transaction_id=checkout_request_id).first()
        
        if transaction:
            transaction.status = 'success' if result_code == 0 else 'failed'
            transaction.save()
        
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
def mpesa_payment_page(request):
    """Render M-Pesa payment page"""
    form = MpesaPaymentForm()  # Move this outside the if-else block
    
    if request.method == 'POST':
        form = MpesaPaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']
            
            mpesa_service = MpesaService()
            result = mpesa_service.initiate_stk_push(
                phone_number, 
                amount, 
                'Payment', 
                'Online Payment'
            )
            
            return render(request, 'mpesa/payment_result.html', {'result': result})
    
    return render(request, 'mpesa/payment_page.html', {'form': form})