from django.contrib import auth
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from cbank.network import *

service = JSONRPCService()

def index(request):
    get_token(request)
    return render_to_response('ClientBank.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse("ok")
        else:
            return HttpResponse("Your account has been disabled!")
    else:
        return HttpResponse("Your username and password were incorrect.")
        
        
@jsonremote(service)
def isAuthenticated(request):
    return request.user.is_authenticated()

