from django.contrib import admin
from .models import Area, Unidade, Vaga, Candidatura, Escolaridade


@admin.register(Escolaridade)
class EscolaridadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_criacao', 'ativo']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_criacao', 'ativo']


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'cnpj', 'is_school', 'ativo']


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ['cod_vaga', 'unidade', 'descricao',  'preenchida', 'data_criacao', 'ativo']


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'data_criacao', 'ativo']
