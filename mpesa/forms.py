from django import forms

class MpesaPaymentForm(forms.Form):
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter M-pesa Phone Number'
        })
    )
    amount = forms.DecimalField(
        label='amount',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Amount'
        })

    )