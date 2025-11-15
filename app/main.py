from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.session_manager import SessionManager
from app.schemas import MessageInput
from fastapi.responses import FileResponse
from app.llm_service import generate_response

app = FastAPI()
session_manager = SessionManager()

# permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/new_session")
def new_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id}

@app.post("/chat")
def chat(data: MessageInput):
    history = session_manager.get_history(data.session_id)

    # adicionar pergunta ao histórico
    session_manager.add_message(data.session_id, "user", data.message)

    # gerar resposta
    response = generate_response(data.message, history)

    # salvar resposta
    session_manager.add_message(data.session_id, "assistant", response)

    return {"response": response}
