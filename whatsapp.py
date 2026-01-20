from twilio.rest import Client
import os

def processar_mensagem(incoming_msg, sender):
    """
    Recebe a mensagem, processa e envia resposta via Twilio
    """
    resposta = f"Você disse tratamento: {incoming_msg}"
    
    # Pega as credenciais do .env
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_WHATSAPP_NUMBER']
    
    # Cria cliente Twilio
    client = Client(account_sid, auth_token)
    
    # Envia a mensagem (adiciona whatsapp: no from_)
    message = client.messages.create(
        body=resposta,
        from_=f"whatsapp:{twilio_number}",
        to=sender
    )
    
    print(f"Mensagem enviada com ID: {message.sid}")
    return resposta