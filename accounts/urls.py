from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.RegisterUserView.as_view(), name='register-user'),
   path('login/', views.LoginView.as_view(), name='login-view') ,
   path('me/', views.GetUserProfileView.as_view(), name='get-user-profile'),
   path("user/update/", views.UpdateUserView.as_view(), name='update-user-view'),
   path('user/password/change/', views.ChangePasswordView.as_view(), name='change-password'),
   path('logout/', views.LogoutApi.as_view(), name='logout'),
   path('user/list/', views.UserListApi.as_view(), name='user-list')
]