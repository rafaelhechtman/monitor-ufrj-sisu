import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://acessograduacao.ufrj.br/periodo-2026-1/2026-sisu-mec"
STATE_FILE = "estado_anterior.txt"

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DESTINATARIOS = [
    "rafaelhechtman@gmail.com",
    "eduardohechtman@hotmail.com",
    "estherhechtman@gmail.com",
    # ... até 10
]

def enviar_email():
    if not EMAIL_FROM or not EMAIL_PASSWORD:
        raise RuntimeError("Secrets de e-mail não configurados (EMAIL_FROM/EMAIL_PASSWORD).")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(DESTINATARIOS)
    msg["Subject"] = "Atualização detectada no site da UFRJ (SiSU 2026)"

    corpo = f"""O robô detectou uma atualização no site da UFRJ (SiSU 2026).

Abra o link oficial para conferir:
{URL}
"""
    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, DESTINATARIOS, msg.as_string())

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
        enviar_email()
        salvar_estado_atual(estado_atual)
    else:
        print("Nenhuma atualização detectada.")

if __name__ == "__main__":
    verificar_atualizacao()
