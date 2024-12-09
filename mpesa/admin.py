from django.contrib import admin
from .models import MpesaTransaction
# Register your models here.

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'phone_number', 'amount', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'phone_number')