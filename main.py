from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import base64
from memoria_utils import salvar_memoria
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIG GEMINI
genai.configure(api_key=os.getenv("AIzaSyA-R6MWmakLrKkZlQXkOSUVmVhD5MXoZrI"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")


class Entrada(BaseModel):
    prompt: str


# -----------------------------
# Segurança sobre HISTÓRIAS
# -----------------------------
def seguro(texto):
    permitido = ["história", "conto", "lenda", "época", "passado", "era", "narrativa", "ficção"]
    return any(p in texto.lower() for p in permitido)


# -----------------------------
# API PRINCIPAL - GEMINI
# -----------------------------
@app.post("/api/responder")
async def responder(dados: Entrada):

    texto = dados.prompt

    # filtro de segurança
    if not seguro(texto):
        resposta = "Só posso falar sobre temas ligados a histórias, contos, eras passadas e narrativas."
        
        audio_response = model.generate_content(
            contents=resposta,
            generation_config={"audio_format": "mp3"}
        )

        audio = audio_response.audio["data"]

        return {
            "texto": resposta,
            "audioBase64": audio,
            "imagens": []
        }

    salvar_memoria(texto)

    prompt_gemini = f"""
    Você é uma narradora feminina da era da Revolução Industrial.
    Responda de forma poética, literária e imersiva.

    O usuário perguntou: "{texto}"

    Regra: nunca saia do tema histórias, contos, lendas e narrativas.
    """

    # GEMINI → texto + voz feminina ao mesmo tempo
    resposta = model.generate_content(
        contents=prompt_gemini,
        generation_config={"audio_format": "mp3"}
    )

    texto_final = resposta.text
    audio_base64 = resposta.audio["data"]

    imagem = "https://i.imgur.com/NdYH2gW.jpeg"

    return {
        "texto": texto_final,
        "audioBase64": audio_base64,
        "imagens": [imagem]
    }
