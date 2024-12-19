import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import re
import html

# Función para limpiar y estructurar texto
def limpiar_texto(texto):
    texto = html.unescape(texto)
    texto = re.sub(r'\s+', ' ', texto)
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
        "https://morena.senado.gob.mx/presentacion-de-las-leyes-reglamentarias-del-poder-judicial-de-la-federacion-en-reunion-de-comisiones-unidas-de-justicia-y-estudios-legislativos/",
        "https://www.gob.mx/presidencia/prensa/con-el-avance-de-la-reforma-al-poder-judicial-triunfa-el-pueblo-la-constitucion-y-el-estado-de-derecho-presidenta-claudia-sheinbaum",
        "https://elpais.com/mexico/2024-09-11/que-dice-la-reforma-judicial-y-que-sigue-tras-su-aprobacion-en-el-senado.html",
        "https://www.milenio.com/negocios/resaltan-interes-ip-sociedad-civil-tampico-reforma-judicial",
        "https://www.siempre.mx/2024/12/el-fin-de-una-era/",
        "https://morena.senado.gob.mx/avanzamos-hacia-una-reforma-judicial-agil-eficaz-y-humanista-antonino-morales/",
        "https://www.eldiariodechihuahua.mx/local/2024/dec/18/va-en-pri-en-contra-de-la-reforma-judicial-662884.html",
        "https://www.milenio.com/videos/milenio-tv/el-asalto-a-la-razon/proceso-reforma-judicial-plagado-irregularidades-asalto-razon",
        "https://oem.com.mx/elsoldelcentro/analisis/el-agora-listas-de-la-reforma-judicial-federal-20739538",
        "https://oem.com.mx/elsoldemexico/mexico/que-sigue-con-la-reforma-judicial-fechas-clave-de-los-comicios-para-elegir-jueces-y-magistrados-19333464",
        "https://oem.com.mx/elsoldeleon/local/jueces-de-guanajuato-preocupados-por-la-reforma-judicial-que-podria-despedirlos-injustificadamente-20601869",
        "https://agendaestadodederecho.com/errores-de-la-reforma-a-la-justicia-en-mexico/",
        "https://www.reformajudicial.gob.mx/secciones/reforma/",
        "https://prime.tirant.com/mx/actualidad-prime/reforma-judicial/",
        "https://comercioyjusticia.info/opinion/reforma-judicial-en-mexico-avance-o-retroceso/"
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