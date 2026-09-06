from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("categories/", views.category_overview, name="category_overview"),
    path("special-offers/", views.special_offers, name="special_offers"),
    path("product/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
]
