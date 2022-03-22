from django.contrib.auth.models import (
    User,
    Group
)
from django.db import connection
from collections import namedtuple
from apps.autorizacoes.models import (
    Autorizador,
    Aluno,
    Enturmacao,
    Evento
)
from apps.core.models import (
    Unidade,
    Turma
)
from apps.agamotto.models import ScheduledTask
import uuid
from datetime import datetime


def get_quotes(day, month):
    cursor = connection.cursor()
    cursor.execute("SELECT PENSAMENTO, AUTORIA FROM NDSISTEMAS.DBO.PENSAMENTOS"
                   " WHERE DAY(data) = '%s' AND MONTH(data) = '%s'" % (day, month))
    quotes = namedtuplefetchall(cursor)
    return quotes


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


def nl2br(s):
    return '<br />\n'.join(s.split('\n'))


def get_gv_unidade(gv_code):
    cursor = connection.cursor()
    if gv_code == 0:
        cursor.execute("SELECT P.NOMEREDUZIDO AS NOME,"
                       "       C.NOME AS CIDADE,"
                       "       UF.SIGLA AS ESTADO,"
                       "       P.CODIGOPESSOA AS GV_CODE,"
                       "       COALESCE(U.CNAE, '00000000') AS CNAE,"
                       "       PJ.CNPJ AS CNPJ"
                       " FROM GVContabilidade.dbo.PAD_UNIDADE U"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA P"
                       "        ON U.CODIGOPESSOA = P.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAENDERECO E"
                       "        ON P.CODIGOPESSOA = E.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.PAD_CIDADE C"
                       "        ON E.CODIGOCIDADE = C.CODIGOCIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADEFEDERACAO UF"
                       "        ON C.CODIGOUF = UF.CODIGOUF"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAJURIDICA PJ"
                       "        ON P.CODIGOPESSOA = PJ.CODIGOPESSOA")
    else:
        cursor.execute("SELECT P.NOMEREDUZIDO AS NOME,"
                       "       C.NOME AS CIDADE,"
                       "       UF.SIGLA AS ESTADO,"
                       "       P.CODIGOPESSOA AS GV_CODE,"
                       "       COALESCE(U.CNAE, '00000000') AS CNAE,"
                       "       PJ.CNPJ AS CNPJ"
                       " FROM GVContabilidade.dbo.PAD_UNIDADE U"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA P"
                       "        ON U.CODIGOPESSOA = P.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAENDERECO E"
                       "        ON P.CODIGOPESSOA = E.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.PAD_CIDADE C"
                       "        ON E.CODIGOCIDADE = C.CODIGOCIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADEFEDERACAO UF"
                       "        ON C.CODIGOUF = UF.CODIGOUF"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAJURIDICA PJ"
                       "        ON P.CODIGOPESSOA = PJ.CODIGOPESSOA"
                       " WHERE P.CODIGOPESSOA = '%s'" % gv_code)

    qs = namedtuplefetchall(cursor)
    return qs


def get_gv_user_data(user_id, option):
    cursor = connection.cursor()
    if option == 1:
        cursor.execute("SELECT P.CODIGOPESSOA"
                       " ,P.NOME"
                       " FROM GVContabilidade.dbo.PAD_PESSOA P"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAFISICA PF"
                       "        ON PF.CODIGOPESSOA = P.CODIGOPESSOA"
                       " WHERE CPF = '%s'" % user_id)
    if option == 2:
        cursor.execute("SELECT P.CODIGOPESSOA"
                       " ,P.NOME"
                       " FROM GVContabilidade.dbo.PAD_PESSOA P"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAFISICA PF"
                       "        ON PF.CODIGOPESSOA = P.CODIGOPESSOA"
                       " WHERE P.CODIGOPESSOA = '%s'" % user_id)
    qs = namedtuplefetchall(cursor)
    return qs


def get_gv_user_relatives(gv_code, year):
    cursor = connection.cursor()
    cursor.execute("SELECT P.NOME,"
                   "       PA.DESCRICAO,"
                   "       PA.CODIGOPAPEL,"
                   "       P_ALUNO.CODIGOPESSOA,"
                   "       P_ALUNO.NOME ALUNO"
                   " FROM GVContabilidade.dbo.PAD_PESSOA P"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAPAPEL PP"
                   "        ON P.CODIGOPESSOA = PP.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PAPEL PA"
                   "        ON PP.CODIGOPAPEL = PA.CODIGOPAPEL"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA P_ALUNO"
                   "        ON PP.CODIGOPESSOAVINCULO = P_ALUNO.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.ACD_ALUNO ALU"
                   "        ON P_ALUNO.CODIGOPESSOA = ALU.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                   "        ON ALU.CODIGOALUNO = ENT.CODIGOALUNO"
                   "    INNER JOIN GVContabilidade.dbo.ACD_TURMA TUR"
                   "        ON ENT.CODIGOTURMA = TUR.CODIGOTURMA"
                   " WHERE P.CODIGOPESSOA = '%s'"
                   "      AND PA.CODIGOPAPEL = 30"
                   "      AND TUR.ANOINICIO = '%s'" % (gv_code, year))
    qs = namedtuplefetchall(cursor)
    return qs


