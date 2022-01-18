from django.urls import path
from .views import CarreirasFormView, CarreirasList

urlpatterns = [
    path('lista_aplicacoes', CarreirasList.as_view(), name='lista_aplicacoes'),
    path('', CarreirasFormView.as_view(), name='carreiras'),
]
