from django.contrib import admin
from .models import InvestmentType,Category,FinancialInstitution

@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_type', 'cnpj', 'website')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'cnpj', 'code')
    list_filter = ('institution_type',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(InvestmentType)
class InvestmentTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)