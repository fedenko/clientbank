# -*- coding: UTF-8 -*-
from django.contrib import auth

from django.utils.translation import ugettext as _

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from cbank.jsonrpc import JSONRPCService, jsonremote #, FormProcessor

from cbank.models import BankAccount

service = JSONRPCService()

#formservice = FormProcessor({})

def index(request):
    get_token(request)
    return render_to_response('ClientBank.html')
    
@jsonremote(service)
def login(request, username, password):
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return True
        else:
            return _(u"Your account has been disabled!")
    else:
        return _(u"Your username and password were incorrect.")
        
@jsonremote(service)
def isauthenticated(request):
    return request.user.is_authenticated()
    
@jsonremote(service)
def logout(request):
    auth.logout(request)
    return True
    
@jsonremote(service)
def register(request,username, password1, password2):
    data = {'username': username,
            'password1': password1,
            'password2': password2}
            
    form = auth.forms.UserCreationForm(data)
    if form.is_valid():
        new_user = form.save()
        new_user.is_active = False
        new_user.save()
        return True
    else:    
        return form.errors
        
    
@jsonremote(service)       
def getaccounts(request):
    if request.user.is_authenticated():        
        accounts = BankAccount.objects.filter(user = request.user)
        return [{'id': account.id,
                 'number': account.number,
                 'type': account.get_accounttype_display(),
                 'balance': '%.2f' % account.balance} for account in accounts]
    else:
        return False