def get_enturmacao(gv_code, year):
    cursor = connection.cursor()
    if gv_code > 0:
        cursor.execute("SELECT ALUP.NOME ALUNO,"
                       "       ALU.MATRICULA"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ALUNO ALU"
                       "        ON ENT.CODIGOALUNO = ALU.CODIGOALUNO"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA ALUP"
                       "        ON ALU.CODIGOPESSOA = ALUP.CODIGOPESSOA"
                       " WHERE ALUP.CODIGOPESSOA = '%s'"
                       "      AND TUR.ANOINICIO = '%s'"
                       " GROUP BY ALUP.NOME,"
                       "         ALU.MATRICULA" % (gv_code, year))
    qs = namedtuplefetchall(cursor)
    return qs


def get_gv_curso(gv_code, year):
    cursor = connection.cursor()
    if gv_code == 0:
        cursor.execute("SELECT PESUNI.CODIGOPESSOA CODIGOUNIDADE,"
                       "       PESUNI.NOMEREDUZIDO UNIDADE,"
                       "       CUR.DESCRICAO CURSO,"
                       "	   CUR.CODIGOCURSO GV_CODE"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE TUR.ANOINICIO = '%s'"
                       " GROUP BY PESUNI.CODIGOPESSOA,"
                       "         PESUNI.NOMEREDUZIDO,"
                       "         CUR.DESCRICAO,"
                       "	     CUR.CODIGOCURSO" % year)
    else:
        cursor.execute("SELECT PESUNI.CODIGOPESSOA CODIGOUNIDADE,"
                       "       PESUNI.NOMEREDUZIDO UNIDADE,"
                       "       CUR.DESCRICAO CURSO,"
                       "	   CUR.CODIGOCURSO GV_CODE"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE CUR.CODIGOCURSO = '%s'"
                       " GROUP BY PESUNI.CODIGOPESSOA,"
                       "         PESUNI.NOMEREDUZIDO,"
                       "         CUR.DESCRICAO,"
                       "	     CUR.CODIGOCURSO" % gv_code)
    qs = namedtuplefetchall(cursor)
    return qs


def get_gv_ciclo(gv_code, year):
    cursor = connection.cursor()
    if gv_code == 0:
        cursor.execute("SELECT CUR.CODIGOCURSO CURSO,"
                       "       CIC.DESCRICAO CICLO,"
                       "       CIC.CODIGOCICLO GV_CODE"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE TUR.ANOINICIO = '%s'"
                       " GROUP BY CUR.CODIGOCURSO,"
                       "       CIC.DESCRICAO,"
                       "       CIC.CODIGOCICLO" % year)
    else:
        cursor.execute("SELECT CUR.CODIGOCURSO CURSO,"
                       "       CIC.DESCRICAO CICLO,"
                       "       CIC.CODIGOCICLO GV_CODE"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE CIC.CODIGOCICLO = '%s'"
                       " GROUP BY CUR.CODIGOCURSO,"
                       "       CIC.DESCRICAO,"
                       "       CIC.CODIGOCICLO" % gv_code)
    qs = namedtuplefetchall(cursor)
    return qs


def get_gv_turma(gv_code, year):
    cursor = connection.cursor()
    if gv_code == 0:
        cursor.execute("SELECT CIC.CODIGOCICLO CICLO,"
                       "       TUR.CODIGOTURMA,"
                       "       TUR.DESCRICAO TURMA,"
                       "	   TUR.CODIGOTURMA GV_CODE,"
                       "       TUR.ANOINICIO ANO"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE TUR.ANOINICIO = '%s'"
                       " GROUP BY CIC.CODIGOCICLO,"
                       "       TUR.CODIGOTURMA,"
                       "       TUR.DESCRICAO,"
                       "	   TUR.CODIGOTURMA,"
                       "       TUR.ANOINICIO" % year)
    else:
        cursor.execute("SELECT CIC.CODIGOCICLO CICLO,"
                       "       TUR.CODIGOTURMA,"
                       "       TUR.DESCRICAO TURMA,"
                       "	   TUR.CODIGOTURMA GV_CODE"
                       " FROM GVContabilidade.dbo.ACD_TURMA TUR"
                       "    INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                       "        ON TUR.CODIGOEMPRESA = UNI.CODIGOEMPRESA"
                       "           AND TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                       "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA PESUNI"
                       "        ON UNI.CODIGOPESSOA = PESUNI.CODIGOPESSOA"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CICLO CIC"
                       "        ON TUR.CODIGOCICLO = CIC.CODIGOCICLO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_CURSO CUR"
                       "        ON CIC.CODIGOCURSO = CUR.CODIGOCURSO"
                       "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                       "        ON TUR.CODIGOTURMA = ENT.CODIGOTURMA"
                       " WHERE TUR.CODIGOTURMA = '%s'"
                       " GROUP BY CIC.CODIGOCICLO,"
                       "       TUR.CODIGOTURMA,"
                       "       TUR.DESCRICAO,"
                       "	   TUR.CODIGOTURMA" % gv_code)
    qs = namedtuplefetchall(cursor)
    return qs


