from llm import generate_response
from twilio.rest import Client
import os

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_WHATSAPP_NUMBER']

def enviar_whatsapp(to: str, body:str):

    # Cria cliente Twilio
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    # Envia a mensagem (adiciona whatsapp: no from_)
    message = client.messages.create(
        body=body,
        from_=f"whatsapp:{TWILIO_NUMBER}",
        to=to
    )
    
    print(f"Mensagem enviada com ID: {message.sid}")


   

def processar_mensagem(incoming_msg, sender):
    """
    Recebe a mensagem, processa e envia resposta via Twilio
    """
    
    resposta = generate_response(incoming_msg, "Responda com no máximo 1500 caracteres. Você faz parte da minha equipe que está desenvolvendo o Sodalis, um Assistente Pessoal Familiar. O MPV 1 enviará notificações períodicas de tarefas")
    
    # Cria cliente Twilio
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    # Envia a mensagem (adiciona whatsapp: no from_)
    message = client.messages.create(
        body=resposta,
        from_=f"whatsapp:{TWILIO_NUMBER}",
        to=sender
    )
    
    print(f"Mensagem enviada com ID: {message.sid}")
    return resposta

# if __name__ == "__main__":
#     Teste de envio
#     enviar_whatsapp("whatsapp:+556181956970", "Olá! Esta é uma mensagem de teste do Sodalis.")