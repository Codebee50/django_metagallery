from rest_framework import serializers
from .models import Deposit, Wallet, Withdrawal

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Wallet
        
        
class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Withdrawal
        read_only_fields = ['wallet', 'is_admin_verified', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        wallet, created = Wallet.objects.get_or_create(user=user)
        validated_data['wallet'] = wallet

        return super().create(validated_data)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero')
        return value
    
    
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Deposit
        read_only_fields= ['wallet', 'is_admin_verified', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        wallet, created = Wallet.objects.get_or_create(user=user)
        validated_data['wallet'] = wallet
        return super().create(validated_data)