import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helper import apology, login_required, validar_email, validar_telefone_e164, formatar_telefone_whatsapp
from jobs.scheduler import iniciar_scheduler
from sqlalchemy import create_engine, text
from whatsapp import processar_mensagem
from werkzeug.security import check_password_hash, generate_password_hash

# Load environment variables
load_dotenv()

# app
app = Flask(__name__)

# Configure session (igual ao CS50)
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-sodalis-2026")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0 # producao 3600

Session(app)

# # Iniciar scheduler apenas em produção
scheduler = iniciar_scheduler()

# Database setup
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)


# Adicionar filtro Jinja para formatação
@app.template_filter('regex_replace')
def regex_replace(s, find, replace):
    import re
    return re.sub(find, replace, s)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if session.get("user_id"):
        return redirect("/minhas-tarefas")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    if request.method == "POST":
        session.clear()
        nr_telefone = request.form.get("nr_telefone")
        password = request.form.get("password")

        if not nr_telefone or nr_telefone == "+55":
            flash("É preciso inserir o número de telefone.", "danger")
            return render_template("login.html"), 403

        if not password:
            flash("É preciso inserir a senha.", "danger")
            return render_template("login.html"), 403

        # Verificar senha
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id_usuario, hash FROM public.usuario WHERE nr_telefone = :nr_telefone"),
                {"nr_telefone": nr_telefone}
            )
            rows = result.mappings().fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Telefone ou senha inválidos.", "danger")
            return render_template("login.html"), 403

        session["user_id"] = rows[0]["id_usuario"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        nr_telefone = request.form.get("nr_telefone")
        nr_whatsapp = formatar_telefone_whatsapp(nr_telefone)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not nome or not email or not nr_telefone or not password or not confirmation:
            flash("Preencha todos os campos.", "danger")
            return render_template("register.html", nome=nome, email=email, nr_telefone=nr_telefone), 400
        
        if not validar_email(email):
            flash("E-mail inválido. Use formato: email@exemplo.com", "danger")
            return render_template("register.html", nome=nome, email=email, nr_telefone=nr_telefone), 400

        if not validar_telefone_e164(nr_telefone):
            flash("Telefone inválido. Use formato: +5561981234567", "danger")
            return render_template("register.html", nome=nome, email=email, nr_telefone=nr_telefone), 400
        
        if password != confirmation:
            flash("As senhas não coincidem.", "danger")
            return render_template("register.html", nome=nome, email=email, nr_telefone=nr_telefone), 400

        hash = generate_password_hash(password)

        # Verificar duplicatas
        with engine.connect() as connection:
            trans = connection.begin()

            try:

                result = connection.execute(
                    text("SELECT email, nr_telefone FROM public.usuario WHERE email = :email OR nr_telefone = :nr_telefone"),
                    {"email": email, "nr_telefone": nr_telefone}
                )
                usuario_existente = result.fetchone()
                
                if usuario_existente:
                    flash("E-mail ou telefone já cadastrado.", "danger")
                    return render_template("register.html", nome=nome, email=email, nr_telefone=nr_telefone), 400
                
                # 1. Criar comunidade pessoal primeiro
                result = connection.execute(
                    text(f"INSERT INTO comunidade(nm_comunidade) VALUES ('Pessoal') RETURNING id_comunidade"),
                    {}
                )
                id_comunidade_pessoal = result.fetchone()[0]
                
                # 2. Criar usuário vinculado a comunidade pessoal
                result = connection.execute(
                    text("""
                        INSERT INTO usuario(nome, email, nr_telefone, hash, nr_whatsapp, id_comunidade_pessoal) 
                        VALUES (:nome, :email, :nr_telefone, :hash, :nr_whatsapp, :id_comunidade_pessoal) 
                        RETURNING id_usuario
                    """),
                    {
                        "nome": nome, 
                        "email": email, 
                        "nr_telefone": nr_telefone, 
                        "hash": hash, 
                        "nr_whatsapp": nr_whatsapp,
                        "id_comunidade_pessoal": id_comunidade_pessoal
                    }
                )
                id_usuario = result.fetchone()[0]
                
                # 3. Vincular usuário à comunidade pessoal
                connection.execute(
                    text("INSERT INTO composicao(id_comunidade, id_usuario) VALUES (:id_comunidade, :id_usuario)"),
                    {"id_comunidade": id_comunidade_pessoal, "id_usuario": id_usuario}
                )
                
                trans.commit()            
            except:
                trans.rollback()
                raise

        flash("Registro realizado com sucesso! Pode fazer o login.", "success")
        return redirect("/login")
    
    return render_template("register.html")


@app.route("/familia")
@login_required
def familia():

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT usuario.id_usuario,
                INITCAP(SPLIT_PART(usuario.nome, ' ', 1)) as nome,
                usuario.nr_telefone,
                usuario.nr_whatsapp
                FROM public.usuario usuario
                WHERE 
                    id_usuario in 
                    (SELECT id_usuario FROM public.composicao WHERE id_comunidade in (
                    SELECT id_comunidade FROM public.composicao WHERE id_usuario = :id_usuario))"""),
            {"id_usuario": session["user_id"]}
        )
        familia = result.mappings().fetchall()

    return render_template("familia.html", familia=familia)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    processar_mensagem(incoming_msg, sender)
    return "OK", 200


@app.route("/minhas-tarefas")
@login_required
def minhas_tarefas():

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT * FROM tarefa
                LEFT JOIN atribuicao ON atribuicao.id_tarefa = tarefa.id_tarefa
                WHERE atribuicao.id_usuario = :id_usuario"""),
            {"id_usuario": session["user_id"]}
        )
        tarefas = result.mappings().fetchall()

    return render_template("minhas_tarefas.html", tarefas=tarefas)



