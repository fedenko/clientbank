from decimal import *
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from random import Random
from cbank.gencc import completed_number

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
class BankAccountManager(models.Manager):
    def create_account(self, user, accounttype):
        generator = Random()
        generator.seed()
        number = completed_number(generator, ['7', '7', '7', '7'], 16)
        account = self.model(user=user,
                             number = number,
                             accounttype=accounttype)
        account.save(using=self._db)
        return account

class BankAccount(models.Model):
    BANK_ACCOUNT_TYPE_CHOICES = (
        (u'CC', _(u'Credit card')),
        (u'TR', _(u'Transactional')),
        (u'DP', _(u'Time deposit')),
    )
    user = models.ForeignKey(User)
    number = models.CharField(max_length=16, unique=True)
    accounttype = models.CharField(max_length=2,
                                   choices=BANK_ACCOUNT_TYPE_CHOICES)
    
    objects = BankAccountManager()
    
    def __unicode__(self):
        return "%s (%s, %s)" % (self.number,
                               self.get_accounttype_display(),
                               self.user.username)
                               
    def _get_balance(self):
        as_payer = self.transaction_as_payer_set.all().values('value')
        as_payer_value = Decimal(0)
        for i in as_payer:
            as_payer_value += i['value']
            
        as_payee = self.transaction_as_payee_set.all().values('value')
        as_payee_value = Decimal(0)
        for j in as_payee:
            as_payee_value += j['value']
            
        balance = as_payee_value - as_payer_value
        
        return balance
        
    balance = property(_get_balance) 
      
      
class  Transaction(models.Model):
    payer = models.ForeignKey(BankAccount, 
                              related_name='%(class)s_as_payer_set')
    payee = models.ForeignKey(BankAccount,
                              related_name='%(class)s_as_payee_set')
    value = models.DecimalField(max_digits=19, decimal_places=2)
    details = models.TextField()
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.details
