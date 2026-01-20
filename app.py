import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import create_engine, text
from whatsapp import processar_mensagem

# Load environment variables
load_dotenv()

# app
app = Flask(__name__)

# database setup
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

@app.route("/")
def hello_database():

    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM teste"))
        row = result.fetchone()
        name = row.name

    return render_template("index.html", name=name)


@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    
    processar_mensagem(incoming_msg, sender)
        
    return "OK", 200