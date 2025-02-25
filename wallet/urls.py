from django.urls import path
from . import views

urlpatterns = [
    path('balance/', views.GetWalletBalanceView.as_view(), name='get-wallet-balance'),
    path('deposit/', views.DepositIntoWalletView.as_view(), name='deposit-into-wallet'),
    path('withdraw/', views.WithdrawFromWalletView.as_view(), name='withdraw-from-wallet'),
    path("edit/<uuid:id>/",views.WalletEditView.as_view(),name='edit-wallet')
]