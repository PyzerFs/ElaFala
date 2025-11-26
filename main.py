from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import requests
from memoria_utils import salvar_memoria
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


# ============================
# FILTRO DE SEGURANÇA
# ============================
def seguro(texto):
    permitido = ["história", "conto", "lenda", "época", "passado", "era", "narrativa", "ficção"]
    return any(p in texto.lower() for p in permitido)


# ============================
# GERAR ÁUDIO (voz feminina)
# ============================
def gerar_audio(texto):
    from gtts import gTTS
    audio = gTTS(texto, lang="pt", tld="com.br", slow=False)
    audio.save("voz.mp3")
    with open("voz.mp3","rb") as f:
        return base64.b64encode(f.read()).decode()


# ============================
# MAPA MENTAL (imagem gerada)
# ============================
def gerar_imagem(texto):
    placeholder = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
    return placeholder


# ============================
# RESPOSTA PRINCIPAL
# ============================
@app.post("/api/responder")
async def responder(dados: Entrada):

    texto = dados.prompt

    # segurança
    if not seguro(texto):
        resposta = "Só posso responder perguntas relacionadas a histórias, contos, narrativas e lendas."
        audio = gerar_audio(resposta)
        return {"texto": resposta, "audioBase64": audio, "imagens": []}

    salvar_memoria(texto)

    resposta = f"Numa era de engrenagens fumegantes e ideas que moldaram o mundo, sua pergunta ecoa como um sussurro vindo das fábricas de bronze: {texto}"

    audio = gerar_audio(resposta)

    img = gerar_imagem(texto)

    return {
        "texto": resposta,
        "audioBase64": audio,
        "imagens": [img]
    }

