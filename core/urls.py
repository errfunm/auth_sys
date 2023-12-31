from django.urls import path
from django.contrib.auth.views import LoginView
from .views import index, register, email_registration_view, waiting, login_view, otp_view


urlpatterns = [
    path('', index, name='index-view'),
    path('login/', login_view, name='login-view'),
    #path('login/', LoginView.as_view(template_name="core/login.html", next_page="/"), name='login-view'),
    path('signup/', register, ),
    path('waiting/', waiting, name='waiting-view'),
    path('verification/<str:token>', email_registration_view, name='verify-view'),
    path('login/otp/', otp_view, name="otp-view")
]