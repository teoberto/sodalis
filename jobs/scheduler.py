from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from notificacao import enviar_notificacao_diaria
import atexit

TIMEZONE = 'America/Sao_Paulo'

def iniciar_scheduler():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    
    # Notificação às 7h
    scheduler.add_job(
        func=enviar_notificacao_diaria,
        trigger=CronTrigger(hour=7, minute=00, timezone=TIMEZONE),
        id='notificacao_diaria_padrao'
    )
    
    # # Executar a cada 1 minuto (para testes)
    # scheduler.add_job(
    #     func=enviar_notificacao_diaria,
    #     trigger="interval",
    #     minutes=1,
    #     id='lembretes_tarefas'
    # )    

    scheduler.start()
    # Listar jobs ativos
    jobs = scheduler.get_jobs()

    print(f"✅ Scheduler iniciado com {len(jobs)} jobs:")
    for job in jobs:
        print(f"  - {job.id}: próxima execução em {job.next_run_time}")
    
    atexit.register(lambda: scheduler.shutdown())
    

    return scheduler
