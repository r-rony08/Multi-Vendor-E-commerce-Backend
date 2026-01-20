import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from products.models import Product, Category
from carts.models import CartItem
from orders.models import Order, OrderItem
from vendors.models import Vendor

User = get_user_model()


# Helper function to auto-create Vendor if user.role == 'VENDOR'
def create_vendor_for_user(user):
    if user.role == 'VENDOR':
        return Vendor.objects.create(user=user, shop_name=f"{user.username}'s Shop")
    return None


@pytest.mark.django_db
def test_order_creation_and_stock():
    client = APIClient()

    # Create customer user
    user = User.objects.create_user(username='customer', password='pass')

    # Create vendor user
    vendor_user = User.objects.create_user(username='vendor', password='pass', role='VENDOR')
    vendor = create_vendor_for_user(vendor_user)  # auto-create Vendor object

    # Create product linked to vendor
    product = Product.objects.create(
        name='Test Product', 
        price=100, 
        stock=5, 
        vendor=vendor
    )

    # Add to cart
    CartItem.objects.create(user=user, product=product, quantity=2)

    client.force_authenticate(user=user)

    # Create order
    response = client.post('/api/orders/create/')
    assert response.status_code == 201

    order = Order.objects.get(id=response.data['order_id'])
    assert order.total_price == 200  # 100 * 2

    # Check stock deducted
    product.refresh_from_db()
    assert product.stock == 3
