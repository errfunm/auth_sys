from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m')
@login_required(login_url='login/')
def index(request):

    return HttpResponse(f" {request.user} / {request.session}")
