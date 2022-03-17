from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .scheduled_task import (
    read_scheduled_tasks,
    update_unidade_gv,
    update_curso_gv,
    update_ciclo_gv,
    update_turma_gv,
    update_enturmacao
)
from hermes import send_test_mail


def start():
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
    # scheduler.add_job(read_scheduled_tasks, 'interval', seconds=30)
    # scheduler.add_job(update_unidade_gv, 'interval', seconds=40)
    # scheduler.add_job(update_curso_gv, 'interval', seconds=45)
    # scheduler.add_job(update_ciclo_gv, 'interval', seconds=50)
    # scheduler.add_job(update_turma_gv, 'interval', seconds=55)
    scheduler.add_job(read_scheduled_tasks, 'interval', minutes=30)
    scheduler.add_job(update_unidade_gv, 'interval', minutes=40)
    scheduler.add_job(update_curso_gv, 'interval', minutes=45)
    scheduler.add_job(update_ciclo_gv, 'interval', minutes=50)
    scheduler.add_job(update_turma_gv, 'interval', minutes=55)
    scheduler.add_job(update_enturmacao, 'date', run_date=datetime(2022, 3, 15, 11, 00, 00))
    scheduler.add_job(send_test_mail, 'cron', hour='0', minute='2')

    scheduler.start()
