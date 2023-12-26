from django.urls import path
from django.contrib.auth.views import LoginView
from .views import index


urlpatterns = [
    path('', index, name='index-view'),
    path('login/', LoginView.as_view(template_name="core/login.html", next_page="/"), name='login-view')
]