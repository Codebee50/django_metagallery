from . import views
from django.urls import path


urlpatterns = [
    path('', views.GetBusiness.as_view(), name='get-business-view'),
    path('edit/', views.EditBusiness.as_view(), name='edit-business'),
    path('deposit/all/', views.GetDeposits.as_view(), name='get-deposits'),
    path('withdrawals/all/', views.GetWithdrawalView.as_view(), name='get-withdrawals'),
    path('deposit/verify/<uuid:deposit_id>/', views.VerifyDepositEndpoint.as_view(), name='verify-deposit'),
    path('deposit/decline/<uuid:deposit_id>/', views.DeclineDepositView.as_view(), name='decline-deposit'),
    path('withdrawal/verify/<uuid:withdrawal_id>/', views.VerifyWithdrawalView.as_view(), name='verify-withdrawal'),
    path('withdrawal/decline/<uuid:withdrawal_id>/', views.DeclineWithdrawalView.as_view(), name='verify-withdrawal'),
    path('nft/all/', views.GetNftList.as_view(), name='get-nft-list'),
    path('nft/verify/<uuid:nft_id>/', views.VerifyNftView.as_view(), name='verify-nft'),
    path('nft/decline/<uuid:nft_id>/', views.DeclineNftView.as_view(), name='decline-nft')
]