from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("AIzaSyA-R6MWmakLrKkZlQXkOSUVmVhD5MXoZrI"))

model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")
model_image = genai.GenerativeModel("gemini-2.0-flash-exp")  # melhor para imagens

class Entrada(BaseModel):
    prompt: str


def seguro(texto):
    permitido = ["história", "conto", "lenda", "época", "passado", "era", "narrativa", "ficção"]
    return any(p in texto.lower() for p in permitido)


@app.post("/api/responder")
async def responder(dados: Entrada):

    texto_usuario = dados.prompt

    # segurança
    if not seguro(texto_usuario):
        resposta = (
            "Posso apenas narrar histórias, contos e lendas. "
            "Pergunte algo do mundo das narrativas."
        )

        audio = model.generate_content(
            resposta,
            generation_config={"audio_format": "mp3"}
        )

        return {
            "texto": resposta,
            "audioBase64": audio.audio["data"],
            "imagens": []
        }

    # prompt literário
    prompt = f"""
    Você é uma narradora feminina da era da Revolução Industrial.
    Seu estilo é poético, imersivo, cinematográfico e literário.

    O usuário perguntou: "{texto_usuario}"

    Crie uma narrativa detalhada e bonita sobre o tema.
    Não fuja do tema histórias, contos ou narrativas.
    """

    # gerar texto + áudio
    resposta = model.generate_content(
        prompt,
        generation_config={"audio_format": "mp3"}
    )

    texto_final = resposta.text
    audio_final = resposta.audio["data"]

    # gerar IMAGEM ESTILO STEAMPUNK com o tema falado
    img_prompt = f"""
    Crie uma ilustração simples e clara estilo mapa mental,
    no tema da Revolução Industrial,
    representando: {texto_usuario}.
    
    Estilo: engrenagens, vapor, cobre, esquema simples,
    fundo limpo, estética steampunk.
    """

    imagem = model_image.generate_content(
        img_prompt,
        generation_config={"response_mime_type": "image/png"}
    )

    imagem_base64 = imagem.image["data"]

    return {
        "texto": texto_final,
        "audioBase64": audio_final,
        "imagens": [f"data:image/png;base64,{imagem_base64}"]
    }
