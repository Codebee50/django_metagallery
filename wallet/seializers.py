from rest_framework import serializers
from .models import Deposit, Wallet, Withdrawal
from accounts.serializers import UserSerializer
from accounts.emails import send_raw_email
from business.models import Business
from .models import Transaction, TransactionTypeChoices
class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        fields = '__all__'
        model = Wallet
        
        
class WithdrawalSerializer(serializers.ModelSerializer):
    wallet= WalletSerializer(required=False)
    class Meta:
        fields = '__all__'
        model = Withdrawal
        read_only_fields = ['wallet', 'is_admin_verified', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        wallet, created = Wallet.objects.get_or_create(user=user)
        validated_data['wallet'] = wallet
        business = Business.objects.first()
    
        amount = validated_data.get('amount')
        narration = f"Withdrawal request from {validated_data.get('source')} balance"
        transaction = Transaction.objects.create(amount=amount, transaction_type=TransactionTypeChoices.WITHDRAWAL, narration=narration)
        
        validated_data['transaction']= transaction
        wallet_address = validated_data.get('wallet_address')
        send_raw_email(business.email, "New withdrawal alert", f"Dear admin, a user is trying to withdraw {amount} into the ETH wallet address {wallet_address}")

        return super().create(validated_data)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero')
        return value


    
class DepositSerializer(serializers.ModelSerializer):
    # c
    wallet = WalletSerializer(required=False)
    class Meta:
        fields = '__all__'
        model = Deposit
        read_only_fields= ['wallet', 'is_admin_verified', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        wallet, created = Wallet.objects.get_or_create(user=user)
        validated_data['wallet'] = wallet
        
        business = Business.objects.first()
        
        amount = validated_data.get('amount')
        narration = "Wallet funding"
        
        transaction = Transaction.objects.create(amount=amount, transaction_type=TransactionTypeChoices.DEPOSIT, narration=narration)
        validated_data['transaction']=transaction
        transaction_hash = validated_data.get('transaction_hash')
        send_raw_email(business.email, "New deposit alert", f"Dear admin, a user has claims to have deposited {amount} ETH with a transaction hash of {transaction_hash}, please confirm the transaction and login to approve this deposit")
        return super().create(validated_data)