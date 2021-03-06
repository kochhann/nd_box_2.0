import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_registration_request(form):
    email_template_name = 'email/registration_request.html'
    m_context = {
        "name": form.cleaned_data['register_name'],
        "email": form.cleaned_data['register_email'],
        "r_id": form.cleaned_data['register_id'],
        "sender": 'Registro'
    }
    email = render_to_string(email_template_name, m_context)
    subject = 'Solicitação de registro no sistema ND Box'
    from_email = '"Sistema ND Box" <contato@nd.org.br>'
    to = form.cleaned_data['register_email']
    msg = EmailMultiAlternatives(subject, email, from_email, [to])
    msg.attach_alternative(email, "text/html")

    msg.send()


def send_not_user(form):
    email_template_name = 'email/user_dont_exists.html'
    m_context = {
        "name": form.cleaned_data['register_name'],
        "email": form.cleaned_data['register_email'],
        "r_id": form.cleaned_data['register_id'],
        "sender": 'Registro'
    }
    email = render_to_string(email_template_name, m_context)
    subject = 'Solicitação de registro no sistema ND Box'
    from_email = '"Sistema ND Box" <contato@nd.org.br>'
    to = form.cleaned_data['register_email']
    msg = EmailMultiAlternatives(subject, email, from_email, [to])
    msg.attach_alternative(email, "text/html")

    msg.send()


def send_not_relative(form):
    email_template_name = 'email/user_not_relative.html'
    m_context = {
        "name": form.cleaned_data['register_name'],
        "email": form.cleaned_data['register_email'],
        "r_id": form.cleaned_data['register_id'],
        "sender": 'Registro'
    }
    email = render_to_string(email_template_name, m_context)
    subject = 'Solicitação de registro no sistema ND Box'
    from_email = '"Sistema ND Box" <contato@nd.org.br>'
    to = form.cleaned_data['register_email']
    msg = EmailMultiAlternatives(subject, email, from_email, [to])
    msg.attach_alternative(email, "text/html")

    msg.send()


def send_cancel_mail(evento, responsavel):
    email_template_name = 'email/event_canceled.html'
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m_context = {
        "evento": evento.nome,
        "motivo": evento.obs_cancelamento,
        "data_evento": evento.data_evento.strftime("%d/%m/%Y"),
        "sender": 'Eventos'

    }
    email = render_to_string(email_template_name, m_context)
    subject = 'Rede Notre Dame - Aviso de cancelamento de evento'
    from_email = '"Sistema ND Box" <contato@nd.org.br>'
    to = 'apoio.ti@nd.org.br'
    # to = responsavel.email
    msg = EmailMultiAlternatives(subject, email, from_email, [to])
    msg.attach_alternative(email, "text/html")

    msg.send()


def send_test_mail():
    email_template_name = 'email/mensagem_teste.html'
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m_context = {
        "date": date
    }
    email = render_to_string(email_template_name, m_context)
    subject = 'Teste do sistema ND Box'
    from_email = '"Sistema ND Box" <contato@nd.org.br>'
    to = 'juliano@kochhann.com.br'
    msg = EmailMultiAlternatives(subject, email, from_email, [to])
    msg.attach_alternative(email, "text/html")

    msg.send()
