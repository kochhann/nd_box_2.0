from datetime import datetime
from .models import ScheduledTask
from apps.core.models import (
    Unidade,
    Curso,
    Ciclo,
    Turma
)
from functions import (
    get_gv_unidade,
    get_gv_curso,
    get_gv_ciclo,
    get_gv_turma
)


def read_scheduled_tasks():
    st = ScheduledTask.objects.filter(status='scheduled', ativo='1')
    for item in st:
        print(item)


def update_unidade_gv():
    unidades = Unidade.objects.all()
    gv_unidades = get_gv_unidade(0)
    list_codes_gv = []
    list_codes_local = []
    for item in gv_unidades:
        list_codes_gv.append(item.GV_CODE)
        for l_item in unidades:
            if item.GV_CODE == l_item.gv_code:
                nu = Unidade(nome=item.NOME,
                             cidade=item.CIDADE,
                             estado=item.ESTADO,
                             cnpj=item.CNPJ,
                             cnae=item.CNAE)
                if nu.cnae[0:2] == '85':
                    nu.is_school = True
                l_item.update_from_origin(nu)
    for item in unidades:
        list_codes_local.append(item.gv_code)
    new_codes = set(list_codes_gv) ^ set(list_codes_local)
    if len(new_codes) > 0:
        for code in new_codes:
            for item in gv_unidades:
                if code == item.GV_CODE:
                    nu = Unidade(nome=item.NOME.title(),
                                 cidade=item.CIDADE.title(),
                                 estado=item.ESTADO,
                                 gv_code=item.GV_CODE,
                                 cnpj=item.CNPJ,
                                 cnae=item.CNAE)
                    if item.CNAE[0:2] == '85':
                        nu.is_school = True
                    nu.save()


def update_curso_gv():
    cursos = Curso.objects.all()
    gv_cursos = get_gv_curso(0, datetime.now().year)
    print('Cursos: ' + str(len(cursos)))
    print('Cursos GV: ' + str(len(gv_cursos)))
    list_codes_gv = []
    list_codes_local = []
    for item in gv_cursos:
        list_codes_gv.append(item.GV_CODE)
        for l_item in cursos:
            if item.GV_CODE == l_item.gv_code and item.CODIGOUNIDADE == l_item.unidade.gv_code:
                unidade = Unidade.objects.get(gv_code=item.CODIGOUNIDADE)
                nc = Curso(nome=item.CURSO,
                           gv_code=item.GV_CODE,
                           unidade=unidade)
                l_item.update_from_origin(nc)
    for item in cursos:
        list_codes_local.append(item.gv_code)
    new_codes = set(list_codes_gv) ^ set(list_codes_local)
    if len(new_codes) > 0:
        for code in new_codes:
            for item in gv_cursos:
                if code == item.GV_CODE:
                    unidade = Unidade.objects.get(gv_code=item.CODIGOUNIDADE)
                    nc = Curso(nome=item.CURSO,
                               gv_code=item.GV_CODE,
                               unidade=unidade)
                    nc.save()
                    print('Curso Cadastrado')


def update_ciclo_gv():
    ciclos = Ciclo.objects.all()
    gv_ciclos = get_gv_ciclo(0, datetime.now().year)
    print('Cursos: ' + str(len(ciclos)))
    print('Cursos GV: ' + str(len(gv_ciclos)))
    list_codes_gv = []
    list_codes_local = []
    for item in gv_ciclos:
        list_codes_gv.append(item.GV_CODE)
        for l_item in ciclos:
            if item.GV_CODE == l_item.gv_code and item.CURSO == l_item.curso.gv_code:
                curso = Curso.objects.get(gv_code=item.CURSO)
                nc = Ciclo(nome=item.CICLO,
                           gv_code=item.GV_CODE,
                           curso=curso)
                l_item.update_from_origin(nc)
    for item in ciclos:
        list_codes_local.append(item.gv_code)
    new_codes = set(list_codes_gv) ^ set(list_codes_local)
    if len(new_codes) > 0:
        for code in new_codes:
            for item in gv_ciclos:
                if code == item.GV_CODE:
                    curso = Curso.objects.get(gv_code=item.CURSO)
                    nc = Ciclo(nome=item.CICLO,
                               gv_code=item.GV_CODE,
                               curso=curso)
                    nc.save()
                    print('Ciclo Cadastrado')


def update_turma_gv():
    turmas = Turma.objects.all()
    gv_turmas = get_gv_turma(0, datetime.now().year)
    print('Cursos: ' + str(len(turmas)))
    print('Cursos GV: ' + str(len(gv_turmas)))
    list_codes_gv = []
    list_codes_local = []
    for item in gv_turmas:
        list_codes_gv.append(item.GV_CODE)
        for l_item in turmas:
            if item.GV_CODE == l_item.gv_code and item.CICLO == l_item.ciclo.gv_code:
                ciclo = Ciclo.objects.get(gv_code=item.CICLO)
                nt = Turma(nome=item.TURMA,
                           ano=item.ANO,
                           gv_code=item.GV_CODE,
                           ciclo=ciclo)
                l_item.update_from_origin(nt)
    for item in turmas:
        list_codes_local.append(item.gv_code)
    new_codes = set(list_codes_gv) ^ set(list_codes_local)
    if len(new_codes) > 0:
        for code in new_codes:
            for item in gv_turmas:
                if code == item.GV_CODE:
                    ciclo = Ciclo.objects.get(gv_code=item.CICLO)
                    nt = Turma(nome=item.TURMA,
                               ano=item.ANO,
                               gv_code=item.GV_CODE,
                               ciclo=ciclo)
                    nt.save()
                    print('Turma cadastrada')
