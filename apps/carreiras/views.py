from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Candidatura, Vaga, Escolaridade, Unidade, Area
from .forms import CandidaturaForm


class CarreirasFormView(FormView):
    template_name = 'carreiras_aplicar.html'
    form_class = CandidaturaForm
    success_url = reverse_lazy('carreiras')

    def get_context_data(self, **kwargs):
        vagas = Vaga.objects.all()
        niveis = Escolaridade.objects.all()
        areas = Area.objects.all()
        unidades = Unidade.objects.all()
        cidades = []
        for item in unidades:
            cidades.append(item.cidade)

        cidades = list(dict.fromkeys(cidades))

        context = super(CarreirasFormView, self).get_context_data(**kwargs)
        context['doc_title'] = 'Trabalhe conosco'
        context['top_app_name'] = 'Carreiras'
        context['pt_h1'] = 'faça parte do nosso time!'
        context['pt_span'] = 'Cadastre-se e envie seu currículo'
        context['pt_breadcrumb2'] = 'Trabalhe conosco'
        context['vagas'] = vagas
        context['niveis'] = niveis
        context['areas'] = areas
        context['unidades'] = unidades
        context['cidades'] = cidades
        return context

    def form_valid(self, form, *args, **kwargs):
        apply = form.save(commit=False)
        apply.ativo = True
        apply.consentimento_1 = True
        apply.consentimento_2 = True
        apply.consentimento_3 = True
        apply.save()
        form.send_mail(apply)
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(CarreirasFormView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        print(form.errors)
        return super(CarreirasFormView, self).form_invalid(form, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CarreirasList(ListView):
    model = Candidatura

    def get_context_data(self, **kwargs):
        context = super(CarreirasList, self).get_context_data(**kwargs)
        context['doc_title'] = 'Portal de Carreiras'
        context['top_app_name'] = 'Carreiras'
        context['pt_h1'] = 'Portal de carreiras'
        context['pt_span'] = ''
        context['pt_breadcrumb2'] = 'Carreiras'
        return context

    def get_queryset(self):
        return Candidatura.objects.all()
