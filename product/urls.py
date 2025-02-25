from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CreateCategoryView.as_view(), name='create-category'),
    path('nft/upload/', views.UploadNftView.as_view(), name='upload-nft'),
    path('nft/user/list/', views.GetUserNftsView.as_view(), name='get-user-nfts'),
    path('nft/update/<uuid:id>/', views.UpdateNftView.as_view(), name='update-nft'),
    path('nft/category/<str:category_id>/', views.GetProductForCategoryView.as_view(), name='get-product-for-category'),
    path('nft/detail/<uuid:id>/', views.NftDetailsView.as_view(), name='nft-details'),
    path('nft/buy/', views.BuyNftView.as_view(), name='buy-nft'),
    path('nft/user/sales/', views.SalesListView.as_view(), name='sale-list'),
    path('category/products/', views.CategoryProductListView.as_view(), name='category-product-list'),
    path('nft/', views.GetNftListView.as_view(), name='get-nft-list'),
    path('nft/user/<uuid:owner_id>/', views.GetUserNftList.as_view(), name='get-user-nfts'),
    path('nft/related/<uuid:id>/', views.GetRelatedNft.as_view(), name='get-related-nft'),
    path('nft/creator/<str:username>/', views.GetUserAndNfts.as_view(), name='get-user-and-nfts')
]