def get_relatives(gv_code, year):
    cursor = connection.cursor()
    cursor.execute("SELECT P_ALUNO.NOME ALUNO,"
                   "       P_ALUNO.CODIGOPESSOA GV_CODE,"
                   "	   P_UNI.CODIGOPESSOA UNIDADE,"
                   "	   ALU.MATRICULA,"
                   "	   P.CODIGOPESSOA RESPONSAVEL,"
                   "       PA.DESCRICAO,"
                   "       PA.CODIGOPAPEL"
                   " FROM GVContabilidade.dbo.PAD_PESSOA P"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PESSOAPAPEL PP"
                   "        ON P.CODIGOPESSOA = PP.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PAPEL PA"
                   "        ON PP.CODIGOPAPEL = PA.CODIGOPAPEL"
                   "    INNER JOIN GVContabilidade.dbo.PAD_PESSOA P_ALUNO"
                   "        ON PP.CODIGOPESSOAVINCULO = P_ALUNO.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.ACD_ALUNO ALU"
                   "        ON P_ALUNO.CODIGOPESSOA = ALU.CODIGOPESSOA"
                   "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                   "        ON ALU.CODIGOALUNO = ENT.CODIGOALUNO"
                   "    INNER JOIN GVContabilidade.dbo.ACD_TURMA TUR"
                   "        ON ENT.CODIGOTURMA = TUR.CODIGOTURMA"
                   "	INNER JOIN GVContabilidade.dbo.PAD_UNIDADE UNI"
                   "		ON TUR.CODIGOUNIDADE = UNI.CODIGOUNIDADE"
                   "	INNER JOIN GVContabilidade.dbo.PAD_PESSOA P_UNI"
                   "		ON UNI.CODIGOPESSOA = P_UNI.CODIGOPESSOA"
                   " WHERE P.CODIGOPESSOA = '%s'"
                   "      AND PA.CODIGOPAPEL = 30"
                   "      AND TUR.ANOINICIO = '%s'" % (gv_code, year))
    qs = namedtuplefetchall(cursor)
    qs = list(dict.fromkeys(qs))
    return qs


def create_aluno(rel):
    responsavel = Autorizador.objects.get(gv_code=rel.RESPONSAVEL)
    unidade = Unidade.objects.get(gv_code=rel.UNIDADE)
    aluno = Aluno(nome=rel.ALUNO.title(),
                  matricula=int(rel.MATRICULA),
                  gv_code=rel.GV_CODE,
                  unidade=unidade,
                  responsavel=responsavel)
    aluno.save()
    return aluno


def get_turma_aluno(matricula, year):
    cursor = connection.cursor()
    cursor.execute("SELECT TUR.CODIGOTURMA"
                   " FROM GVContabilidade.dbo.ACD_ALUNO ALU"
                   "    INNER JOIN GVContabilidade.dbo.ACD_ENTURMACAO ENT"
                   "        ON ALU.CODIGOALUNO = ENT.CODIGOALUNO"
                   "    INNER JOIN GVContabilidade.dbo.ACD_TURMA TUR"
                   "        ON ENT.CODIGOTURMA = TUR.CODIGOTURMA"
                   " WHERE ALU.MATRICULA = '%s'"
                   "      AND TUR.ANOINICIO = '%s'" % (matricula, year))
    qs = namedtuplefetchall(cursor)
    codigo = 0
    if len(qs) > 0:
        codigo = qs[0].CODIGOTURMA
    return codigo


def create_enturmacao(aluno, turma):
    enturmacao = Enturmacao(unidade=aluno.unidade,
                            aluno=aluno,
                            turma=turma)
    enturmacao.save()
    return enturmacao.id


def user_creation_autorizador(id_number):
    task = ScheduledTask.objects.get(id=id_number)
    gv_user = get_gv_user_data(task.gv_code, 2)
    full = gv_user[0].NOME.title()
    nome, *sobrenome = full.split()
    sobrenome = " ".join(sobrenome)
    email = task.extra_field
    gv_code = gv_user[0].CODIGOPESSOA

    # create user in auth system
    user = User.objects.create_user(email, email, sobrenome)
    user.first_name = nome
    user.last_name = sobrenome
    user.save()

    # add in Autorizadores group
    g = Group.objects.get(name='Autorizadores')
    g.user_set.add(user)

    # create Autorizador and references user
    autorizador = Autorizador(user=user,
                              gv_code=gv_code)
    autorizador.save()

    # get relatives
    rel = get_relatives(gv_code, datetime.now().year)
    alunos = []
    for aluno in rel:
        new_aluno = create_aluno(aluno)
        alunos.append(new_aluno)

    # make grouping
    for item in alunos:
        turma = Turma.objects.get(gv_code=get_turma_aluno(item.matricula, datetime.now().year))
        item.create_enturmacao(turma)

    task.status = 'completed'
    task.soft_delete()


def generate_authorization(id_evento, tipo):
    evento = Evento.objects.get(pk=id_evento)
    evento.gera_autorizacoes(tipo)
    print('autorizações geradas')
