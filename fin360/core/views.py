from django.shortcuts import render


def home(request):
    # Dados iniciais podem ser adicionados ao context mais tarde
    return render(request, 'core/dashboard.html', {})