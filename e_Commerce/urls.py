from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from products.views import ProductDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/", include("users.urls", namespace="users")),
    path("api/v1/vendors/", include("vendors.urls", namespace="vendors")),
    path("api/v1/products/", include("products.urls", namespace="products")),
    path("api/v1/products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail-slug"),
    path("api/v1/orders/", include("orders.urls", namespace="orders")),
    path("api/v1/carts/", include("carts.urls", namespace="carts")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/analytics/", include("analytics.urls")),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
