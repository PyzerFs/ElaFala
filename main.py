from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from memoria_utils import salvar_memoria
from gtts import gTTS
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entrada(BaseModel):
    prompt: str


# -----------------------------
# Segurança: só responder histórias
# -----------------------------
def seguro(texto):
    permitido = ["história", "conto", "lenda", "época", "passado", "era", "narrativa", "ficção"]
    return any(p in texto.lower() for p in permitido)


# -----------------------------
# VOZ FEMININA — 100% garantida
# -----------------------------
def criar_audio(texto):
    nome = f"voice_{uuid.uuid4()}.mp3"

    # gTTS voz feminina (padrão do tld com.br)
    tts = gTTS(texto, lang="pt", tld="com.br")
    tts.save(nome)

    with open(nome, "rb") as f:
        base64_audio = base64.b64encode(f.read()).decode("utf-8")

    os.remove(nome)
    return base64_audio


# -----------------------------
# API principal
# -----------------------------
@app.post("/api/responder")
async def responder(dados: Entrada):

    texto = dados.prompt

    # filtro de segurança
    if not seguro(texto):
        resposta = "Só posso responder perguntas sobre histórias, contos, narrativas e lendas."
        audio = criar_audio(resposta)
        return {"texto": resposta, "audioBase64": audio, "imagens": []}

    salvar_memoria(texto)

    resposta = (
        "Em meio às engrenagens da Revolução Industrial, "
        "sua pergunta ecoa como o vapor que sobe das chaminés de aço. "
        f"{texto}"
    )

    # voz feminina REAL
    audio = criar_audio(resposta)

    # mapa mental simples
    img = "https://i.imgur.com/NdYH2gW.jpeg"

    return {
        "texto": resposta,
        "audioBase64": audio,
        "imagens": [img]
    }
