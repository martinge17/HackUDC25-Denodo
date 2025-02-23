import json
import os
import subprocess
from google import genai
from google.genai import types

# ===========================
# CONFIGURACIÓN
# ===========================
PROJECT_ID = "denodochatbot"        # Tu proyecto de GCP
LOCATION = "us-central1"            # Región
MODEL_NAME = "gemini-2.0-flash-001" # Modelo a invocar

# Directorio donde se guardará el archivo .vql
OUTPUT_DIR = "./vql_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def leer_relaciones(ruta_relaciones=None):
    """
    Lee las relaciones ejecutando el script generador o desde archivo
    """
    if ruta_relaciones and os.path.exists(ruta_relaciones):
        with open(ruta_relaciones, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Ejecutar el script generador de relaciones
        resultado = subprocess.run(
            ["python", "./scripts/databaseRelations-generator.py", "./jjoo"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if resultado.returncode == 0:
            return resultado.stdout
        else:
            raise RuntimeError(
                f"Error generando relaciones: {resultado.stderr}"
            )

def construir_prompt(relaciones, contexto, intereses, tipo_vista, max_tablas, max_columnas):
    """
    Construye el prompt adaptado al tipo de vista con reglas específicas
    """
    reglas_especificas = {
        "especifica": {
            "descripcion": "Vista ESPECÍFICA (muy enfocada)",
            "instrucciones": """Requisitos ESPECÍFICOS:
- Máximo de 2 tablas relacionadas directamente con los intereses, si con una llega se cogera una
- 3 columnas clave por tabla como máximo
- Filtros estrictos aplicados a disciplinas o países
- Joins simples con relaciones directas
- No incluyas en ningun caso la extension .csv"""
        },
        "general": {
            "descripcion": "Vista GENERAL (análisis amplio)",
            "instrucciones": """Requisitos GENERALES:
- Maximo de 3 tablas con relaciones complejas si es necesario
- 5 columnas descriptivas por tabla
- Incluir metadatos contextuales
- Joins que permitan análisis multidimensional
- No incluyas en ningun caso la extension .csv"""
        }
    }
    
    reglas = reglas_especificas[tipo_vista]
    
    prompt = f"""
Eres un diseñador experto de vistas Denodo para análisis olímpicos. Necesito una vista de tipo '{tipo_vista.upper()}' con estos requisitos:

{reglas['instrucciones']}
- Usar alias de tablas siempre que se hagan joins
- Verificar que los nombres de columnas en condiciones de join existan en ambas tablas
- Especificar explícitamente 'teams' como tabla principal cuando se relacionen con coaches

Contexto del proyecto: {contexto}
Intereses principales del usuario: {intereses}

Base de conocimiento:
{relaciones}

Instrucciones técnicas:
1. Combina exactamente {max_tablas} tablas máximo
2. Máximo {max_columnas} columnas por tabla
3. Usa ALIAS claros para columnas (formato: tabla_columna)
4. Aplica mínimo 1 filtro relevante a los intereses
5. Usa solo LEFT join por predeterminado

Formato JSON requerido:
{{
  "view_name": "view_medallistas_{tipo_vista}_X",
  "tables": ["tabla1", "tabla2"],
  "joins": [
    {{
      "left_table": "tabla1", 
      "right_table": "tabla2",
      "join_type": "RIGHT",
      "condition": "tabla1.col = tabla2.col"
    }}
  ],
  "columns": [
    {{
      "table": "tabla1",
      "column": "col1",
      "alias": "alias_col1" 
    }}
  ],
  "filters": ["tabla1.col = 'valor'"],
  "description": "Descripción de 15 palabras máximo"
}}

Solo responde con el JSON válido, sin markdown ni texto adicional.
"""
    return prompt

def llamar_gemini(prompt):
    """
    Llama al modelo Gemini y devuelve la respuesta como un diccionario JSON.
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
    )

    respuesta_texto = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=generate_content_config,
    ):
        respuesta_texto += chunk.text

    # Eliminar backticks y texto adicional
    respuesta_texto = respuesta_texto.strip()
    if respuesta_texto.startswith("```json"):
        respuesta_texto = respuesta_texto[7:].strip()
    if respuesta_texto.endswith("```"):
        respuesta_texto = respuesta_texto[:-3].strip()

    try:
        resultado_json = json.loads(respuesta_texto)
    except Exception as e:
        raise ValueError(f"El chatbot no devolvió un JSON válido. Respuesta:\n{respuesta_texto}")

    return resultado_json

def generar_vql(sugerencia, max_tablas, max_columnas):
    """
    Genera el código VQL para la vista basada en la sugerencia del chatbot.
    """

    # Convertir todos los joins a LEFT por defecto para evitar resultados vacíos
    for join in sugerencia["joins"]:
        if join["join_type"] in ["INNER", "RIGHT"]:
            join["join_type"] = "LEFT"  # Forzar LEFT JOIN como seguro por defecto
    
    # Resto de validaciones...
    if len(sugerencia["tables"]) > max_tablas:
        raise ValueError(f"Máximo {max_tablas} tablas permitidas")
    
    # Contar columnas por tabla
    columnas_por_tabla = {}
    for col in sugerencia["columns"]:
        tabla = col["table"]
        columnas_por_tabla[tabla] = columnas_por_tabla.get(tabla, 0) + 1
    
    # Validar máximo de columnas por tabla
    for tabla, cantidad in columnas_por_tabla.items():
        if cantidad > max_columnas:
            raise ValueError(f"La tabla {tabla} tiene {cantidad} columnas (máximo permitido: {max_columnas})")
    
    # Resto del código original...
    view_name = sugerencia["view_name"]
    tables = sugerencia["tables"]
    joins = sugerencia["joins"]
    columns = sugerencia["columns"]
    description = sugerencia["description"]

    # Construir la parte SELECT
    select_cols = [f"{col['table']}.{col['column']} AS {col['alias']}" for col in columns]
    select_block = ",\n    ".join(select_cols)

    # Construir la parte FROM y JOINS
    from_block = f"FROM {tables[0]}"
    join_blocks = [f"{join['join_type']} JOIN {join['right_table']} ON {join['condition']}" for join in joins]
    joins_block = "\n".join(join_blocks)

    # Código VQL completo
    vql_script = f"""# Generated with Denodo Platform 9.1.3.

CREATE OR REPLACE VIEW {view_name} AS
SELECT 
    {select_block}
{from_block}
{joins_block};

# Descripción: {description}
"""
    # Construcción del script VQL...
    joins_block = "\n".join(
        f"{join['join_type']} JOIN {join['right_table']} ON {join['condition']}" 
        for join in sugerencia["joins"]
    )

    return vql_script

def construir_prompt_mejorado(relaciones, contexto, intereses, tipo_vista, max_tablas, max_columnas):
    """Versión mejorada del prompt con parámetros configurables"""
    prompt = f"""
Eres un experto en diseño de bases de datos y Denodo. Tengo una base de datos sobre los Juegos Olímpicos de 2024 con estas relaciones:

{relaciones}

Contexto: {contexto}
Intereses del usuario: {intereses}

Necesito una vista {tipo_vista} que combine hasta {max_tablas} tablas con máximo {max_columnas} columnas por tabla.

Requisitos:
- Usar solo joins necesarios
- Incluir solo columnas relevantes
- Nombre descriptivo para la vista
- Aplicar filtros según intereses
- Estructura JSON válida

El JSON debe tener:
{{
  "view_name": "nombre",
  "tables": ["tabla1", ...],
  "joins": [{{"left_table": "...", "right_table": "...", "join_type": "...", "condition": "..."}}],
  "columns": [{{"table": "...", "column": "...", "alias": "..."}}],
  "description": "..."
}}

Solo el JSON, sin comentarios.
"""
    return prompt

def generar_vista(relaciones, contexto, intereses, tipo_vista, numero, max_tablas, max_columnas):
    """Genera una vista individual basada en los parámetros"""
    try:
        prompt = construir_prompt(relaciones, contexto, intereses, tipo_vista, max_tablas, max_columnas)
        print(f"\nGenerando vista {tipo_vista} #{numero}...")
        sugerencia = llamar_gemini(prompt)
        
        # Validar estructura adicional
        if "filters" not in sugerencia:
            raise ValueError("Faltan filtros en la sugerencia")
            
        # Asegurar nombre único
        sugerencia["view_name"] = f"{sugerencia['view_name']}_{numero}"
        
        vql_script = generar_vql(sugerencia, max_tablas, max_columnas)
        vql_filename = os.path.join(OUTPUT_DIR, f"{sugerencia['view_name']}.vql")
        
        with open(vql_filename, "w", encoding="utf-8") as f:
            f.write(vql_script)
            
        print(f"¡Vista {tipo_vista} #{numero} generada! -> {vql_filename}")
        
    except Exception as e:
        print(f"Error generando vista {tipo_vista} #{numero}: {str(e)}")

def gestionar_vistas(relaciones):
    last_contexto = None
    last_intereses = None
    
    while True:
        print("\n\n=== Menú principal ===")
        print("(0) Empezar vistas nuevas")
        print("(1) Continuar creando vistas del último contexto")
        print("(2) Continuar creando vistas del último contexto con el mismo interés")
        print("(3) Subir todos los VQL generados")
        print("(4) Salir")
        
        try:
            opcion = int(input("\nSelecciona una opción: "))
        except ValueError:
            print("¡Error! Introduce un número válido.")
            continue
            
        if opcion == 4:
            print("Saliendo del programa...")
            break
            
        if opcion not in [0, 1, 2, 3]:
            print("Opción no válida. Inténtalo de nuevo.")
            continue
            
        # Gestionar contexto según la opción
        if opcion == 0:
            contexto = input("\nPor favor, proporciona el contexto de la base de datos: ")
            intereses = input("Por favor, proporciona tus intereses principales: ")
        elif opcion == 1:
            if not last_contexto:
                print("No hay contexto previo. Primero selecciona la opción 0.")
                continue
            contexto = last_contexto
            intereses = input("Por favor, proporciona los NUEVOS intereses principales: ")
        elif opcion == 2:
            if not last_contexto or not last_intereses:
                print("No hay contexto/intereses previos. Primero selecciona la opción 0.")
                continue
            contexto = last_contexto
            intereses = last_intereses
        elif opcion == 3:
            print("Subiendo todos los VQL generados...")
            # Se asume que el script que importa los VQL se llama "vql-import.py"
            subprocess.run(["python", "./scripts/vql-import.py"])
            continue
            
        # Actualizar últimos valores
        last_contexto = contexto
        last_intereses = intereses
        
        # Obtener cantidades de vistas
        print("\n¿Cuántas vistas ESPECÍFICAS deseas generar?")
        vistas_especificas = int(input("Número de vistas específicas: "))
        print("\n¿Cuántas vistas GENERALES deseas generar?")
        vistas_generales = int(input("Número de vistas generales: "))
        
        # Generar las vistas
        for i in range(1, vistas_especificas + 1):
            generar_vista(relaciones, contexto, intereses, "especifica", i, 2, 3)
        
        for i in range(1, vistas_generales + 1):
            generar_vista(relaciones, contexto, intereses, "general", i, 3, 5)

def main():
    """
    Función principal: lee relaciones y gestiona el menú
    """
    relaciones = leer_relaciones()
    gestionar_vistas(relaciones)

if __name__ == "__main__":
    main()