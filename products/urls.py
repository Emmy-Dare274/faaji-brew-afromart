from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("categories/", views.category_overview, name="category_overview"),
    path("special-offers/", views.special_offers, name="special_offers"),
    path("product/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path("product/<slug:product_slug>/review/", views.add_review, name="add_review"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("reviews/moderate/", views.review_moderation, name="review_moderation"),
    path("review/<int:review_id>/approve/", views.approve_review, name="approve_review"),
    path("review/<int:review_id>/reject/", views.reject_review, name="reject_review"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
]
