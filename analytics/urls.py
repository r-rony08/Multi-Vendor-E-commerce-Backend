from django.urls import path
from .views import AdminAnalyticsView

app_name = "analytics"

urlpatterns = [
    path("admin/analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
]
