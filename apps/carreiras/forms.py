from django import forms
from .models import (
    Candidatura,
    Vaga,
)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = '__all__'

    def send_mail(self, apply):
        codigo = ''
        vaga = 'candidatura espontânea'
        if apply.cod_vaga != '' and apply.cod_vaga is not None:
            codigo = 'VAGA - ' + apply.cod_vaga.cod_vaga + ' '
            vaga = 'vaga ' + apply.cod_vaga.cod_vaga
        email_template_name = 'email/send_application.html'
        m_context = {
            "vaga": vaga,
            "name": apply.nome,
            "email": apply.email,
            "area": apply.area_interesse,
            "phone": apply.telefone,
            "sender": 'Candidatura'
        }
        email = render_to_string(email_template_name, m_context)
        subject = codigo + 'Candidatura através do portal ND Box'
        from_email = '"Sistema ND Box | Carreiras" <contato@nd.org.br>'
        to = 'apoio.ti@nd.org.br'
        msg = EmailMultiAlternatives(subject, email, from_email, [to])
        msg.attach_alternative(email, "text/html")
        msg.attach_file(apply.arquivo.path)
        msg.send()


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo',
                  'unidade',
                  'cod_vaga',
                  'area_interesse',
                  'descricao',
                  'escolaridade',
                  'tempo_experiencia'
                  ]


class VagaEditForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo',
                  'descricao',
                  'tempo_experiencia'
                  ]


class VagaSearchForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['cod_vaga',
                  'unidade',
                  'area_interesse',
                  'escolaridade',
                  'aberta',
                  'preenchida'
                  ]
