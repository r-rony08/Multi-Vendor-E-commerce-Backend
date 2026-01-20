from django.urls import path
from .views import CartItemListCreateView, CartItemDetailView, CartSummaryView

app_name = "carts"

urlpatterns = [
    path("", CartItemListCreateView.as_view(), name="cart-list-create"),
    path("<int:pk>/", CartItemDetailView.as_view(), name="cart-detail"),
    path("summary/", CartSummaryView.as_view(), name="cart-summary"),
]
