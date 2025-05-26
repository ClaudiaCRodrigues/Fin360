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
    InstitutionListView, InstitutionDetailView,
    InstitutionCreateView, InstitutionUpdateView, InstitutionDeleteView,
    PortfolioView,importar_investimentos,
    IndexSummaryListView, IndexDetailView, SyncIndicesView,
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
    path('institutions/', InstitutionListView.as_view(), name='institution_list'),
    path('institutions/novo/', InstitutionCreateView.as_view(), name='institution_create'),
    path('institutions/<slug:slug>/', InstitutionDetailView.as_view(), name='institution_detail'),
    path('institutions/<slug:slug>/editar/', InstitutionUpdateView.as_view(), name='institution_update'),
    path('institutions/<slug:slug>/excluir/', InstitutionDeleteView.as_view(), name='institution_delete'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('imports/', importar_investimentos, name='investment_import'), 
    path('indices/', IndexSummaryListView.as_view(), name='index_summary'),
    path('indices/sync/', SyncIndicesView.as_view(), name='sync_indices'),
    path('indices/<str:name>/', IndexDetailView.as_view(), name='index_detail'),

]
