from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("wishlist/", views.wishlist_detail, name="wishlist_detail"),
    path("wishlist/toggle/<slug:product_slug>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("account/", views.my_account, name="my_account"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<str:order_number>/reorder/", views.reorder, name="reorder"),
]