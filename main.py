# main.py

import os
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Configura o diretório do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")  # se o CSV estiver na pasta 'dados'
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados")  # pasta das imagens

# Carrega o catálogo
catalogo_csv = os.path.join(DADOS_DIR, "catalogo.csv")
if not os.path.exists(catalogo_csv):
    raise FileNotFoundError("Arquivo catalogo.csv não encontrado na pasta 'dados'.")

df = pd.read_csv(catalogo_csv)

# Inicializa o app FastAPI
app = FastAPI(title="App Loc - Catálogo de Peças")

# Permite que o site seja acessado de qualquer lugar (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensagem": "App Loc rodando!"}

@app.get("/search")
def buscar_part_number(part_number: str):
    """
    Busca o part number no catálogo e retorna os dados encontrados.
    """
    resultados = df[df['texto_extraido'].str.contains(part_number, case=False, na=False)]
    retorno = resultados.to_dict(orient="records")
    return JSONResponse(content=retorno)

@app.get("/image/{nome_arquivo}")
def buscar_imagem(nome_arquivo: str):
    """
    Retorna a imagem da peça solicitada.
    """
    caminho_imagem = os.path.join(RESULTADOS_DIR, nome_arquivo)
    if not os.path.exists(caminho_imagem):
        return JSONResponse(content={"erro": "Arquivo de imagem não encontrado"}, status_code=404)
    return FileResponse(caminho_imagem)
