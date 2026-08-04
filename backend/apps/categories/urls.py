from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path("categories/<slug:slug>/", views.SingleCategoryView.as_view(), name="category-detail"),
]