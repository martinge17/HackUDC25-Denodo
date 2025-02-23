import os
import csv
import json

# Librerías de Google GenAI
from google import genai
from google.genai import types

# ===========================
# CONFIGURACIÓN
# ===========================
PROJECT_ID = "denodochatbot"        # Tu proyecto de GCP
LOCATION = "us-central1"            # Región
MODEL_NAME = "gemini-2.0-flash-001"   # Modelo a invocar

DIRECTORIO_CSV = "./jjoo"
OUTPUT_DIR = "./vql_output"  # Ruta de salida hardcodeada para los VQL
NUM_LINEAS_MUESTRA = 5

CSV_DELIMITER = ","
CSV_ENCODING = "UTF-8"
CSV_QUOTECHAR = '"'


def obtener_muestra_csv(ruta_csv, num_lineas=5):
    """
    Lee la cabecera y las primeras `num_lineas` de un CSV.
    Devuelve una lista de strings (cada string es una fila separada por comas).
    """
    lineas = []
    with open(ruta_csv, "r", encoding=CSV_ENCODING) as f:
        reader = csv.reader(f, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        for i, row in enumerate(reader):
            if i <= num_lineas:
                lineas.append(CSV_DELIMITER.join(row))
            else:
                break
    return lineas


def construir_prompt(lineas_csv):
    """
    Construye el prompt para inferir tipo de dato y descripción de columnas.
    Le pedimos un JSON con la siguiente estructura:

    {
      "columns": [
        {
          "name": "col_name",
          "type": "STRING|INTEGER|...",
          "description": "..."
        },
        ...
      ]
    }

    Pedimos al modelo devolver solo el JSON (sin backticks ni código).
    """
    prompt = (
        "Actúa como un analista de datos experto. "
        "Te proporcionaré la primera línea (cabecera) y algunas líneas de ejemplo de un fichero CSV. "
        "Estamos en el contexto de los juegos olímpicos de 2024. "
        "Necesito que, basándote en la muestra, generes un JSON con la siguiente estructura:\n\n"
        " {\n"
        "   \"columns\": [\n"
        "       {\n"
        "         \"name\": \"<nombre_de_columna>\",\n"
        "         \"type\": \"<tipo_de_dato_inferido>\",\n"
        "         \"description\": \"<descripción_breve>\"\n"
        "       },\n"
        "       ...\n"
        "   ]\n"
        " }\n\n"
        "Por favor, NO incluyas backticks ni bloques de código, tu respuesta tiene que esta en english, "
        "todas las descripciones en english y no uses ´ ni símbolos raros que puedan llevar a un mal parseo. "
        "Devuélveme **solo** el JSON.\n\n"
        f"La primera línea del CSV (cabecera) es:\n{lineas_csv[0]}\n\n"
        "Las siguientes líneas de ejemplo son:\n"
    )
    for l in lineas_csv[1:]:
        prompt += l + "\n"
    prompt += (
        "\nSi no puedes inferir algún tipo, devuélvelo como STRING.\n"
        "Recuerda: únicamente quiero el JSON sin formatear como bloque de código.\n"
    )
    return prompt


def llamar_gemini(prompt):
    """
    Llama al modelo 'gemini-2.0-flash-001' vía google-genai y devuelve la respuesta como dict (JSON).
    """
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0.0,
        top_p=0.95,
        max_output_tokens=4096,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            ),
        ],
    )

    respuesta_texto = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=generate_content_config,
    ):
        respuesta_texto += chunk.text

    respuesta_texto = respuesta_texto.replace("```", "").strip()

    if respuesta_texto.lower().startswith("json"):
        respuesta_texto = respuesta_texto[4:].strip()

    try:
        resultado_json = json.loads(respuesta_texto)
    except Exception as e:
        raise ValueError(f"El LLM no devolvió JSON válido. Respuesta:\n{respuesta_texto}")

    return resultado_json


