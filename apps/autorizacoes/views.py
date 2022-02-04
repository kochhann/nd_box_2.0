from django.contrib import messages
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DetailView
)
from .models import (
    Autorizador,
    Evento,
    EventoUnidade,
    Coordenador,
    Aluno,
    Autorizacao
)
from apps.core.models import (
    Turma,
    Ciclo,
    Curso,
    Unidade
)
from .forms import EventoForm
from apps.agamotto.models import ScheduledTask


def gera_autorizacoes(request, evento_id, tipo):
    st = ScheduledTask(task='generateAuth',
                       status='scheduled',
                       gv_code=evento_id,
                       extra_field=tipo)
    st.save()
    return redirect('evento-autorizacoes-success')


class AutorizadorView(TemplateView):
    template_name = 'autorizador_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AutorizadorView, self).get_context_data(**kwargs)
        aut = Autorizador.objects.get(user=self.request.user)
        context['doc_title'] = 'Área do Usuário'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Área do usuário'
        context['pt_span'] = 'Detalhes da sua conta'
        context['pt_breadcrumb2'] = 'Área do usuário'
        context['autorizador'] = aut
        context['dependentes'] = aut.aluno_set.all()

        return context


class EventoDelete(DeleteView):
    model = Evento
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        ev_un = EventoUnidade.objects.get(evento=self.object.pk)
        ev_un.soft_delete()
        messages.success(self.request, 'Evento excluído com sucesso!')
        return HttpResponseRedirect(self.get_success_url())


class EventoCreate(CreateView):
    model = Evento
    form_class = EventoForm

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        unidade = coord.unidade
        cursos = Curso.objects.filter(unidade=unidade)
        alunos = Aluno.objects.filter(unidade=unidade)
        ciclos = Ciclo.objects.filter(curso__in=cursos)
        turmas = Turma.objects.filter(ciclo__in=ciclos)
        unidades = Unidade.objects.filter(pk=coord.unidade.pk)
        context = super(EventoCreate, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['turmas'] = turmas
        context['ciclos'] = ciclos
        context['cursos'] = cursos
        context['alunos'] = alunos
        context['unidades'] = unidades
        return context

    def form_valid(self, form, *args, **kwargs):
        evento = form.save(commit=False)
        evento.ativo = True
        evento.save()
        coord = Coordenador.objects.get(user=self.request.user)
        ev_un = EventoUnidade(evento=evento, unidade=coord.unidade)
        ev_un.save()
        messages.success(self.request, 'Evento ' + evento.nome + ' criado com sucesso')
        return super(EventoCreate, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro no preenchimento: ' + str(form.errors))
        return super(EventoCreate, self).form_invalid(form, *args, **kwargs)


class EventoUnidadeList(ListView):
    model = EventoUnidade
    template_name = 'coordenador_evento_list.html'

    def get_queryset(self):
        coord = Coordenador.objects.get(user=self.request.user)
        ev_un = EventoUnidade.objects.filter(ativo=True, unidade=coord.unidade)
        eventos = sorted(ev_un, key=attrgetter('evento.data_evento'))
        return eventos

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(EventoUnidadeList, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        return context


class EventoEdit(UpdateView):
    model = Evento
    fields = ['nome', 'data_evento', 'descricao']
    template_name = 'autorizacoes/evento_edit_form.html'

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(EventoEdit, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        return context

    def form_valid(self, form):
        evento = form.save()
        messages.success(self.request, 'Evento ' + evento.nome + ' alterado com sucesso')
        return super(EventoEdit, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro no preenchimento: ' + str(form.errors))
        return super(EventoEdit, self).form_invalid(form, *args, **kwargs)


class EventoView(DetailView):
    # template_name = 'evento_detail.html'
    model = Evento

    def get_context_data(self, **kwargs):
        context = super(EventoView, self).get_context_data(**kwargs)
        coord = Coordenador.objects.get(user=self.request.user)
        aut = self.object.autorizacao_set.all()
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['autorizacoes'] = aut
        return context


class AutorizacaoList(ListView):
    model = Autorizacao
    # template_name = 'coordenador_evento_list.html'

    def get_queryset(self):
        coord = Coordenador.objects.get(user=self.request.user)
        eventos = []
        ev_un = EventoUnidade.objects.filter(ativo=True, unidade=coord.unidade)
        for evento in ev_un:
            eventos.append(evento.evento)
        aut = Autorizacao.objects.filter(evento__in=eventos)
        # autorizacoes = sorted(aut, key=attrgetter('evento.data_evento'))
        return aut

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(AutorizacaoList, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        return context


class AutorizacaoSuccess(TemplateView):
    template_name = 'success_auth_generation.html'

    def get_context_data(self, *args, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(AutorizacaoSuccess, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        return context

