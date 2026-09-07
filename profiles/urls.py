from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("wishlist/", views.wishlist_detail, name="wishlist_detail"),
    path("wishlist/toggle/<slug:product_slug>/", views.toggle_wishlist, name="toggle_wishlist"),
]