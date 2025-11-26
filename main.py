from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ------------------------ CONFIG ---------------------------
genai.configure(api_key=os.getenv("AIzaSyA-R6MWmakLrKkZlQXkOSUVmVhD5MXoZrI"))

model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")
model_image = genai.GenerativeModel("gemini-2.0-flash-exp")  # melhor para imagens

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entrada(BaseModel):
    prompt: str

# ------------------------ API ------------------------------

@app.post("/api/responder")
async def responder(dados: Entrada):

    entrada = dados.prompt

    prompt_texto = f"""
    Você é uma narradora feminina da estética steampunk/revolução industrial.
    Sua voz e suas respostas são literárias, poéticas e imersivas.
    Crie uma resposta detalhada sobre:

    "{entrada}"

    Adote sempre tons narrativos.
    """

    # GEMINI → texto + áudio feminino
    resposta = model.generate_content(
        prompt_texto,
        generation_config={
            "audio_format": "mp3"
        }
    )

    texto_final = resposta.text
    audio_base64 = resposta.audio["data"]

    # -------- GERAR IMAGEM --------
    prompt_img = f"""
    Crie uma ilustração simples estilo "mapa mental", clara e direta,
    com elementos steampunk (engrenagens, cobre, vapor), representando:
    {entrada}.
    Fundo limpo, forma simples, estética industrial.
    """

    imagem = model_image.generate_content(
        prompt_img,
        generation_config={
            "response_mime_type": "image/png"
        }
    )

    imagem_base64 = imagem.image["data"]

    return {
        "texto": texto_final,
        "audioBase64": audio_base64,
        "imagens": [f"data:image/png;base64,{imagem_base64}"]
    }
