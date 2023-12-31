import random
from datetime import datetime 
import pyotp

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.signing import Signer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django_ratelimit.decorators import ratelimit

from .models import User
from .forms import UserRegistrationForm
from .utils import send_otp
#from django.contrib.auth.forms import UserCreationForm


@ratelimit(key='ip', rate='5/m')
@login_required(login_url='login/')
def index(request):

    return HttpResponse(f" {request.user} / {request.session.values()}")

def register(request):
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data["email"]
            signer = Signer()
            signed_obj = signer.sign_object(data)
            send_mail(
                "Account verification",
                f"http://127.0.0.1:8000/verification/{signed_obj}",
                "from@example.com",
                [email],
                fail_silently=False,
            )
            return redirect('/waiting/')

    form = UserRegistrationForm()      
    context = {
        "form": form,
    }

    return render(request, 'core/signup.html', context)


def waiting(request):

    return HttpResponse("You will recieve a verification Email. check your emails.")


def email_registration_view(request, token):
    signer = Signer()
    obj = signer.unsign_object(token)
    if obj:
        form = UserRegistrationForm(data=obj)
        form.save()
        return redirect('/')



def login_view(request):
    error_message = None
    if request.method == 'POST':
        credentials = request.POST
        username = credentials["username"]
        password = credentials["password"]
        user = authenticate(request, username=username, password=password )
        if user is not None:
            
            if user.is_2fa_enabled:
                # generate otp
                send_otp(request)
                request.session["username"] = user.username
                # email pass
                return redirect('otp-view')
            else:
                login(request, user)
                return redirect('/')
        else:
            error_message = "User doesn't exist"
    
    form = AuthenticationForm
    context = {"form": form, "error_msg": error_message}
    return render(request, 'core/login.html', context)



def otp_view(request):
    error_message = None
    if request.method == "POST":
        otp = request.POST["otp"]
        otp_secret_key = request.session["otp_secret_key"]
        otp_valid_until = request.session["otp_valid_date"]
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    # get user
                    username = request.session["username"]
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    return redirect('index-view')
                else:
                    error_message = "Invalid one time password"
            else:
                error_message = "Token has expired"
        else:
            error_message = "something went wrong :( "
    
    return render(request, 'core/otp.html', {"error_msg": error_message})