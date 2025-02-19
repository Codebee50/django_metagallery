from rest_framework import serializers
from .models import Category
from .models import Nft

class NftSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Nft
        read_only_fields = ['id', 'uploaded_by', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context.get('request').user
        return super().create(validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
        read_only_fields = ['id', 'created_at', 'updated_at'] 