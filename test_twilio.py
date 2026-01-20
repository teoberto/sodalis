from whatsapp import processar_mensagem
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simula uma mensagem
incoming_msg = "Olá! Só de boa?"
sender = f"whatsapp:{os.environ['TESTE_SENDER']}"  # Seu número real

processar_mensagem(incoming_msg, sender)

