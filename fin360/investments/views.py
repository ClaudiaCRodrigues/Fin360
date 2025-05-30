from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Max
from .forms import PdfImportForm
from .models import FinancialInstitution, Category, InvestmentType, Index, InvestmentTransaction
from .services import sync_indices, processar_importacao

def importar_investimentos(request):
    if request.method == "POST":
        step = request.POST.get("step", "upload")
        arquivos = request.FILES.getlist("arquivos")

        # passo 1: upload e detecção
        if step == "upload":
            resultados = processar_importacao(arquivos)
            faltantes = [r for r in resultados if r["broker"] is None]
            if faltantes:
                # renderiza seleção de corretora
                return render(request, "imports/missing_institutions.html", {
                    "step": "select",
                    "faltantes": faltantes,
                    "institutions": FinancialInstitution.objects.all()
                })
            # se todos identificados, mostra resultado
            return render(request, "imports/resultado.html", {"resultados": resultados})

        # passo 2: usuário escolheu manualmente
        if step == "select":
            # recupera overrides: map file_name -> inst
            overrides = {}
            for idx, file_name in enumerate(request.POST.getlist("file_names")):
                sel = request.POST.get(f"broker_for_{idx}")
                if sel:
                    overrides[file_name] = FinancialInstitution.objects.get(pk=sel)

            # reusa os mesmos arquivos do upload
            resultados = processar_importacao(arquivos, overrides)
            return render(request, "imports/resultado.html", {"resultados": resultados})

    # GET ou erro
    return render(request, "imports/form_import.html", {"error_message": None})

class IndexSummaryListView(TemplateView):
    template_name = 'investments/index_summary_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        summary = []
        # Busca o último registro para cada índice
        for name, last_date in Index.objects.values_list('name').annotate(last_date=Max('date')):
            last_record = Index.objects.get(name=name, date=last_date)
            summary.append({
                'name': name,
                'last_date': last_date,
                'last_value': last_record.value,
            })
        ctx['indices'] = summary
        return ctx


class IndexDetailView(ListView):
    model = Index
    template_name = 'investments/index_detail.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Index.objects.filter(name=self.kwargs['name']).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['index_name'] = self.kwargs['name']
        return ctx


class SyncIndicesView(View):
    def get(self, request, *args, **kwargs):
        try:
            count = sync_indices()
            count = sync_indices(years=1)
            messages.success(request, f"{count} novos registros importados.")
        except Exception as e:
            messages.error(request, f"Erro ao sincronizar: {e}")
        return redirect('index_summary')


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
    fields = ['name', 'slug', 'institution_type', 'code', 'cnpj', 'website', 'email', 'phone_number', 'address']
    template_name = 'investments/institution_form.html'
    success_url = reverse_lazy('institution_list')


class InstitutionUpdateView(UpdateView):
    model = FinancialInstitution
    fields = ['name', 'slug', 'institution_type', 'code', 'cnpj', 'website', 'email', 'phone_number', 'address']
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
    context_object_name = 'category'
    template_name = 'investments/category_detail.html'
    slug_field = 'slug'

    def get_queryset(self):
        return Category.objects.prefetch_related('investment_types')


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
    template_name = 'investments/investment_type_list.html'
    context_object_name = 'types'


class InvestmentTypeCreateView(CreateView):
    model = InvestmentType
    fields = ['nome', 'category', 'descricao']
    template_name = 'investments/investment_type_form.html'
    success_url = reverse_lazy('investment_type_list')


class InvestmentTypeUpdateView(UpdateView):
    model = InvestmentType
    fields = ['nome', 'category', 'descricao']
    template_name = 'investments/investment_type_form.html'
    success_url = reverse_lazy('investment_type_list')


class InvestmentTypeDeleteView(DeleteView):
    model = InvestmentType
    template_name = 'investments/investment_type_confirm_delete.html'
    success_url = reverse_lazy('investment_type_list')


class PortfolioView(TemplateView):
    template_name = 'investments/portfolio.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['transactions'] = InvestmentTransaction.objects.select_related('investment').all()
        # Se quiser somar o valor total:
        ctx['total_portfolio'] = sum(tx.quantity * tx.price for tx in ctx['transactions'])
        return ctx
