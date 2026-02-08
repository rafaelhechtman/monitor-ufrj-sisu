import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://news.ycombinator.com/"
STATE_FILE = "estado_anterior.txt"

def obter_estado_pagina():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    texto = soup.get_text(separator=" ", strip=True)

    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

def carregar_estado_anterior():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return f.read().strip()

def salvar_estado_atual(estado):
    with open(STATE_FILE, "w") as f:
        f.write(estado)

def verificar_atualizacao():
    estado_atual = obter_estado_pagina()
    estado_anterior = carregar_estado_anterior()

    if estado_anterior is None:
        salvar_estado_atual(estado_atual)
        print("Estado inicial salvo.")
        return

    if estado_atual != estado_anterior:
        print("ATUALIZAÇÃO DETECTADA NO SITE DA UFRJ.")
        salvar_estado_atual(estado_atual)
    else:
        print("Nenhuma atualização detectada.")

if __name__ == "__main__":
    verificar_atualizacao()
