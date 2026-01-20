import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from orders.models import Order
from payments.models import Payment
from vendors.models import Vendor
from products.models import Product

User = get_user_model()


def create_vendor_for_user(user):
    if user.role == 'VENDOR':
        return Vendor.objects.create(user=user, shop_name=f"{user.username}'s Shop")
    return None


@pytest.mark.django_db
def test_payment_webhook():
    client = APIClient()

    # Create customer user
    user = User.objects.create_user(username='customer', password='pass')

    # Create vendor user
    vendor_user = User.objects.create_user(username='vendor', password='pass', role='VENDOR')
    vendor = create_vendor_for_user(vendor_user)

    # Create product and order
    product = Product.objects.create(name='Test Product', price=100, stock=5, vendor=vendor)
    order = Order.objects.create(user=user, total_price=100)

    # Create payment for order
    payment = Payment.objects.create(order=order, amount=100, gateway='STRIPE_SANDBOX')

    # Simulate webhook
    response = client.post('/api/payments/webhook/', data={
        "payment_id": payment.id,
        "status": "success"
    })
    assert response.status_code == 200

    payment.refresh_from_db()
    order.refresh_from_db()
    assert payment.status == 'SUCCESS'
    assert order.status == 'PAID'
