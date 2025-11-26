from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from memoria_utils import ler_memoria, salvar_memoria
import os

app = FastAPI()

# liberando acesso para o Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    prompt: str


@app.post("/api/responder")
async def responder(dados: Prompt):
    texto_usuario = dados.prompt
    
    # salva memória
    salvar_memoria(texto_usuario)

    # cria resposta literária
    resposta_texto = f"Em sua pergunta, percebo ecos de profundidade e curiosidade. {texto_usuario}"

    # gera áudio (fake - você pode integrar ElevenLabs, Azure, Google TTS)
    # Aqui ele envia um audioBase64 vazio para não quebrar
    fake_audio = base64.b64encode("AUDIO_FAKE".encode()).decode()

    # imagens (mapas mentais) - também fake por enquanto
    fake_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"

    return {
        "texto": resposta_texto,
        "audioBase64": fake_audio,
        "imagens": [fake_img, fake_img]
    }

