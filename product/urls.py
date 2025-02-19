from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CreateCategoryView.as_view(), name='create-category'),
    path('nft/upload/', views.UploadNftView.as_view(), name='upload-nft')
]