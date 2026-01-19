---
applyTo: '**'
---
# Eu

Eu estou fazendo um software para como projeto final do CS50. Quero aprender durante o processo cada ponto.

# Projeto Final do CS50
Especificação de Projeto: AI FamOps (Assistente Familiar)
1. Descrição Geral
O AI FamOps é uma solução de engenharia de software desenhada para centralizar e automatizar a gestão da rotina familiar. O sistema atua como um "Orquestrador de Intenções", permitindo que membros de uma família gerenciem tarefas, calendários e listas de compras através de uma interface de conversação no WhatsApp, eliminando a necessidade de múltiplos aplicativos.

2. Visão do Produto
Problema: A fragmentação de informações familiares (mensagens soltas, esquecimentos, carga mental elevada).

Solução: Um assistente via WhatsApp processado por LLM (Large Language Model) que organiza as demandas em ferramentas estruturadas (Trello/Google).

Diferencial: Cadastro centralizado e interface amigável via web para configuração inicial.

3. Arquitetura do Sistema (Stack)
Backend: Python com Flask (Lógica de API e Webhook).

Frontend: HTML5, CSS3 (Bootstrap 5) e JavaScript (Cadastro e Dashboard).

Banco de Dados: PostgreSQL (Persistência de dados de usuários e famílias).

Processamento de Linguagem: API do Google Gemini ou OpenAI (GPT-4o).

Comunicação: Twilio API for WhatsApp.

Hospedagem: Railway.

4. Requisitos Funcionais
RF01: Portal de Cadastro (Interface Web)
A porta de entrada do sistema. Uma aplicação web responsiva para:

Cadastro da Família: Nome da família e criação de um ID único.

Gestão de Membros: Adição de membros com Nome, E-mail e Número de WhatsApp (formato internacional).

Configuração de Integrações: Campos para inserir as chaves de API ou IDs de quadros do Trello/Google Calendar.

RF02: Webhook de Processamento (WhatsApp)
O motor que roda silenciosamente:

Receber mensagens (texto/áudio) via Twilio.

Validar se o número pertence a uma família cadastrada.

Enviar o contexto para a LLM com instruções de sistema (JSON Mode).

RF03: Despachante de Ações (Action Dispatcher)
O código Python que interpreta o retorno da IA e executa:

Trello: POST /cards (Adicionar itens de compras ou projetos).

Google Calendar: POST /events (Agendar reuniões escolares ou consultas).

Feedback: Enviar mensagem de confirmação automática no WhatsApp.

5. Modelo de Dados (Entidades Principais)
SQL
-- Estrutura simplificada para o PostgreSQL
CREATE TABLE families (
    id SERIAL PRIMARY KEY,
    family_name VARCHAR(100) NOT NULL,
    trello_board_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    family_id INTEGER REFERENCES families(id),
    name VARCHAR(100) NOT NULL,
    whatsapp_number VARCHAR(20) UNIQUE NOT NULL,
    role VARCHAR(20) -- 'admin' ou 'member'
);

CREATE TABLE task_history (
    id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES members(id),
    raw_text TEXT,
    action_executed VARCHAR(50),
    status VARCHAR(20)
);
6. Configuração da IA (O System Prompt)
Para o MVP, a configuração do POST para a LLM deve conter esta instrução mestra:

"Você é o Assistente FamOps. Analise a mensagem do usuário. Se for algo para comprar ou tarefa manual, responda APENAS o JSON: {"action": "trello", "item": "...", "list": "..."}. Se envolver data e hora, responda: {"action": "calendar", "event": "...", "date": "..."}. Se for apenas conversa, responda: {"action": "chat", "response": "..."}."

7. Roadmap de Implementação para o CS50
Fase 1: Setup e Banco (Dias 1-3)
Configurar o banco PostgreSQL no Railway.

Criar as rotas Flask para o formulário de cadastro HTML.

Fase 2: O Webhook "Eco" (Dias 4-6)
Configurar o Twilio Sandbox.

Criar a rota /webhook que recebe uma mensagem e apenas a devolve (para testar a conexão).

Fase 3: Integração com IA (Dias 7-10)
Implementar a chamada de API para a LLM (Gemini/OpenAI).

Criar o parser que lê o JSON retornado pela IA.

Fase 4: Integrações Externas (Dias 11-14)
Conectar com a API do Trello.

Finalizar o CSS da página de cadastro para garantir que seja "Mobile Friendly".

8. Por que este projeto é "Nota 10" no CS50?
Complexidade: Usa Python além do básico, manipulando APIs JSON complexas.

Utilidade Real: Resolve um problema que o próprio aluno (ou qualquer pessoa) enfrenta.

Full Stack: Envolve banco de dados relacional, backend lógico e frontend funcional.

Inovação: Demonstra conhecimento em IA, a habilidade mais requisitada atualmente.