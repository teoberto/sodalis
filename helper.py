from dotenv import load_dotenv
from flask import redirect, render_template, session
from functools import wraps
from sqlalchemy import create_engine, text
import os
import re

# Load environment variables
load_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]


class ConectaBancoDados:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def executar_query(self, query, parametros=None):
        with self.engine.connect() as connection:
            resultado = connection.execute(text(query), parametros or {})
            return resultado.mappings().all()



def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def validar_email(email):
    """
    Valida formato de e-mail usando regex.
    Retorna True se válido, False caso contrário.
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


def validar_telefone_e164(telefone):
    """
    Valida formato E.164: +[código país][número]
    Exemplo: +5561981234567
    """
    padrao = r'^\+[1-9]\d{1,14}$'
    return re.match(padrao, telefone) is not None


def formatar_telefone_whatsapp(nr_telefone):
    """
    Converte +5561981956970 para +556181956970 (remove 9º dígito)
    """
    if nr_telefone.startswith('+55') and len(nr_telefone) == 14:
        # +55 61 9 81956970 -> +55 61 81956970
        return nr_telefone[:5] + nr_telefone[6:]
    return nr_telefone