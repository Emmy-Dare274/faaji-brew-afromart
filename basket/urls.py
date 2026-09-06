from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path("", views.basket_detail, name="basket_detail"),
    path("add/<slug:product_slug>/", views.add_to_basket, name="add_to_basket"),
    path("update/<int:item_id>/", views.update_basket_item, name="update_basket_item"),
    path("remove/<int:item_id>/", views.remove_basket_item, name="remove_basket_item"),
]