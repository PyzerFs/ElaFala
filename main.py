from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyA-R6MWmakLrKkZlQXkOSUVmVhD5MXoZrI"))

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

    # Gerar texto + áudio
    resposta = model.generate_content(
        contents=pergunta,
        response_modalities=["text", "audio"]
    )
    texto_final = resposta.text
    audio_base64 = resposta.audio.data

    # Gerar imagem
    imagem_res = model_image.generate_content(
        contents=(
            f"Ilustração estilo steampunk / revolução industrial, "
            f"como um mapa mental que representa: \"{pergunta}\""
        ),
        response_mime_type="image/png"
    )
    imagem_base64 = imagem_res.image.data

    return {
        "texto": texto_final,
        "audioBase64": audio_base64,
        "imagens": [f"data:image/png;base64,{imagem_base64}"]
    }
