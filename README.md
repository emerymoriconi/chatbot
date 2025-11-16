# Backend - Chatbot Multiusuário com Gemini e FastAPI

Este é o serviço de backend para o projeto **Chatbot Multiusuário**, uma API RESTful desenvolvida com **FastAPI** que gerencia sessões de conversa e interage com o modelo **Gemini 2.5 Flash** da Google. A arquitetura é desenhada para ser limpa, eficiente e pronta para implantação em containers (Docker) em ambientes como o AWS EC2.

---

## 📜 Funcionalidades

### Gerenciamento de Sessão (Multiusuário)
- **Criação de Sessão:** Rota para gerar um novo e único `session_id` (UUID) para cada usuário/aba de navegador.  
- **Histórico em Memória:** Armazenamento do histórico de conversas em um dicionário (em memória) associado ao `session_id`.  
- **Contexto de Conversa:** Preservação do contexto, enviando o histórico completo (mensagens anteriores) junto com a nova pergunta do usuário para o LLM.

### Serviço de LLM (Large Language Model)
- **Integração Gemini:** Uso do modelo `gemini-2.5-flash` via `langchain-google-genai` para geração de respostas.  
- **Formato de Comunicação:** Conversão do histórico de sessão para o formato aceito pela API do Gemini/LangChain.  
- **Saída Padronizada:** O modelo sempre retorna a resposta como uma string em Markdown, renderizada no frontend.

---

## 🎯 Casos de Uso

| Caso de Uso | Descrição |
|-------------|-----------|
| **UC-01: Iniciar Nova Sessão** | Um usuário acessa a página e solicita uma nova sessão, obtendo um `session_id` único. |
| **UC-02: Enviar Mensagem** | Um usuário envia uma mensagem ao chatbot. |
| **UC-03: Manter Contexto** | O sistema envia o histórico completo dessa sessão ao Gemini, obtendo uma resposta contextualizada. |
| **UC-04: Salvar Interação** | A pergunta do usuário e a resposta do chatbot são salvas no histórico. |
| **UC-05: Visualizar Resposta** | O frontend recebe a resposta e renderiza em HTML. |

---

## 🏛️ Arquitetura

A aplicação segue uma arquitetura simples e modular:

- **Framework:** FastAPI  
- **LLM Integration:** `langchain-google-genai`  
- **Gerenciamento de Sessão:** Classe `SessionManager` usando dicionário em memória  
- **Containerização:** Docker + Uvicorn  
- **Configuração:** `python-dotenv` carregando `GEMINI_API_KEY` via `.env`

---

## 🚀 Como Executar (Implantação em AWS EC2 via Docker Hub)

Este projeto é desenvolvido para implantação containerizada.

### Pré-requisitos
- Python (3.11+ recomendado)  
- Docker instalado localmente  
- Conta no Docker Hub  
- Instância AWS EC2 com Docker e porta **8000** liberada  

---

## Passos para Instalação e Implantação

### **1. Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz:

```bash
GEMINI_API_KEY="SUA_CHAVE_AQUI"
```

---

### 2. Construir e Enviar a Imagem Docker

Substitua `SEU_USUARIO` pelo seu usuário do Docker Hub:

```bash
# 1. Construir a imagem
docker build -t chatbot-gemini-fastapi .

# 2. Taggear para o Docker Hub
docker tag chatbot-gemini-fastapi SEU_USUARIO/chatbot-gemini-fastapi:latest

# 3. Fazer login
docker login

# 4. Enviar a imagem
docker push SEU_USUARIO/chatbot-gemini-fastapi:latest
```

---

### 3. Implantar no AWS EC2

Conectado via SSH ao EC2:

```bash
# 1. Puxar imagem
docker pull SEU_USUARIO/chatbot-gemini-fastapi:latest

# 2. Executar container
docker run -d \
  -p 8000:8000 \
  --name gemini-chatbot-instance \
  --env GEMINI_API_KEY="SUA_CHAVE_AQUI" \
  SEU_USUARIO/chatbot-gemini-fastapi:latest
```
O chatbot estará acessível em: http://<IP_PÚBLICO_DO_EC2>:8000

---

## ⚙️ Aspectos Técnicos

- **Linguagem:** Python 3.11+  
- **Framework:** FastAPI  
- **Servidor ASGI:** Uvicorn  
- **LLM:** Gemini 2.5 Flash  
- **SDK:** langchain-google-genai  
- **Containerização:** Docker  
- **Validação:** Pydantic  
- **Dependências:** `requirements.txt` / Pip  

---

## 🔚 Endpoints da API

A documentação Swagger estará disponível em **/docs**.

---

## 📝 Rotas de Sessão

### **GET /**
Retorna o frontend (`index.html`).

### **GET /new_session**
Cria um novo `session_id`.

**Resposta:**
```json
{
  "session_id": "UUID_AQUI"
}
```

## 💬 Rota de Chat

### **POST /chat**

Envia a mensagem do usuário, gera a resposta do Gemini e salva no histórico.

**Corpo da requisição:**
```json
{
  "session_id": "string (UUID da sessão)",
  "message": "string (Mensagem do usuário)"
}
```

**Resposta:**
```json
{
  "response": "string (Resposta do Gemini em formato Markdown)"
}
```


