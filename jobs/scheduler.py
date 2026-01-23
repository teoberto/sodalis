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
        trigger=CronTrigger(hour=1, minute=32, timezone=TIMEZONE),
        id='notificacao_8h'
    )
    
    # Notificação às 9h
    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=1, minute=35, timezone=TIMEZONE),
        id='notificacao_9h'
    )
    

    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=8, minute=0, timezone=TIMEZONE),
        id='notificacao_12h'
    )
    
    scheduler.start()
    print("✅ Scheduler iniciado - Notificações às 8h, 9h e 12h (horário de Brasília)")
    
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler