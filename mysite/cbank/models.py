from django.db import models
from django.contrib.auth.models import User

from random import Random
from cbank.gencc import completed_number

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    
class BankAccountManager(models.Manager):
    def create_account(self, user):
        generator = Random()
        generator.seed()
        number = int(completed_number(generator, ['7', '7', '7', '7'], 16))
        account = self.model(user=user, number = number)
        account.save(using=self._db)
        return account

class BankAccount(models.Model):
    user = models.ForeignKey(User)
    number = models.PositiveIntegerField(unique=True)
    
    objects = BankAccountManager()
    
    def __unicode__(self):
        return u'%d' % self.number
        
class  Transaction(models.Model):
    payer = models.ForeignKey(BankAccount, related_name='%(class)s_as_payer_set')
    payee = models.ForeignKey(BankAccount, related_name='%(class)s_as_payee_set')
    value = models.DecimalField(max_digits=19, decimal_places=2)
    details = models.TextField()
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True)
