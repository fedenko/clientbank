from django.contrib import auth

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from cbank.jsonrpc import JSONRPCService, jsonremote, FormProcessor

service = JSONRPCService()

processor = FormProcessor({})

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
            return "Your account has been disabled!"
    else:
        return "Your username and password were incorrect."
        
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
            
    form = UserCreationForm(data)
    if form.is_valid():
        new_user = form.save()
        return True
    else:    
        return form.errors

