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
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gv_code = models.IntegerField('GV Code', blank=False, null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Aluno(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=100, blank=False, null=False)
    matricula = models.IntegerField("Matrícula", blank=False, null=False)
    gv_code = models.IntegerField('GV Code', blank=False, null=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Enturmacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    aluno = models.OneToOneField(Aluno, on_delete=models.PROTECT)
    turma = models.OneToOneField(Turma, on_delete=models.PROTECT)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.aluno.nome + ' ' + self.turma.nome + ' - ' + self.turma.ano


class Evento(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=200, blank=False, null=False)
    descricao = models.CharField("Descricao", max_length=500, blank=False, null=False)
    data_evento = models.DateField('Data', blank=False, null=False)
    aluno = models.OneToOneField(Aluno, on_delete=models.PROTECT, blank=True, null=True)
    turma = models.OneToOneField(Turma, on_delete=models.PROTECT, blank=True, null=True)
    ciclo = models.OneToOneField(Ciclo, on_delete=models.PROTECT, blank=True, null=True)
    curso = models.OneToOneField(Curso, on_delete=models.PROTECT, blank=True, null=True)
    unidade = models.OneToOneField(Unidade, on_delete=models.PROTECT, blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.nome + ' - ' + self.data_evento


class Autorizacao(Base):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    evento = models.OneToOneField(Evento, on_delete=models.PROTECT, blank=False, null=False)
    responsavel = models.OneToOneField(Autorizador, on_delete=models.PROTECT, blank=False, null=False)
    aluno = models.OneToOneField(Aluno, on_delete=models.PROTECT, blank=False, null=False)
    autorizado = models.BooleanField('Autorizado', default=False)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def __str__(self):
        return self.evento.nome + ' - ' + self.aluno.nome

