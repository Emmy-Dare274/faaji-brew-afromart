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
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/products/", views.staff_product_list, name="staff_product_list"),
    path("staff/products/add/", views.staff_product_add, name="staff_product_add"),
    path("staff/products/<slug:slug>/edit/", views.staff_product_edit, name="staff_product_edit"),
    path("staff/products/<slug:slug>/toggle-active/", views.staff_product_toggle_active, name="staff_product_toggle_active"),
    path("staff/products/<slug:slug>/delete/", views.staff_product_delete, name="staff_product_delete"),
    path("staff/categories/", views.staff_category_list, name="staff_category_list"),
    path("staff/categories/add/", views.staff_category_add, name="staff_category_add"),
    path("staff/categories/<slug:slug>/edit/", views.staff_category_edit, name="staff_category_edit"),
    path("staff/categories/<slug:slug>/delete/", views.staff_category_delete, name="staff_category_delete"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
]
