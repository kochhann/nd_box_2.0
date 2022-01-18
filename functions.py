from django.db import connection
from collections import namedtuple
from apps.autorizacoes.models import (
    Autorizador
)
import uuid


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


def get_base_educacional_gv(year):
    cursor = connection.cursor()
    cursor.execute("SELECT UNI.CODIGOUNIDADE,"
                   "       PESUNI.NOMEREDUZIDO UNIDADE,"
                   "       CUR.DESCRICAO CURSO,"
                   "       CIC.DESCRICAO CICLO,"
                   "       TUR.CODIGOTURMA,"
                   "       TUR.DESCRICAO TURMA"
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
                   " GROUP BY UNI.CODIGOUNIDADE,"
                   "         PESUNI.NOMEREDUZIDO,"
                   "         CUR.DESCRICAO,"
                   "         CIC.DESCRICAO,"
                   "         TUR.CODIGOTURMA,"
                   "         TUR.DESCRICAO" % year)
    qs = namedtuplefetchall(cursor)
    return qs


def user_creation(id_number):
    gv_user = get_gv_user_data(id_number, 2)
    # user = User.objects.create(
    #     username=usuario.email,
    #     first_name=usuario.nome,
    #     last_name=usuario.sobrenome)
    # user.set_password(usuario.sobrenome)
    # user.save()
    # autorizador = Autorizador()
    # autorizador.save()
    print(gv_user)
