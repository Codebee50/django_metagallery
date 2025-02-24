from rest_framework import serializers
from .models import Category
from .models import Nft, Sale
from accounts.serializers import UserSerializer


        

class BuyNftSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class NftSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        fields = "__all__"
        model = Nft
        read_only_fields = ['id', 'uploaded_by', 'status', 'created_at', 'updated_at', 'owner', 'is_admin_approved']
    
    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context.get('request').user
        validated_data['owner'] = self.context.get('request').user
        validated_data['is_listed'] = True
        return super().create(validated_data)

class SaleSerializer(serializers.ModelSerializer):
    buyer=UserSerializer()
    seller =UserSerializer()
    nft=NftSerializer()
    class Meta:
        model = Sale
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):
    nfts = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_nfts(self, obj):
        return NftSerializer(Nft.objects.filter(category=obj),many=True).data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
        read_only_fields = ['id', 'created_at', 'updated_at'] 