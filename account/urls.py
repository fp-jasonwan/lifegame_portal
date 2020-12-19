from django.contrib.auth import views

from django.urls import path, include
from account.forms import UserLoginForm
urlpatterns = [
    
    path('', include('django.contrib.auth.urls')),
    path(
        'login/',
        views.LoginView.as_view(
            template_name="login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
)
]