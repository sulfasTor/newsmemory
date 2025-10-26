from django.urls import path

from .views import health, orders

urlpatterns = [path("health/", health, name="health"), path("orders/", orders, name="orders")]
