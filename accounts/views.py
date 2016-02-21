from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate


def persona_login(request):
    authenticate(assertion=request.POST['assertion'])
    return HttpResponse()