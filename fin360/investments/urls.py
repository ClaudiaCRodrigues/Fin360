from django.urls import path
from .views import (
    InvestmentTypeListView,
    InvestmentTypeCreateView,
    InvestmentTypeUpdateView,
    InvestmentTypeDeleteView,
)

urlpatterns = [
    path('investment-types/', InvestmentTypeListView.as_view(), name='investment_type_list'),
    path('investment-types/new/', InvestmentTypeCreateView.as_view(), name='investment_type_create'),
    path('investment-types/<int:pk>/edit/', InvestmentTypeUpdateView.as_view(), name='investment_type_update'),
    path('investment-types/<int:pk>/delete/', InvestmentTypeDeleteView.as_view(), name='investment_type_delete'),
]
