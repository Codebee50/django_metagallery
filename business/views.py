from django.shortcuts import render
from rest_framework import generics
from .models import Business
from .serializers import BusinessSerializer
from accounts.permissions import IsAdmin, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from wallet.seializers import DepositSerializer, WithdrawalSerializer
from wallet.models import Deposit, Withdrawal, WithdrawalSourceChoices
from product.serializers import NftSerializer
from product.models import Nft, Sale
from common.responses import ErrorResponse, SuccessResponse
from django.db.models import F
from accounts.emails import send_raw_email
from product.serializers import SaleSerializer
from accounts.mixins import IsAdminMixin


class GetAllSalesView(IsAdminMixin, generics.ListAPIView):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()


class VerifyNftView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        nft_id = kwargs.get("nft_id")

        try:
            nft = Nft.objects.get(id=nft_id)
        except Nft.DoesNotExist:
            return ErrorResponse(message="Nft not found")

        nft.is_admin_approved = True
        nft.save()

        send_raw_email(
            nft.owner.email,
            "Nft verified",
            f"Hurrayy!! {nft.owner.username} Your nft was approved and is now listed",
        )

        return SuccessResponse(message="Nft verified successfully")


class DeclineNftView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        nft_id = kwargs.get("nft_id")

        try:
            nft = Nft.objects.get(id=nft_id)
        except Nft.DoesNotExist:
            return ErrorResponse(message="Nft not found")

        nft.is_admin_approved = False
        nft.save()

        send_raw_email(
            nft.owner.email,
            "Nft declined",
            f"Hello {nft.owner.username} Your nft was declined by the admin",
        )

        return SuccessResponse(message="Nft declined successfully")


class GetNftList(generics.ListAPIView):
    serializer_class = NftSerializer
    queryset = Nft.objects.all()


class DeclineWithdrawalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        withdrawal_id = kwargs.get("withdrawal_id")

        try:
            withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        except Withdrawal.DoesNotExist:
            return ErrorResponse(message="Withdrawal not found")

        if not withdrawal.is_admin_verified:
            return ErrorResponse(message="Withdrawal is already declined")

        if withdrawal.source == WithdrawalSourceChoices.SALES:
            withdrawal.wallet.sales_balance = F("sales_balance") + withdrawal.amount
        else:
            withdrawal.wallet.account_balance = F("account_balance") + withdrawal.amount

        withdrawal.wallet.save()
        withdrawal.initial_admin_activity = True
        withdrawal.is_admin_verified = False
        withdrawal.save()
        send_raw_email(
            withdrawal.wallet.user.email,
            "Withdrawal declined",
            f"Hello {withdrawal.wallet.user.username} Your withdrawal request has been declined",
        )

        return SuccessResponse(
            message="Withdrawal declined successfully",
            data=WithdrawalSerializer(withdrawal).data,
        )


class VerifyWithdrawalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        withdrawal_id = kwargs.get("withdrawal_id")

        try:
            withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        except Withdrawal.DoesNotExist:
            return ErrorResponse(message="Withdrawal not found")

        if withdrawal.is_admin_verified:
            return ErrorResponse(message="Withdrawal is already verified")

        if withdrawal.initial_admin_activity:
            if withdrawal.source == WithdrawalSourceChoices.SALES:
                withdrawal.wallet.sales_balance = F("sales_balance") - withdrawal.amount
            else:
                withdrawal.wallet.account_balance = (
                    F("account_balance") - withdrawal.amount
                )

        withdrawal.is_admin_verified = True
        withdrawal.initial_admin_activity = True
        withdrawal.save()

        send_raw_email(
            withdrawal.wallet.user.email,
            "Withdrawal verified",
            f"Hello {withdrawal.wallet.user.username} Your withdrawal has been processed successfully",
        )
        return SuccessResponse(
            message="Withdrawal verified successfully",
            data=WithdrawalSerializer(withdrawal).data,
        )


class DeclineDepositView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        deposit_id = kwargs.get("deposit_id")
        try:
            deposit = Deposit.objects.get(id=deposit_id)
        except Deposit.DoesNotExist:
            return ErrorResponse(message="Deposit not found")

        if not deposit.is_admin_verified:
            return ErrorResponse(message="Cannot decline a pending deposit")

        deposit.wallet.sales_balance = F("sales_balance") - deposit.amount
        deposit.wallet.save()

        deposit.is_admin_verified = False
        deposit.save()

        send_raw_email(
            deposit.wallet.user.email,
            "Deposit declined",
            f"Hello {deposit.wallet.user.username} Your deposit request has been declined",
        )

        return SuccessResponse(message="Deposit verified successfully")


class VerifyDepositEndpoint(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        deposit_id = kwargs.get("deposit_id")
        try:
            deposit = Deposit.objects.get(id=deposit_id)
        except Deposit.DoesNotExist:
            return ErrorResponse(message="Deposit not found")

        if deposit.is_admin_verified:
            return ErrorResponse(message="Cannot verify an already verified deposit")

        deposit.wallet.account_balance = F("account_balance") + deposit.amount
        deposit.wallet.save()

        deposit.is_admin_verified = True
        deposit.save()

        send_raw_email(
            deposit.wallet.user.email,
            "Deposit verified",
            f"Hello {deposit.wallet.user.username} Your Deposit has been processed successfully",
        )

        return SuccessResponse(message="Deposit verified successfully")


class GetWithdrawalView(generics.ListAPIView):
    queryset = Withdrawal.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = WithdrawalSerializer


class GetDeposits(generics.ListAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Deposit.objects.all()


class EditBusiness(generics.UpdateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        return Business.objects.first()


class GetBusiness(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer

    def get_object(self):
        return Business.objects.first()
