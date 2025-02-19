from rest_framework import generics
from .serializers import CategorySerializer, NftSerializer
from rest_framework import permissions
from .models import Category, Nft


class CreateCategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()




class UploadNftView(generics.ListCreateAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Nft.objects.all()