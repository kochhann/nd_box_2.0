from django import forms
from .models import Evento
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(EventoForm, self).clean()
        count = 0
        check = [self.cleaned_data.get('aluno'),
                 self.cleaned_data.get('turma'),
                 self.cleaned_data.get('ciclo'),
                 self.cleaned_data.get('curso'),
                 self.cleaned_data.get('unidade')]
        nome = self.cleaned_data.get('nome')
        for item in check:
            if item is None:
                count += 1

        if count == 5:
            self._errors['aluno'] = self.error_class([
                'Defina o escopo para o evento!'])

        if count < 4:
            self._errors['aluno'] = self.error_class([
                'Escolha apenas UM escopo para o evento!'])

        # return any errors if found
        return self.cleaned_data
