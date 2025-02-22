from rest_framework import generics
from .serializers import CategorySerializer, NftSerializer, BuyNftSerializer, SaleSerializer, CategoryProductSerializer
from rest_framework import permissions
from .models import Category, Nft, Sale
from common.responses import SuccessResponse, ErrorResponse
from common.utils import format_first_error
from wallet.models import Wallet
from django.db.models import Q
from decimal import Decimal
from rest_framework.response import Response

class GetRelatedNft(generics.ListAPIView):
    serializer_class = NftSerializer
    def get_queryset(self):
        try:
            nft = Nft.objects.get(id=self.kwargs.get('id'))
        except Nft.DoesNotExist:
            return Nft.objects.none()
    
        return Nft.objects.filter(category=nft.category)

class GetUserNftList(generics.ListAPIView):
    serializer_class = NftSerializer
    def get_queryset(self):
        return Nft.objects.filter(owner=self.kwargs.get('owner_id'))

class GetNftListView(generics.ListAPIView):
    queryset = Nft.objects.all()
    serializer_class = NftSerializer

class CategoryProductListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializer
    queryset = Category.objects.all()


class SalesListView(generics.ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        q1 = Q(buyer=self.request.user)
        q2 = Q(seller=self.request.user)
        #TODO: filter by q1 and q2
        return Sale.objects.all()
        

class BuyNftView(generics.GenericAPIView):
    serializer_class = BuyNftSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                nft = Nft.objects.get(id=serializer.validated_data.get('id'))
            except Nft.DoesNotExist:
                return ErrorResponse(message="Nft does not exist")
            
            if nft.owner == request.user:
                return ErrorResponse(message="You cannot purchase your own NFT")
                    
            owner_wallet, created = Wallet.objects.get_or_create(user=nft.owner)
            user_wallet, created= Wallet.objects.get_or_create(user=request.user)
            
            if user_wallet.account_balance < nft.price:
                return ErrorResponse(message="Insufficient funds")
            
            Sale.objects.create(nft=nft, buyer=request.user, seller=nft.owner, amount=nft.price)

            user_wallet.account_balance -= nft.price
            owner_wallet.sales_balance += nft.price
            
            user_wallet.save()
            owner_wallet.save()
            
            nft.owner = request.user
            nft.save()
            
            return SuccessResponse(message="Success!!, you now own this nft")
        else:
            return ErrorResponse(message=format_first_error(serializer.errors))


class NftDetailsView(generics.RetrieveAPIView):
    serializer_class = NftSerializer
    lookup_field = 'id'
    queryset = Nft.objects.all()


class GetProductForCategoryView(generics.ListAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.AllowAny]
    
    default_category_description = "Step into a dynamic digital marketplace where creators and collectors unite to buy, sell, and trade one-of-a-kind NFTs. Dive into a diverse collection of digital assets, from art and collectibles to music, videos, and beyond—each securely authenticated on the blockchain to ensure verified ownership and rarity."
    

    def list(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.get(id=int(self.kwargs.get('category_id')))
        except:
            nft_list = Nft.objects.all()
            category = Category(name=str(category_id).capitalize(), description=self.default_category_description)
            return SuccessResponse(message="Category", data={
                "category": CategorySerializer(category).data,
                "nfts": NftSerializer(nft_list, many=True).data
            })
            
        nft_list = Nft.objects.filter(category=int(category_id))
        
        return SuccessResponse(message="Category", data={
            "category": CategorySerializer(category).data,
            "nfts": NftSerializer(nft_list, many=True).data
        })

class UpdateNftView(generics.UpdateAPIView):
    serializer_class = NftSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field='id'
    def get_queryset(self):
        return Nft.objects.filter(owner=self.request.user)

class GetUserNftsView(generics.ListAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Nft.objects.filter(owner=self.request.user)

class CreateCategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()




class UploadNftView(generics.ListCreateAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Nft.objects.all()
    
    
    def create(self, request, *args, **kwargs):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        wallet.account_balance -= Decimal(0.2)
        wallet.save()
        return super().create(request, *args, **kwargs)