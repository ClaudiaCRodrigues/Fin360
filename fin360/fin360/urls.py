# fin360/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # 1) Toda requisição a '/' redireciona para a URL nomeada 'login'
    path(
        '',
        RedirectView.as_view(pattern_name='login', permanent=False),
        name='root-redirect'
    ),

    # 2) URLs de login/logout/password management do Django
    path('accounts/', include('django.contrib.auth.urls')),

    # 3) Sua área interna (dashboard, home etc.), que agora pode ficar em /dashboard/
    path('dashboard/', include('core.urls'), name='dashboard'),

    # 4) Admin
    path('admin/', admin.site.urls),
]

# Servir arquivos estáticos em DEV
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
