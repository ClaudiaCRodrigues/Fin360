# fin360/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from investments.views import InvestmentTypeListView

urlpatterns = [
    path(
        '',
        RedirectView.as_view(pattern_name='login', permanent=False),
        name='root-redirect'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('core.urls'), name='dashboard'),
    path('admin/', admin.site.urls),
    path('', include('investments.urls')),
]

# Servir arquivos estáticos em DEV
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
