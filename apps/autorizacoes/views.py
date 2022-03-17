from django.contrib import messages
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import date
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import (
    Table,
    TableStyle
)
from apps.reports.printing import *
from django.views.generic import (
    View,
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
    check = ScheduledTask.objects.filter(gv_code=evento_id, task='generateAuth')
    if len(check) > 0:
        for i in check:
            if i.status == 'scheduled':
                return redirect('evento-autorizacoes-scheduled')
            if i.status == 'completed':
                return redirect('evento-autorizacoes-success')
    else:
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
        return super(EventoCreate, self).form_invalid(form, *args, **kwargs)


class EventoUnidadeList(ListView):
    model = EventoUnidade
    template_name = 'coordenador_evento_list.html'

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(EventoUnidadeList, self).get_context_data(**kwargs)
        ev_un = EventoUnidade.objects.filter(ativo=True, unidade=coord.unidade)
        eventos = sorted(ev_un, key=attrgetter('evento.data_evento'))
        passados = []
        agendados = []
        for e in eventos:
            if e.evento.data_evento >= date.today():
                agendados.append(e)
            else:
                passados.append(e)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['eventos'] = eventos
        context['passados'] = passados
        context['agendados'] = agendados
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
        geradas = len(aut)
        aceitas = 0
        negadas = 0
        for a in aut:
            if a.autorizado == 'Autorizado':
                aceitas += 1
            else:
                negadas += 1
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['autorizacoes'] = geradas
        context['aceitas'] = aceitas
        context['negadas'] = negadas
        return context


class AutorizacaoEventoList(ListView):
    model = Autorizacao

    def get_queryset(self):
        evento_id = self.kwargs['evento_id']
        aut = Autorizacao.objects.filter(evento=evento_id).order_by('-evento.data_evento')
        return aut

    def get_context_data(self, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(AutorizacaoEventoList, self).get_context_data(**kwargs)
        evento_id = self.kwargs['evento_id']
        evento = Evento.objects.get(pk=evento_id)
        autorizacoes = Autorizacao.objects.filter(evento=evento_id)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['autorizacoes'] = autorizacoes
        context['evento'] = evento
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
        context['p_message'] = 'As autorizações estão em processamento! Retorne em alguns minutos.'
        context['tipo'] = 'scheduled'
        return context


class AutorizacaoScheduled(TemplateView):
    template_name = 'success_auth_generation.html'

    def get_context_data(self, *args, **kwargs):
        coord = Coordenador.objects.get(user=self.request.user)
        context = super(AutorizacaoScheduled, self).get_context_data(**kwargs)
        context['doc_title'] = 'Gestão de eventos'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos'
        context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
        context['pt_breadcrumb2'] = 'Autorizações'
        context['p_message'] = 'As autorizações deste evento já estão sendo processadas! Retorne em alguns minutos.'
        context['tipo'] = 'scheduled'
        return context


class AutorizacaoView(DetailView):
    # template_name = 'evento_detail.html'
    model = Autorizacao

    def get_context_data(self, **kwargs):
        context = super(AutorizacaoView, self).get_context_data(**kwargs)
        groups = self.request.user.groups.all()
        autorizador = False
        coordenador = False
        a_id = self.object.pk
        aut = Autorizacao.objects.get(pk=a_id)
        for i in groups:
            if i.name == 'Autorizadores':
                autorizador = True
            if i.name == 'Coordenação':
                coordenador = True
        context['doc_title'] = 'Gestão de eventos' if coordenador else 'Área do usuário'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Gestão de eventos' if coordenador else 'Área do usuário'
        context['pt_breadcrumb2'] = 'Autorizações'
        context['pt_span'] = 'Detalhes de autorizações' if autorizador else ''
        context['is_autorizador'] = autorizador
        context['is_coordenador'] = coordenador
        context['status'] = 'Pendente'
        if aut.autorizado == 'Autorizado':
            context['status'] = 'Autorizado'
            messages.success(self.request, 'Esta atividade foi AUTORIZADA em ' +
                             aut.data_modificacao.strftime('%d/%m/%Y'))
        if aut.autorizado == 'Negado':
            context['status'] = 'Negado'
            messages.error(self.request, 'Esta atividade foi NEGADA em ' + aut.data_modificacao.strftime('%d/%m/%Y'))
        return context


class AutorizacaoReleased(View):
    template_name = 'autorizacao_detail.html'

    def post(self, request, *args, **kwargs):
        aut = Autorizacao.objects.get(pk=self.request.POST.get('autorizacao', None))
        check = self.request.POST.get('inlineRadioOptions', None)
        if check == 'y':
            aut.autorizar()
        else:
            aut.recusar()
        return redirect('autorizacao-released-success')


class AutorizacaoReleaseSuccess(TemplateView):
    template_name = 'success_auth_generation.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AutorizacaoReleaseSuccess, self).get_context_data(**kwargs)
        context['doc_title'] = 'Área do usuário'
        context['top_app_name'] = 'Autorizações'
        context['pt_h1'] = 'Área do usuário'
        context['pt_span'] = 'Detalhes de autorizações'
        context['pt_breadcrumb2'] = 'Autorizações'
        context['p_message'] = 'Obrigado! Recebemos sua resposta.'
        context['is_autorizador'] = True
        context['tipo'] = 'aut'
        return context


class PrintAutReportView(View):
    def get(self, request, *args, **kwargs):
        report_type = self.kwargs['rpt_type']
        evento_id = self.kwargs['evento_id']
        evento = Evento.objects.get(pk=evento_id)
        autorizacoes = evento.autorizacao_set.all()
        if report_type == 0:
            autorizacoes = Autorizacao.objects.filter(evento=evento, autorizado='Autorizado')
            report_type = 'Concedidas'
        if report_type == 1:
            autorizacoes = Autorizacao.objects.filter(evento=evento, autorizado='Negado')
            report_type = 'Negadas'
        if report_type == 2:
            autorizacoes = Autorizacao.objects.filter(evento=evento, autorizado='Pendente')
            report_type = 'Pendentes'
        if report_type == 3:
            report_type = 'Todos'

        response = HttpResponse(content_type='application/pdf')
        doc = SimpleDocTemplate(response, topMargin=2 * cm, rightMargin=2.5 * cm, leftMargin=2.5 * cm,
                                bottomMargin=2 * cm)

        # Style
        h1 = PS(
            name='Heading1',
            fontName='Times-Bold',
            alignment=TA_LEFT,
            fontSize=14,
            leading=14)

        h2 = PS(
            name='Heading2',
            fontName='Times-Bold',
            alignment=TA_CENTER,
            fontSize=14,
            leading=14)

        c1 = PS(
            name='Cell1',
            fontName='Times-Roman',
            alignment=TA_JUSTIFY,
            fontSize=12,
            leading=14)

        c2 = PS(
            name='Cell2',
            fontName='Times-Roman',
            alignment=TA_LEFT,
            fontSize=12,
            leading=14)

        n_session = 1

        # Body
        elements = [Paragraph(evento.nome, h2),
                    Spacer(1, 0.25 * cm),
                    Paragraph('Data: ' + evento.data_evento.strftime("%d/%m/%Y"), c1),
                    Spacer(1, 0.25 * cm),
                    Paragraph('Escopo: ' + evento.scope, c1),
                    Spacer(1, 0.25 * cm),
                    Paragraph(report_type, h2),
                    Spacer(1, 0.25 * cm)]

        if autorizacoes:
            for a in autorizacoes:
                day = a.data_modificacao.strftime("%d")
                month = a.data_modificacao.strftime("%m")
                year = a.data_modificacao.strftime("%Y")
                data = [[Paragraph(a.aluno.nome.title(), c2),
                         '-',
                         Paragraph(a.autorizado + ' em ' + a.data_modificacao.strftime("%d/%m/%Y"), c1)]]
                t = Table(data, colWidths=[220.0, 15.0, 220.0])
                t.setStyle(TableStyle([('ALIGN', (0, 0), (1, 0), 'LEFT'),
                                       ('ALIGN', (1, 0), (3, 0), 'CENTRE'),
                                       ('VALIGN', (0, 0), (3, 0), 'TOP'),
                                       ]))
                elements.append(t)
                elements.append(Spacer(1, 0.25 * cm))
        else:
            elements = [Paragraph('Não há autorizações ' + report_type, h2),
                        Spacer(1, 0.25 * cm)]
        ###

        buffer = BytesIO()
        doc.title = evento.nome + ' - Lista de ' + report_type

        report = MyPrint(buffer, 'A4')

        # response.write(doc.build(elements))
        response.write(doc.build(elements, canvasmaker=NumberedCanvas))

        return response
