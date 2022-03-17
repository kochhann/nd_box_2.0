from django.db import models
from django.urls import reverse
from datetime import date
from apps.core.models import (
    Base,
    Turma,
    Ciclo,
    Curso,
    Unidade
)
from django.utils import timezone
from django.contrib.auth.models import User


class Autorizador(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.PROTECT, blank=False, null=False)
    gv_code = models.IntegerField('GV Code', blank=False, null=False, unique=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    @property
    def name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def last_login(self):
        return self.user.last_login

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Autorizador'
        verbose_name_plural = 'Autorizadores'


class Coordenador(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.PROTECT, blank=False,
                                null=False)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.PROTECT, blank=False, null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    @property
    def name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def last_login(self):
        return self.user.last_login

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Coordenador'
        verbose_name_plural = 'Coordenadores'


class Aluno(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=100, blank=False, null=False)
    matricula = models.IntegerField("Matrícula", blank=False, null=False, unique=True)
    gv_code = models.IntegerField('GV Code', blank=False, null=False, unique=True)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.PROTECT, blank=False,
                                null=False)
    responsavel = models.ForeignKey(Autorizador, verbose_name='Autorizador', on_delete=models.PROTECT, blank=False,
                                    null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def update_enturmacao(self, gv_origin):
        same = gv_origin == self.turma_atual.gv_code
        if same:
            print('mesma turma')
        else:
            print('outra turma')

    @property
    def turma_atual(self):
        ent = self.enturmacao_set.all()
        tur = 0
        for t in ent:
            if t.turma.ano == timezone.now().year:
                tur = t.turma
        return tur

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Enturmacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.PROTECT, blank=False, null=False)
    aluno = models.ForeignKey(Aluno, verbose_name='Aluno', on_delete=models.PROTECT, blank=False, null=False)
    turma = models.ForeignKey(Turma, verbose_name='Turma', on_delete=models.PROTECT, blank=False, null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.aluno.nome + ' ' + self.turma.nome + ' - ' + self.turma.ano

    class Meta:
        verbose_name = 'Enturmação'
        verbose_name_plural = 'Enturmações'


class Evento(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=200, blank=False, null=False)
    descricao = models.CharField("Descricao", max_length=1000, blank=False, null=False)
    data_evento = models.DateField('Data', blank=False, null=False)
    aluno = models.ForeignKey(Aluno, verbose_name='Aluno', on_delete=models.SET_NULL, blank=True, null=True)
    turma = models.ForeignKey(Turma, verbose_name='Turma', on_delete=models.SET_NULL, blank=True, null=True)
    ciclo = models.ForeignKey(Ciclo, verbose_name='Ciclo', on_delete=models.SET_NULL, blank=True, null=True)
    curso = models.ForeignKey(Curso, verbose_name='Curso', on_delete=models.SET_NULL, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.SET_NULL, blank=True, null=True)

    def gera_autorizacoes(self, tipo):
        alunos = []
        model = AutorizacoesModel.objects.get(tipo=tipo)
        if self.aluno is not None:
            alunos.append(self.aluno)
        if self.turma is not None:
            ent = Enturmacao.objects.filter(turma=self.turma)
            for item in ent:
                alunos.append(item.aluno)
        if self.ciclo is not None:
            ciclo = Ciclo.objects.get(pk=self.ciclo.pk)
            for item in ciclo.turma_set.all():
                for ent in item.enturmacao_set.all():
                    alunos.append(ent.aluno)
        if self.curso is not None:
            curso = Curso.objects.get(pk=self.curso.pk)
            for ciclo in curso.ciclo_set.all():
                for turma in ciclo.turma_set.all():
                    for ent in turma.enturmacao_set.all():
                        alunos.append(ent.aluno)
        if self.unidade is not None:
            unidade = Unidade.objects.get(pk=self.unidade.pk)
            for curso in unidade.curso_set.all():
                for ciclo in curso.ciclo_set.all():
                    for turma in ciclo.turma_set.all():
                        for ent in turma.enturmacao_set.all():
                            alunos.append(ent.aluno)
        for aluno in alunos:
            aut = Autorizacao(evento=self,
                              responsavel=aluno.responsavel,
                              tipo=model,
                              aluno=aluno,
                              termos=model.texto)
            aut.save()

    def get_absolute_url(self):
        return reverse('index')

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.nome

    @property
    def scope(self):
        if self.aluno is not None:
            return self.aluno.nome
        if self.turma is not None:
            return 'Turma ' + self.turma.nome
        if self.ciclo is not None:
            return self.ciclo.nome
        if self.curso is not None:
            return self.curso.nome
        if self.unidade is not None:
            return self.unidade.nome

    @property
    def is_past_due(self):
        return date.today() > self.data_evento

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


class EventoUnidade(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    evento = models.ForeignKey(Evento, verbose_name='Evento', on_delete=models.PROTECT, blank=False, null=False)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.PROTECT, blank=False, null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.id

    @property
    def data_evento(self):
        return self.evento.data_evento


class AutorizacoesModel(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=100, blank=False, null=False)
    texto = models.TextField("Texto", blank=False, null=False)
    tipo = models.CharField("Tipo", max_length=15, unique=True, blank=False, null=False, default='imagem')

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Autorização'
        verbose_name_plural = 'Tipos de Autorização'


class Autorizacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    evento = models.ForeignKey(Evento, verbose_name='Evento', on_delete=models.PROTECT, blank=False, null=False)
    responsavel = models.ForeignKey(Autorizador, verbose_name='Responsável', on_delete=models.PROTECT, blank=False,
                                    null=False)
    tipo = models.ForeignKey(AutorizacoesModel, verbose_name='Tipo', on_delete=models.PROTECT, blank=False, null=False)
    aluno = models.ForeignKey(Aluno, verbose_name='Aluno', on_delete=models.PROTECT, blank=False, null=False)
    termos = models.TextField("Termos", blank=False, null=False)
    autorizado = models.CharField("Situação", max_length=20, blank=False, null=False, default='Pendente')

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.evento.nome + ' - ' + self.aluno.nome

    def autorizar(self):
        self.autorizado = 'Autorizado'
        self.save()

    def recusar(self):
        self.autorizado = 'Negado'
        self.save()

    class Meta:
        verbose_name = 'Autorização'
        verbose_name_plural = 'Autorizações'
