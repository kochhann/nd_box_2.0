from django.contrib.auth.decorators import login_required
from operator import attrgetter
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    FormView
)
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm
from datetime import datetime
from apps.agamotto.models import ScheduledTask
from apps.autorizacoes.models import (
    Autorizador,
    Coordenador,
    EventoUnidade,
)
from functions import (
    get_quotes,
    get_gv_user_data,
    get_gv_user_relatives
)


class LoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Autenticação'
        context['top_app_name'] = 'Autenticação'
        context['pt_h1'] = 'Login no sistema ND Box'
        context['pt_span'] = 'Entre com e-mail e senha'
        context['pt_breadcrumb2'] = 'Autenticação'
        return context


class SuccessView(TemplateView):
    template_name = 'success_request.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Registro'
        context['top_app_name'] = 'Registro'
        context['pt_h1'] = 'registro no sistema ND'
        context['pt_span'] = 'Cadastre-se para acessar o sistema'
        context['pt_breadcrumb2'] = 'Registro'
        return context


class RegistrationFormView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):

        context = super(RegistrationFormView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Registro'
        context['top_app_name'] = 'Registro'
        context['pt_h1'] = 'registro no sistema ND'
        context['pt_span'] = 'Cadastre-se para acessar o sistema'
        context['pt_breadcrumb2'] = 'Registro'
        return context

    def form_valid(self, form, *args, **kwargs):
        gv_user_data = get_gv_user_data(form.cleaned_data.get('register_id'), 1)
        email = form.cleaned_data.get('register_email')

        if len(gv_user_data) == 0:
            form.send_not_user()
        else:
            gv_id = gv_user_data[0].CODIGOPESSOA
            user_relatives = get_gv_user_relatives(gv_id, datetime.now().year)
            if len(user_relatives) == 0:
                form.send_not_relative()
            else:
                check = ScheduledTask.objects.filter(gv_code=gv_id, task='createUser')
                if len(check) > 0:
                    for i in check:
                        if i.status == 'scheduled':
                            msg = 'Sua solicitação (id:' + str(i.id) + ') já foi recebida anteriormente. Verifique ' \
                                  'suas mensagens ou entre em contato com a sua Unidade.'
                            messages.error(self.request, msg)
                            return super(RegistrationFormView, self).form_valid(form, *args, **kwargs)
                        if i.status == 'completed':
                            msg = 'Sua solicitação (id: ' + str(i.id) + ') já foi atendida. Se você não lembra a sua ' \
                                  ' senha, volte para o login e selecione "Esqueceu a senha?"'
                            messages.error(self.request, msg)
                            return super(RegistrationFormView, self).form_valid(form, *args, **kwargs)
                else:
                    st = ScheduledTask(task='createUser',
                                       status='scheduled',
                                       gv_code=gv_id,
                                       extra_field=email)
                    st.save()
                    form.send_registration()
        messages.success(self.request, 'Sua solicitação foi recebida. Em breve entraremos em contato através do email'
                                       ' cadastrado.')
        return super(RegistrationFormView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        print(form.errors)
        return super(RegistrationFormView, self).form_invalid(form, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'link_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        day = datetime.now().day
        month = datetime.now().month
        quotes = get_quotes(day, month)
        quote = quotes[0].PENSAMENTO
        author = quotes[0].AUTORIA
        groups = self.request.user.groups.all()
        autorizador = False
        coordenador = False
        for i in groups:
            if i.name == 'Autorizadores':
                autorizador = True
            if i.name == 'Coordenação':
                coordenador = True
        if self.request.user.is_staff or self.request.user.is_anonymous:
            context['doc_title'] = 'Switch'
            context['top_app_name'] = 'Switch'
            context['pt_h1'] = 'ACESSO AOS SERVIÇOS'
            context['pt_span'] = ''
            context['pt_breadcrumb2'] = 'Acesso a portais'
            context['quote'] = quote
            context['author'] = author
        if autorizador:
            aut = Autorizador.objects.get(user=self.request.user)
            context['doc_title'] = 'Área do Usuário'
            context['top_app_name'] = 'Autorizações'
            context['pt_h1'] = 'Área do usuário'
            context['pt_span'] = 'Detalhes da sua conta'
            context['pt_breadcrumb2'] = 'Área do usuário'
            context['quote'] = quote
            context['author'] = author
            context['autorizador'] = aut
            context['dependentes'] = aut.aluno_set.all()
            context['autorizacoes'] = aut.autorizacao_set.all()
        if coordenador:
            coord = Coordenador.objects.get(user=self.request.user)
            ev_un = EventoUnidade.objects.filter(ativo=True, unidade=coord.unidade,
                                                 evento__data_cancelamento=None)
            ev_un_x = []
            for e in ev_un:
                if not e.evento.is_past_due:
                    ev_un_x.append(e)
            eventos = sorted(ev_un_x, key=attrgetter('evento.data_evento'))[:2]
            context['doc_title'] = 'Gestão de eventos'
            context['top_app_name'] = 'Autorizações'
            context['pt_h1'] = 'Gestão de eventos'
            context['pt_span'] = coord.name + ' - ' + coord.unidade.nome
            context['pt_breadcrumb2'] = 'Autorizações'
            context['quote'] = quote
            context['author'] = author
            context['coordenador'] = coord
            context['eventos'] = eventos
        context['is_autorizador'] = autorizador
        context['is_coordenador'] = coordenador
        return context


@method_decorator(login_required, name='dispatch')
class IntranetView(TemplateView):
    template_name = 'intranet_dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IntranetView, self).get_context_data(**kwargs)
        day = datetime.now().day
        month = datetime.now().month
        quotes = get_quotes(day, month)
        quote = quotes[0].PENSAMENTO
        author = quotes[0].AUTORIA
        context['doc_title'] = 'Switch'
        context['top_app_name'] = 'Switch - Intranet'
        context['pt_h1'] = 'ACESSO AOS SERVIÇOS'
        context['pt_span'] = 'Serviços da Intranet ND'
        context['pt_breadcrumb2'] = 'Intranet'
        context['quote'] = quote
        context['author'] = author
        return context
