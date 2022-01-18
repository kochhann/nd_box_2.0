from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.core.urls')),
    path('manager/', admin.site.urls),
    path('carreiras/', include('apps.carreiras.urls')),
    path('reports/', include('apps.reports.urls')),
    path('privacidade/', include('apps.privacidade.urls')),
    path('autorizacoes/', include('apps.autorizacoes.urls'))
]

admin.site.site_header = 'Gestão ND Box'
admin.site.site_title = 'Gestão ND Box'
admin.site.index_title = 'Área Administrativa'