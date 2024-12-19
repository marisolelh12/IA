# REPORTE PROYECTO 4

## **Introducción**

La presente actividad tiene como objetivo principal extraer, limpiar y estructurar información de páginas web para su posterior análisis. Esta información se utiliza para responder preguntas clave sobre temas de interés, como lo son la Ley para la Reforma Judicial y la Ley de los Organismos Autónomos, consolidando datos relevantes en formatos accesibles como JSON y CSV. Las herramientas utilizadas en este proyecto están diseñadas para abordar páginas web y asegurar la calidad y la coherencia de los datos extraídos.

## **Aspectos Considerados al Crear y Utilizar las Herramientas**

### **1. Extracción de Datos de Páginas Web**

#### **Herramientas Utilizadas**

- **`requests`**: Para realizar solicitudes HTTP y obtener el contenido HTML de las páginas web.
- **`BeautifulSoup`**: Para analizar el HTML y extraer elementos específicos (por ejemplo, títulos y párrafos).

#### **Proceso**

1. **Solicitud HTTP**: Se envía una solicitud GET utilizando `requests` para obtener el contenido HTML de la página.
2. **Parseo del HTML**: Con `BeautifulSoup`, se analiza el contenido para extraer elementos relevantes como:
   - El título de la página (`<title>`).
   - Los textos en párrafos (`<p>`).
3. **Limpieza de Datos**: Se implementa una función de limpieza que elimina caracteres no deseados, entidades HTML y normaliza espacios.

#### **Consideraciones**

- **Encabezados HTTP**: Se incluye un User-Agent para evitar bloqueos al parecer una solicitud legítima de un navegador.
- **Manejo de Excepciones**: El script maneja errores como falta de conexión o contenido inaccesible (por ejemplo, errores 404 o 403).

### **2. Limpieza y Normalización de Datos**

#### **Función Implementada**

Se utiliza una función personalizada para limpiar y estructurar los textos extraídos:

```python
import re
import html

def limpiar_texto(texto):
    # Decodificar entidades HTML (e.g., &nbsp;, &amp;)
    texto = html.unescape(texto)
    # Quitar múltiples espacios y saltos de línea
    texto = re.sub(r'\s+', ' ', texto)
    # Quitar caracteres no deseados excepto letras, números, espacios, puntos y comas
    texto = re.sub(r'[^\w\s.,áéíóúñÁÉÍÓÚÑ]', '', texto)
    return texto.strip()
```

#### **Aspectos Clave**

- **Normalización**: Convierte entidades HTML a caracteres legibles y elimina caracteres especiales.
- **Espacios y Saltos de Línea**: Condensa espacios múltiples y líneas en un solo espacio.
- **Flexibilidad**: Permite manejar diferentes formatos de entrada (páginas web, RSS, PDF).

### **3. Almacenamiento de Datos**

#### Formatos Utilizados

1. JSON:

   - Estructura jerárquica para almacenar datos como objetos con claves y valores.
   - Ventaja: Fácil de leer por humanos y máquinas.

2. CSV:

   - Estructura tabular para almacenar datos en filas y columnas.
   - Ventaja: Compatible con herramientas como Excel y pandas (para análisis).

#### Proceso de Almacenamiento

- JSON:

  ```python
  with open("datos_limpios.json", "w", encoding="utf-8") as archivo:
      json.dump(datos_totales, archivo, ensure_ascii=False, indent=4)
  ```

- CSV:

  ```python
  with open("datos_limpios.csv", "w", encoding="utf-8", newline="") as archivo:
      writer = csv.DictWriter(archivo, fieldnames=["origen", "url", "titulo", "contenido", "fecha_extraccion"])
      writer.writeheader()
      writer.writerows(datos_totales)
  ```

### **4. Análisis de Datos Proporcionados**

Se utilizó Chat GPT para el análsis de datos, se le proporcionó el archivo .json generado y las preguntas para que las respondiera a partir de esos datos, obteniendo los siguientes resultados sobre la **Reforma al poder judicial**:

<cite>

1. **¿El diagnóstico de la ley al poder judicial es conocido y qué estudios expertos se tuvieron en cuenta?**
   El diagnóstico de la reforma judicial no estuvo precedido por un análisis profundo o un debate nacional abierto. En algunos textos críticos se señala que la reforma carece de un diagnóstico sólido y fue percibida como un movimiento para cooptar el sistema judicial más que para fortalecerlo.

2. **¿Por qué la reforma no incluyó a las fiscalías y a la defensoría, limitándose solo al poder judicial?**
   La reforma se enfocó exclusivamente en el Poder Judicial, específicamente en su reestructuración y en la elección popular de jueces y magistrados. Aunque incluye cambios como la refundación de la Escuela Nacional de Formación Judicial para capacitar defensores públicos y otros actores, no se menciona una reforma integral que abarque fiscalías o defensorías de manera estructural.

