from django.contrib import admin
from apps.core.models import (
    Unidade,
    Curso,
    Ciclo,
    Turma
)


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'cnpj', 'is_school', 'ativo']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'unidade', 'gv_code', 'ativo']


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'curso', 'gv_code', 'ativo']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['ciclo', 'nome', 'ano', 'ativo']

