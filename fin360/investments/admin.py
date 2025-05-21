from django.contrib import admin
from .models import InvestmentType

@admin.register(InvestmentType)
class InvestmentTypeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)