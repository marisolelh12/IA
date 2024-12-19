import requests
from bs4 import BeautifulSoup
import feedparser
import pdfplumber
import json
import csv
from datetime import datetime
import re
import html

# Función para limpiar y estructurar texto
def limpiar_texto(texto):
    # Decodificar entidades HTML (e.g., &nbsp;, &amp;)
    texto = html.unescape(texto)
    # Quitar múltiples espacios y saltos de línea
    texto = re.sub(r'\s+', ' ', texto)
    # Quitar caracteres no deseados excepto letras, números, espacios, puntos y comas
    texto = re.sub(r'[^\w\s.,áéíóúñÁÉÍÓÚÑ]', '', texto)
    return texto.strip()

# Función para extraer texto de una página web
def extraer_pagina_web(url):
    print(f"Extrayendo página web: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        titulo = limpiar_texto(soup.title.string) if soup.title else "Sin Título"
        contenido = limpiar_texto(" ".join([p.text for p in soup.find_all("p")]))
        return {
            "origen": "Sitio Web",
            "url": url,
            "titulo": titulo,
            "contenido": contenido,
            "fecha_extraccion": datetime.now().strftime("%Y-%m-%d"),
        }
    except Exception as e:
        print(f"Error al extraer {url}: {e}")
        return None

# Función para guardar datos en JSON
def guardar_en_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)
    print(f"Datos guardados en {nombre_archivo} (JSON)")

# Función para guardar datos en CSV
def guardar_en_csv(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["origen", "url", "titulo", "contenido", "fecha_extraccion"])
        writer.writeheader()
        writer.writerows(datos)
    print(f"Datos guardados en {nombre_archivo} (CSV)")

# Flujo principal
def main():
    paginas_web = [
        "https://coparmex.org.mx/la-desaparicion-de-los-organismos-autonomos-compromete-el-futuro-de-mexico-pone-en-riesgo-el-equilibrio-de-poderes-y-la-democracia/",
        "https://elpais.com/mexico/2024-08-28/organos-autonomos-que-son-y-que-implica-la-reforma-para-desaparecerlos.html",
        "https://www.bloomberglinea.com/actualidad/senado-de-mexico-aprueba-ley-que-elimina-organismos-autonomos-cinco-cosas-que-debe-saber/",
        "https://www.milenio.com/politica/diputados-discutiran-extincion-de-siete-organismos-autonomos",
        "https://www.24-horas.mx/2024/11/27/aprueba-senado-en-comisiones-desaparicion-de-organismos-autonomos/",
        "https://animalpolitico.com/politica/organos-autonomos-discutira-camara-diputados?fbclid=IwY2xjawGftcZleHRuA2FlbQIxMAABHQkmwZE_TE3uFPc0oG2tagvCiofvBJizuoZfJtPcl0cv_ogAXphFdsBFjg_aem_ePLjUyQVuPLnSA1HHOTPvA",
        "https://www.infobae.com/mexico/2024/08/24/coparmex-expresa-preocupacion-por-extincion-de-organismos-autonomos-llama-a-legisladores-a-reflexionar/",
        "https://latinus.us/mexico/2024/11/11/diputados-de-la-4t-van-este-miercoles-por-extincion-de-organismos-autonomos-votaran-dictamen-de-prision-preventiva-oficiosa-que-agrega-nuevos-delitos-128168.html"
    ]

    # Lista para almacenar todos los datos
    datos_totales = []

    # Extraer datos de páginas web
    for url in paginas_web:
        resultado = extraer_pagina_web(url)
        if resultado:
            datos_totales.append(resultado)

    # Guardar resultados en JSON y CSV
    guardar_en_json("datos_limpios.json", datos_totales)
    guardar_en_csv("datos_limpios.csv", datos_totales)

if __name__ == "__main__":
    main()