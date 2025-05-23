from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)
from .models import (
    FinancialInstitution, Category, InvestmentType, Investment
)

class InstitutionListView(ListView):
    model = FinancialInstitution
    context_object_name = 'institutions'
    template_name = 'investments/institution_list.html'

class InstitutionDetailView(DetailView):
    model = FinancialInstitution
    context_object_name = 'institution'
    template_name = 'investments/institution_detail.html'
    slug_field = 'slug'

class InstitutionCreateView(CreateView):
    model = FinancialInstitution
    fields = [
        'name', 'slug', 'institution_type', 'code', 'cnpj',
        'website', 'email', 'phone_number', 'address'
    ]
    template_name = 'investments/institution_form.html'
    success_url = reverse_lazy('institution_list')

class InstitutionUpdateView(UpdateView):
    model = FinancialInstitution
    fields = [
        'name', 'slug', 'institution_type', 'code', 'cnpj',
        'website', 'email', 'phone_number', 'address'
    ]
    template_name = 'investments/institution_form.html'
    success_url = reverse_lazy('institution_list')

class InstitutionDeleteView(DeleteView):
    model = FinancialInstitution
    template_name = 'investments/institution_confirm_delete.html'
    success_url = reverse_lazy('institution_list')
class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'investments/category_list.html'
    
class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "investments/category_detail.html"
    slug_field = "slug"
    
    def get_queryset(self):
        return Category.objects.prefetch_related("investment_types")
    
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'investments/category_form.html'
    success_url = reverse_lazy('category_list')
    
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'investments/category_form.html'
    success_url = reverse_lazy('category_list')

class InvestmentTypeListView(ListView):
    model = InvestmentType
    template_name = "investments/investment_type_list.html"
    context_object_name = "types"

class InvestmentTypeCreateView(CreateView):
    model = InvestmentType
    # use o nome exato do atributo no model: category
    fields = ["nome", "category", "descricao"]
    template_name = "investments/investment_type_form.html"
    success_url = reverse_lazy("investment_type_list")

class InvestmentTypeUpdateView(UpdateView):
    model = InvestmentType
    fields = ["nome", "category", "descricao"]
    template_name = "investments/investment_type_form.html"
    success_url = reverse_lazy("investment_type_list")

class InvestmentTypeDeleteView(DeleteView):
    model = InvestmentType
    template_name = "investments/investment_type_confirm_delete.html"
    success_url = reverse_lazy("investment_type_list")
    
class PortfolioView(TemplateView):
    template_name = 'investments/portfolio.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        categories = Category.objects.prefetch_related('investments').all()
        ctx['categories'] = categories
        ctx['total_portfolio'] = sum(
            inv.current_value for cat in categories for inv in cat.investments.all()
        )
        return ctx