from llm import generate_response
from sqlalchemy import create_engine, text
from whatsapp import enviar_whatsapp
from dotenv import load_dotenv
import os
import time

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

def enviar_notificacao_diaria():

    tarefas = consultar_tarefas_diarias()    
    usuarios_tarefas = agrupar_tarefas_por_usuario(tarefas)

    # Gera reflexão UMA VEZ para todos os usuários
    motivacional = generate_response(
        "Gere uma reflexão diária cristã católica", 
        system_prompt="Apenas uma frase. Cite exclusivamente: santos, padres, doutores da igreja, bíblia ou papa. Cite a fonte."
    )
        
    # Enviar uma mensagem por usuário
    for nr_whatsapp, dados in usuarios_tarefas.items():
        nome = dados['nome']
        tarefas = dados['tarefas']
        
        mensagem = f"🏠 Bom dia!\n\n📋 Lembrete das tarefas diárias:\n\n"
        mensagem += "\n".join([f"• {tarefa}" for tarefa in tarefas])
        mensagem += f"\n\n_Reflexão do dia_: {motivacional}"
        
        enviar_whatsapp(f"whatsapp:{nr_whatsapp}", mensagem)
        print(f"✅ Enviado para {nr_whatsapp} ({nome}):\n")
        time.sleep(1)  # Pausa de 1 segundo entre mensagens


def consultar_tarefas_diarias():
    with engine.connect() as connection:
        resultado = connection.execute(text(   
            """SELECT usuario.nr_whatsapp, usuario.nome, tarefa.nm_tarefa
                FROM atribuicao
                LEFT JOIN tarefa ON tarefa.id_tarefa = atribuicao.id_tarefa
                LEFT JOIN usuario ON usuario.id_usuario = atribuicao.id_usuario"""))            
        return resultado.mappings().all()
    
def agrupar_tarefas_por_usuario(list_dict:list) -> dict:
   
    # Agrupar tarefas por usuário
    usuarios_tarefas = {}
    
    for row in list_dict:
        nr_whatsapp = row['nr_whatsapp']
        nm_tarefa = row['nm_tarefa']
        nome = row['nome']
        
        if nr_whatsapp not in usuarios_tarefas:
            usuarios_tarefas[nr_whatsapp] = {
                'nome': nome,
                'tarefas': []
            }
        
        usuarios_tarefas[nr_whatsapp]['tarefas'].append(nm_tarefa)    

    return usuarios_tarefas

if __name__ == "__main__":
    enviar_notificacao_diaria()