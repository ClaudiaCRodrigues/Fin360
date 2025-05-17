from django.contrib import admin
from django.urls import path, include
# staticfiles permanece conforme configuração anterior
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),       # rota root -> core.home
    path('admin/', admin.site.urls),
    # outras rotas...
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)