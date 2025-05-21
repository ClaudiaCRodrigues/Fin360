from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import InvestmentType,Category

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