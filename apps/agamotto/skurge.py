from apscheduler.schedulers.background import BackgroundScheduler
from .scheduled_task import (
    read_scheduled_tasks,
    update_unidade_gv,
    # update_base_educacional_gv
)


def start():
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
    scheduler.add_job(read_scheduled_tasks, 'interval', minutes=30)
    scheduler.add_job(update_unidade_gv, 'interval', minutes=60)
    # scheduler.add_job(update_base_educacional_gv, 'interval', minutes=65)

    scheduler.start()
