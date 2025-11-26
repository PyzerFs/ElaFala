from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configurar Gemini
genai.configure(api_key=os.getenv("AIzaSyA-R6MWmakLrKkZlQXkOSUVmVhD5MXoZrI"))

# Modelos
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")
model_image = genai.GenerativeModel("gemini-2.0-flash-exp")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Entrada(BaseModel):
    prompt: str


@app.post("/api/responder")
async def responder(dados: Entrada):

    
    pergunta = dados.prompt

    
    # --------------------- TEXTO + ÁUDIO ---------------------
    resposta = model.generate_content(
        contents=pergunta,
        # Aqui você pede explicitamente ÁUDIO
        response_modalities=["text", "audio"]
    )

    texto_final = resposta.text
    audio_data = resposta.audio.data  # <- Agora o SDK usa .data

    
    # ----------------------- IMAGEM --------------------------
    imagem_res = model_image.generate_content(
        contents=f"""
            Gere uma imagem estilo mapa mental steampunk,
            com engrenagens, vapor, metais, e elementos simples que representem:
            "{pergunta}"
        """,
        # Aqui o campo correto para pedir imagem
        response_mime_type="image/png"
    )

    imagem_base64 = imagem_res.image.data  # <- Nova sintaxe oficial

    return {
        "texto": texto_final,
        "audioBase64": audio_data,
        "imagens": [f"data:image/png;base64,{imagem_base64}"]
    }

    
