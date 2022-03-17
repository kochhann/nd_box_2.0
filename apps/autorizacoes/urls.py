from django.urls import path
from .views import (
    AutorizadorView,
    EventoDelete,
    EventoCreate,
    EventoUnidadeList,
    EventoEdit,
    EventoView,
    AutorizacaoEventoList,
    AutorizacaoSuccess,
    AutorizacaoScheduled,
    AutorizacaoView,
    AutorizacaoReleaseSuccess,
    AutorizacaoReleased,
    PrintAutReportView,
    gera_autorizacoes
)


urlpatterns = [
    path('<int:id_autorizador>/', AutorizadorView.as_view(), name='autorizador-detail'),
    path('gera_autorizacoes/<int:evento_id>/<slug:tipo>', gera_autorizacoes, name='autorizacao-gerar'),
    path('evento/delete/<int:pk>/', EventoDelete.as_view(), name='evento-delete'),
    path('evento/create/', EventoCreate.as_view(), name='evento-create'),
    path('evento/list/', EventoUnidadeList.as_view(), name='evento-list'),
    path('evento/update/<int:pk>/', EventoEdit.as_view(), name='evento-update'),
    path('evento/<int:pk>/', EventoView.as_view(), name='evento-detail'),
    path('autorizacao/list/<int:evento_id>', AutorizacaoEventoList.as_view(), name='autorizacao-list'),
    path('autorizacao/success/', AutorizacaoSuccess.as_view(), name='evento-autorizacoes-success'),
    path('autorizacao/scheduled/', AutorizacaoScheduled.as_view(), name='evento-autorizacoes-scheduled'),
    path('autorizacao/<int:pk>/', AutorizacaoView.as_view(), name='autorizacao-detail'),
    path('autorizacao/released/success/', AutorizacaoReleaseSuccess.as_view(), name='autorizacao-released-success'),
    path('autorizacao/released/', AutorizacaoReleased.as_view(), name='autorizacao-released'),
    path('autorizacao/print/<int:rpt_type>/<int:evento_id>/', PrintAutReportView.as_view(), name='autorizacao-print'),
]
