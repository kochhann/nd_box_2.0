from django.urls import path
from .views import (
    AutorizadorView,
    EventoDelete,
    EventoCreate,
    EventoUnidadeList,
    EventoEdit,
    EventoView,
    AutorizacaoList,
    AutorizacaoSuccess,
    gera_autorizacoes

)


urlpatterns = [
    path('<int:id_autorizador>/', AutorizadorView.as_view(), name='autorizador-detail'),
    path('evento/delete/<int:pk>/', EventoDelete.as_view(), name='evento-delete'),
    path('evento/create/', EventoCreate.as_view(), name='evento-create'),
    path('evento/list/', EventoUnidadeList.as_view(), name='evento-list'),
    path('evento/update/<int:pk>/', EventoEdit.as_view(), name='evento-update'),
    path('evento/<int:pk>/', EventoView.as_view(), name='evento-detail'),
    path('evento/autorizacoes/list/', AutorizacaoList.as_view(), name='autorizacao-list'),
    path('evento/autorizacoes/success/', AutorizacaoSuccess.as_view(), name='evento-autorizacoes-success'),
    path('evento/gera_autorizacoes/<int:evento_id>/<slug:tipo>', gera_autorizacoes, name='autorizacao-gerar'),
]