def generar_script_vql(csv_filename, columns_info):
    """
    Genera el contenido (string) de un script VQL con descripciones inline y
    forzamos que la ruta sea /home/jjoo/<nombre_archivo>.csv.
    """

    base_name = os.path.splitext(os.path.basename(csv_filename))[0]
    base_name_clean = base_name.replace(" ", "_").replace("-", "_").lower()

    csv_filename_only = os.path.basename(csv_filename)
    denodo_csv_path = f"/home/jjoo/{csv_filename_only}"

    tipo_mapeo = {
        "STRING": "text",
        "INTEGER": "int",
        "FLOAT": "decimal",
        "DOUBLE": "double",
        "BOOLEAN": "boolean",
        "DATE": "date",
        "DATETIME": "timestamp",
    }

    def escape_column_name(name):
        if " " in name:
            return f'"{name}"'
        return name

    esquema_cols = []
    for col in columns_info:
        c_name = col["name"].strip()
        escaped_name = escape_column_name(c_name)
        esquema_cols.append(f"        {escaped_name} = '{c_name}'")
    col_schema_block = ",\n".join(esquema_cols)

    tabla_cols = []
    for col in columns_info:
        c_name = col["name"].strip()
        raw_type = col.get("type", "STRING").upper()
        desc = col.get("description", "").strip()
        desc = desc.replace("'", "´")

        denodo_type = tipo_mapeo.get(raw_type, "text")
        escaped_name = escape_column_name(c_name)

        if desc:
            col_def = f"        {escaped_name}:{denodo_type} (description = '{desc}')"
        else:
            col_def = f"        {escaped_name}:{denodo_type}"

        tabla_cols.append(col_def)
    col_table_block = ",\n".join(tabla_cols)

    constraints_cols = []
    for col in columns_info:
        c_name = col["name"].strip()
        escaped_name = escape_column_name(c_name)
        constraints_cols.append(f"             ADD {escaped_name} NOS ZERO ()")
    col_constraints_block = "\n".join(constraints_cols)

    all_col_names = [escape_column_name(c["name"].strip()) for c in columns_info]
    col_list_block = ", ".join(all_col_names)

    script = f"""# Generated with Denodo Platform 9.1.3.

CREATE OR REPLACE DATASOURCE DF {base_name_clean}
    ROUTE LOCAL 'LocalConnection' '{denodo_csv_path}' FILENAMEPATTERN = ''
    CHARSET = 'UTF-8'
    COLUMNDELIMITER = ','
    ENDOFLINEDELIMITER = '\\n'
    HEADER = TRUE;

CREATE OR REPLACE WRAPPER DF {base_name_clean}
    DATASOURCENAME={base_name_clean}
    OUTPUTSCHEMA (
{col_schema_block}
    );

CREATE OR REPLACE TABLE {base_name_clean} I18N us_pst (
{col_table_block}
    )
    CACHE OFF
    TIMETOLIVEINCACHE DEFAULT
    ADD SEARCHMETHOD {base_name_clean}(
        I18N us_pst
        CONSTRAINTS (
{col_constraints_block}
        )
        OUTPUTLIST ({col_list_block})
        WRAPPER (df {base_name_clean})
    );
"""
    return script


def main():
    """
    Función principal: recorre el directorio de CSV, procesa cada CSV y genera el .vql
    con descripciones inline. La ruta del CSV se fuerza a /home/jjoo/<archivo>.csv
    en lugar de la ruta real local.
    Los archivos VQL se guardarán en la ruta hardcodeada definida en OUTPUT_DIR.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    for archivo in os.listdir(DIRECTORIO_CSV):
        if archivo.lower().endswith(".csv"):
            ruta_csv = os.path.join(DIRECTORIO_CSV, archivo)
            print(f"Procesando: {ruta_csv}")

            lineas_csv = obtener_muestra_csv(ruta_csv, NUM_LINEAS_MUESTRA)
            if not lineas_csv:
                print(f"  El fichero {archivo} está vacío o no se pudo leer.")
                continue

            prompt = construir_prompt(lineas_csv)

            try:
                resultado_json = llamar_gemini(prompt)
            except Exception as e:
                print(f"  Error al llamar al LLM para {archivo}: {e}")
                continue

            if "columns" not in resultado_json:
                print(f"  El JSON devuelto no contiene 'columns' para {archivo}.\nRespuesta:\n{resultado_json}")
                continue

            columns_info = resultado_json["columns"]

            vql_script = generar_script_vql(ruta_csv, columns_info)

            base_name = os.path.splitext(archivo)[0] + ".vql"
            vql_filename = os.path.join(OUTPUT_DIR, base_name)
            with open(vql_filename, "w", encoding="UTF-8") as f:
                f.write(vql_script)

            print(f"  Generado el fichero VQL: {vql_filename}")


if __name__ == "__main__":
    main()
