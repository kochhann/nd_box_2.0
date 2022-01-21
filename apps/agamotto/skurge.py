from apscheduler.schedulers.background import BackgroundScheduler
from .scheduled_task import (
    read_scheduled_tasks,
    update_unidade_gv,
    update_curso_gv,
    update_ciclo_gv,
    update_turma_gv
)


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

    scheduler.start()
