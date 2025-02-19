from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.RegisterUserView.as_view(), name='register-user'),
   path('login/', views.LoginView.as_view(), name='login-view') 
]