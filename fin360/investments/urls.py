from django.urls import path
from .views import (
    InvestmentTypeListView,
    InvestmentTypeCreateView,
    InvestmentTypeUpdateView,
    InvestmentTypeDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
)

urlpatterns = [
    path('investment-types/', InvestmentTypeListView.as_view(), name='investment_type_list'),
    path('investment-types/new/', InvestmentTypeCreateView.as_view(), name='investment_type_create'),
    path('investment-types/<int:pk>/edit/', InvestmentTypeUpdateView.as_view(), name='investment_type_update'),
    path('investment-types/<int:pk>/delete/', InvestmentTypeDeleteView.as_view(), name='investment_type_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/delete/', CategoryUpdateView.as_view(), name='category_delete'),
]
