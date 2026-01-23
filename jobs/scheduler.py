from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from notificacao import enviar_notificacao_diaria
import atexit

TIMEZONE = 'America/Sao_Paulo'

def iniciar_scheduler():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    
    # Notificação às 8h
    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=9, minute=21, timezone=TIMEZONE),
        id='notificacao_1'
    )
    
    # Notificação às 9h
    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=9, minute=22, timezone=TIMEZONE),
        id='notificacao_2'
    )
    

    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=9, minute=23, timezone=TIMEZONE),
        id='notificacao_3'
    )
    
    scheduler.start()
    # Listar jobs ativos
    jobs = scheduler.get_jobs()

    print(f"✅ Scheduler iniciado com {len(jobs)} jobs:")
    for job in jobs:
        print(f"  - {job.id}: próxima execução em {job.next_run_time}")
    
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler