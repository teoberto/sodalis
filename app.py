import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# app
app = Flask(__name__)

# database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.route("/")
def hello_database():

    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM teste"))
        row = result.fetchone()
        name = row.name

    return render_template("index.html", name=name)