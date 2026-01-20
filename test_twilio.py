from whatsapp import processar_mensagem
import os
from dotenv import load_dotenv

# Simula uma mensagem
incoming_msg = "Olá, RaiumundA!"
sender = f"whatsapp:{os.environ['TESTE_SENDER']}"  # Seu número real

processar_mensagem(incoming_msg, sender)

