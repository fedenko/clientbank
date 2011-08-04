from cbank.models import BankAccount, Transaction
from django.contrib import admin

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'accounttype', 'user')
    prepopulated_fields = { 'number': ('user',)} 
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('details', 'payer', 'payee', 'value', 'datetime')

admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
