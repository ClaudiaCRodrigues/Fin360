from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import InvestmentType

class InvestmentTypeListView(ListView):
    model = InvestmentType
    template_name = 'investments/investment_type_list.html'
    context_object_name = 'types'

class InvestmentTypeCreateView(CreateView):
    model = InvestmentType
    fields = ['nome', 'descricao']
    template_name = 'investments/investment_type_form.html'
    success_url = reverse_lazy('investment_type_list')

class InvestmentTypeUpdateView(UpdateView):
    model = InvestmentType
    fields = ['nome', 'descricao']
    template_name = 'investments/investment_type_form.html'
    success_url = reverse_lazy('investment_type_list')

class InvestmentTypeDeleteView(DeleteView):
    model = InvestmentType
    template_name = 'investments/investment_type_confirm_delete.html'
    success_url = reverse_lazy('investment_type_list')
