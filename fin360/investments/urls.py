# investments/urls.py

from django.urls import path
from .views import InvestmentTypeListView

urlpatterns = [
    path('investment-types/', InvestmentTypeListView.as_view(), name='investment_type_list'),
]
