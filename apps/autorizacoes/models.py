from django.db import models
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
    gv_code = models.IntegerField('GV Code', blank=False, null=False)

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
        return self.user.last_login.date()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Autorizador'
        verbose_name_plural = 'Autorizadores'


class Aluno(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=100, blank=False, null=False)
    matricula = models.IntegerField("Matrícula", blank=False, null=False)
    gv_code = models.IntegerField('GV Code', blank=False, null=False)
    responsavel = models.ForeignKey(Autorizador, verbose_name='Autorizador', on_delete=models.PROTECT, blank=False,
                                    null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Enturmacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
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
    descricao = models.CharField("Descricao", max_length=500, blank=False, null=False)
    data_evento = models.DateField('Data', blank=False, null=False)
    aluno = models.ForeignKey(Aluno, verbose_name='Aluno', on_delete=models.SET_NULL, blank=True, null=True)
    turma = models.ForeignKey(Turma, verbose_name='Turma', on_delete=models.SET_NULL, blank=True, null=True)
    ciclo = models.ForeignKey(Ciclo, verbose_name='Ciclo', on_delete=models.SET_NULL, blank=True, null=True)
    curso = models.ForeignKey(Curso, verbose_name='Curso', on_delete=models.SET_NULL, blank=True, null=True)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', on_delete=models.SET_NULL, blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.nome + ' - ' + self.data_evento

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


class Autorizacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    evento = models.ForeignKey(Evento, verbose_name='Evento', on_delete=models.PROTECT, blank=False, null=False)
    responsavel = models.ForeignKey(Autorizador, verbose_name='Responsável', on_delete=models.PROTECT, blank=False, null=False)
    aluno = models.ForeignKey(Aluno, verbose_name='Aluno', on_delete=models.PROTECT, blank=False, null=False)
    autorizado = models.BooleanField('Autorizado', default=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.evento.nome + ' - ' + self.aluno.nome

    class Meta:
        verbose_name = 'Autorização'
        verbose_name_plural = 'Autorizações'

