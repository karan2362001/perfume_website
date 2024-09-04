from django.urls import path
from . import views
urlpatterns = [
    path("product/", views.CartItems.as_view(),name = "add_cart")
   
]
