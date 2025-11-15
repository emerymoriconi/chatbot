import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=GEMINI_API_KEY
)

def generate_response(message: str, history: list):
    """
    Gera resposta usando Gemini.
    message = última mensagem do usuário
    history = mensagens anteriores da sessão
    """

    # Converter histórico para o formato aceito:
    messages = []

    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # adiciona a nova mensagem do usuário
    messages.append({"role": "user", "content": message})

    # envia para o modelo
    response = model.invoke(messages)

    # sempre retorna string
    return response.content