@app.route("/minhas-tarefas/nova", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    
    if request.method == "POST":
        nm_tarefa = request.form.get("nm_tarefa")
        
        if not nm_tarefa:
            flash("O nome da tarefa é obrigatório.", "danger")
            return render_template("nova_tarefa.html")
        
        with engine.connect() as connection:
            trans = connection.begin()
            
            try:
                # 1. Buscar comunidade pessoal do usuário
                result = connection.execute(
                    text("SELECT id_comunidade_pessoal FROM usuario WHERE id_usuario = :id_usuario"),
                    {"id_usuario": session["user_id"]}
                )
                id_comunidade_pessoal = result.fetchone()[0]
                
                # 2. Inserir tarefa
                result = connection.execute(
                    text("INSERT INTO tarefa (nm_tarefa, id_comunidade) VALUES (:nm_tarefa, :id_comunidade) RETURNING id_tarefa"),
                    {"nm_tarefa": nm_tarefa, "id_comunidade": id_comunidade_pessoal}
                )
                id_tarefa = result.fetchone()[0]
                
                # 3. Criar atribuição
                connection.execute(
                    text("""
                        INSERT INTO atribuicao (id_usuario, id_comunidade, id_tarefa, id_periodicidade) 
                        VALUES (:id_usuario, :id_comunidade, :id_tarefa, 1)
                    """),
                    {
                        "id_usuario": session["user_id"],
                        "id_comunidade": id_comunidade_pessoal,
                        "id_tarefa": id_tarefa
                    }
                )
                
                trans.commit()
                
            except:
                trans.rollback()
                raise
        
        flash("Tarefa criada com sucesso!", "success")
        return redirect("/minhas-tarefas")
    
    return render_template("nova_tarefa.html")


@app.route("/minhas-tarefas/<int:id_tarefa>/excluir", methods=["POST"])
@login_required
def excluir_tarefa(id_tarefa):
    
    with engine.connect() as connection:
        trans = connection.begin()
        
        connection.execute(
            text("DELETE FROM atribuicao WHERE id_tarefa = :id_tarefa"),
            {"id_tarefa": id_tarefa}
        )
        
        connection.execute(
            text("DELETE FROM tarefa WHERE id_tarefa = :id_tarefa"),
            {"id_tarefa": id_tarefa}
        )
        
        trans.commit()
    
    flash("Tarefa excluída com sucesso!", "success")
    return redirect("/minhas-tarefas")

# # modo debuter provisorio
# if __name__ == "__main__":
#     app.run(debug=True)