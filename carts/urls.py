from django.urls import path
from .views import CartItemListCreateView, CartItemDetailView, CartSummaryView

urlpatterns = [
    path('cart/', CartItemListCreateView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartItemDetailView.as_view(), name='cart-detail'),
    path('cart/summary/', CartSummaryView.as_view(), name='cart-summary'),

]
