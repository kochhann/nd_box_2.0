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
    get_base_educacional_gv
)


def read_scheduled_tasks():
    st = ScheduledTask.objects.filter(status='scheduled', ativo='1')
    for item in st:
        print(item)


def update_unidade_gv():
    unidades = Unidade.objects.all()
    gv_unidades = get_gv_unidade(0)
    print('Unidades: ' + str(len(unidades)))
    print('Unidades GV: ' + str(len(gv_unidades)))
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
                    print('Unidade Cadastrada')


# def update_base_educacional_gv():
#     unidades = Unidade.objects.all()
#     cursos = Curso.objects.all()
#     ciclos = Ciclo.objects.all()
#     turmas = Turma.objects.all()
#     gv_base_educacional = get_base_educacional_gv(datetime.now().year)
#     print(str(len(gv_base_educacional)))
#     for bu in gv_base_educacional:
#         continue
#     pass
