from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Wallet
from common.responses import SuccessResponse, ErrorResponse
from .seializers import DepositSerializer, WithdrawalSerializer, WalletSimpleSerializer
from common.utils import format_first_error
from django.db.models import F
from accounts.permissions import IsAdmin

class WalletEditView(generics.UpdateAPIView):
    serializer_class = WalletSimpleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Wallet.objects.all()
    lookup_field = 'id'

class WithdrawFromWalletView(generics.CreateAPIView):
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wallet = Wallet.objects.get(user=request.user)
            source = serializer.validated_data.get('source')
            amount = serializer.validated_data.get('amount')
            
            key = "account_balance" if source == "account" else "sales_balance"
            if getattr(wallet, key) < serializer.validated_data['amount']:
                return ErrorResponse(message="Insufficient balance")
            
            if key=='account_balance':
                wallet.account_balance = F('account_balance') - amount
            
            if key =='sales_balance':
                wallet.sales_balance = F(key) - amount
            
            wallet.save()
                    
        else:
            return ErrorResponse(message=format_first_error(serializer.errors))
        return super().create(request, *args, **kwargs)

class DepositIntoWalletView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class GetWalletBalanceView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        return SuccessResponse(message="User balance", data={
            'sales_balance': wallet.sales_balance,
            'account_balance': wallet.account_balance
        })