3. **¿Qué medidas concretas se implementarán para evitar la captación del crimen organizado y la violencia en el contexto electoral?**
   La reforma establece la supervisión de los procesos de elección de jueces y magistrados mediante el Instituto Nacional Electoral (INE), pero no se especifican medidas concretas para evitar la influencia del crimen organizado en las elecciones judiciales, lo cual ha sido señalado como un riesgo inherente de este modelo.

4. **¿Cómo garantizar que juristas probos y honestos se animen a competir públicamente frente a los riesgos de la violencia?**
   No hay una propuesta detallada en la reforma para garantizar la protección de los juristas en este contexto. Esto ha generado críticas por no abordar la seguridad de los postulantes, lo cual podría desincentivar la participación de juristas honestos.

5. **¿Cómo se conforman los comités de postulación?**
   Los comités de evaluación serán los encargados de filtrar las candidaturas en las elecciones judiciales, pero no se detallan mecanismos específicos sobre cómo se conforman o cómo garantizar su imparcialidad.

6. **¿Cómo asegurar la carrera judicial?**
   Se incluyó una Ley de Carrera Judicial que establece principios como excelencia, imparcialidad y paridad de género. Además, se busca eliminar prácticas como el nepotismo y la corrupción para legitimar el sistema judicial.

7. **¿Cómo compatibilizar la incorporación de medidas para preservar la identidad de los jueces ("jueces sin rostro") con los estándares internacionales?**
   La implementación de "jueces sin rostro" es criticada como contraria a la Convención Americana de Derechos Humanos, según precedentes de la Corte Interamericana de Derechos Humanos. Este aspecto no parece alinearse con los estándares internacionales.

8. **¿Cómo impactará el costo económico de esta reforma en la promoción y el acceso a la justicia?**
   La reforma plantea costos significativos asociados a la elección popular y la reorganización del sistema judicial. Este gasto podría afectar la sostenibilidad del acceso a la justicia y la operación del sistema, según análisis críticos.

</cite>

Esto fue lo que respondió a la Ley de los Organimos Autónomos:

<cite>

1. **¿El diagnóstico de la ley al poder judicial es conocido y qué estudios expertos se tuvieron en cuenta?**
El diagnóstico de la reforma judicial no estuvo precedido por un análisis profundo o un debate nacional abierto. En algunos textos críticos se señala que la reforma carece de un diagnóstico sólido y fue percibida como un movimiento para cooptar el sistema judicial más que para fortalecerlo.

2. **¿Por qué la reforma no incluyó a las fiscalías y a la defensoría, limitándose solo al poder judicial?**
La reforma se enfocó exclusivamente en el Poder Judicial, específicamente en su reestructuración y en la elección popular de jueces y magistrados. Aunque incluye cambios como la refundación de la Escuela Nacional de Formación Judicial para capacitar defensores públicos y otros actores, no se menciona una reforma integral que abarque fiscalías o defensorías de manera estructural.

3. **¿Qué medidas concretas se implementarán para evitar la captación del crimen organizado y la violencia en el contexto electoral?**
La reforma establece la supervisión de los procesos de elección de jueces y magistrados mediante el Instituto Nacional Electoral (INE), pero no se especifican medidas concretas para evitar la influencia del crimen organizado en las elecciones judiciales, lo cual ha sido señalado como un riesgo inherente de este modelo.

4. **¿Cómo garantizar que juristas probos y honestos se animen a competir públicamente frente a los riesgos de la violencia?**
No hay una propuesta detallada en la reforma para garantizar la protección de los juristas en este contexto. Esto ha generado críticas por no abordar la seguridad de los postulantes, lo cual podría desincentivar la participación de juristas honestos.

5. **¿Cómo se conforman los comités de postulación?**
Los comités de evaluación serán los encargados de filtrar las candidaturas en las elecciones judiciales, pero no se detallan mecanismos específicos sobre cómo se conforman o cómo garantizar su imparcialidad.

6. **¿Cómo asegurar la carrera judicial?**
Se incluyó una Ley de Carrera Judicial que establece principios como excelencia, imparcialidad y paridad de género. Además, se busca eliminar prácticas como el nepotismo y la corrupción para legitimar el sistema judicial.

7. **¿Cómo compatibilizar la incorporación de medidas para preservar la identidad de los jueces ("jueces sin rostro") con los estándares internacionales?**
La implementación de "jueces sin rostro" es criticada como contraria a la Convención Americana de Derechos Humanos, según precedentes de la Corte Interamericana de Derechos Humanos. Este aspecto no parece alinearse con los estándares internacionales.

8. **¿Cómo impactará el costo económico de esta reforma en la promoción y el acceso a la justicia?**
La reforma plantea costos significativos asociados a la elección popular y la reorganización del sistema judicial. Este gasto podría afectar la sostenibilidad del acceso a la justicia y la operación del sistema, según análisis críticos.

</cite>

## **Conclusión**

La combinación de herramientas como `Request` y `BeautifulSoup` con técnicas de limpieza y almacenamiento garantiza un flujo sólido de extracción y procesamiento de datos. Estos datos están listos para un análisis más detallado, que puede responder preguntas clave sobre temas de interés.
