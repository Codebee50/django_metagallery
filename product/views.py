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
from business.models import Business
from accounts.emails import send_raw_email
from accounts.models import UserAccount
from accounts.serializers import UserSerializer


class GetUserAndNfts(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            return ErrorResponse(message="User not found")

        nfts = Nft.objects.filter(owner=user)
        return SuccessResponse(message="User account and nfts", data={
            'user': UserSerializer(user, context={'request': request}).data,
            'nfts': NftSerializer(nfts, many=True, context={'request': request}).data
        })
        

class GetRelatedNft(generics.ListAPIView):
    serializer_class = NftSerializer
    def get_queryset(self):
        try:
            nft = Nft.objects.get(id=self.kwargs.get('id'))
        except Nft.DoesNotExist:
            return Nft.objects.none()
    
        return Nft.approved.filter(category=nft.category)

class GetUserNftList(generics.ListAPIView):
    serializer_class = NftSerializer
    def get_queryset(self):
        return Nft.approved.filter(owner=self.kwargs.get('owner_id'))

class GetNftListView(generics.ListAPIView):
    queryset = Nft.approved.all()
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


class CategoryOrSearchView(generics.ListAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.AllowAny]
    
    default_category_description = "Step into a dynamic digital marketplace where creators and collectors unite to buy, sell, and trade one-of-a-kind NFTs. Dive into a diverse collection of digital assets, from art and collectibles to music, videos, and beyond—each securely authenticated on the blockchain to ensure verified ownership and rarity."

    def list(self, request, *args, **kwargs):
        category_name = self.kwargs.get('category_name')
        search_term = request.query_params.get('search')
        
        
        if search_term:
            nft_list= Nft.objects.filter(title__icontains=search_term)
            category = Category(name=str(search_term).capitalize(), description=self.default_category_description)
            return SuccessResponse( message="Category search", data={
                "category": CategorySerializer(category).data,
                "nfts": NftSerializer(nft_list, many=True, context={"request": request}).data   
            })
        
        category_list = Category.objects.filter(name__iexact=category_name)
        if category_list.exists():
            category = category_list.first()
            nft_list = Nft.objects.filter(category__name__iexact=category_name)
        else:
            category = Category(name=str(category_name).capitalize(), description=self.default_category_description)
            nft_list = Nft.objects.filter(category__name__icontains=category_name)
        
        return SuccessResponse( message="Category search", data={
            "category": CategorySerializer(category).data,
            "nfts": NftSerializer(nft_list, many=True, context={'request': request}).data   
        })
                    

class GetProductForCategoryView(generics.ListAPIView):
    serializer_class = NftSerializer
    permission_classes = [permissions.AllowAny]
    
    default_category_description = "Step into a dynamic digital marketplace where creators and collectors unite to buy, sell, and trade one-of-a-kind NFTs. Dive into a diverse collection of digital assets, from art and collectibles to music, videos, and beyond—each securely authenticated on the blockchain to ensure verified ownership and rarity."
    

    def list(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.get(id=int(self.kwargs.get('category_id')))
        except:
            nft_list = Nft.objects.filter(is_admin_approved=True)
            category = Category(name=str(category_id).capitalize(), description=self.default_category_description)
            return SuccessResponse(message="Category", data={
                "category": CategorySerializer(category).data,
                "nfts": NftSerializer(nft_list, many=True).data
            })
            
        nft_list = Nft.objects.filter(category=int(category_id), is_admin_approved=True )
        
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
        
        
        business = Business.objects.first()
        
        minting_fee = business.minting_fee if business else 0.2
        
        if wallet.account_balance < minting_fee:
            return ErrorResponse(message=f"Insufficient balance, you need at least {minting_fee} eth in your account balance in order to mint nfts")
        wallet.account_balance -= minting_fee
        wallet.save()
        
        send_raw_email(business.email, 'New nft upload', "A user has uploaded a new nft on the site, please login to approve it")
        return super().create(request, *args, **kwargs)