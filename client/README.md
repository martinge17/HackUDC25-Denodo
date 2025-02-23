# Estructura del client para el chatbot generador de views
Todos los scripts se encuentran en el directorio client/scripts:

## chatbot-vql.py

Script interactivo que genera vistas en Denodo.
Construye prompts personalizados (con distintos requisitos según el tipo de vista: específica o general) y llama al modelo Gemini para obtener una sugerencia en JSON que luego se valida y transforma en código VQL.

## databaseRelations-generator.py

Lee archivos CSV desde un directorio (por defecto ./jjoo) para extraer metadatos y relaciones entre ellos.
Genera un reporte formateado de relaciones significativas, útil para entender la estructura de la base de datos.

## description-generator.py

Procesa archivos CSV para extraer una muestra (cabecera y algunas filas).
Utiliza Google GenAI para inferir el tipo y la descripción de las columnas, generando un JSON.
A partir de este JSON, construye un script VQL que define una datasource, un wrapper y una tabla en Denodo con descripciones inline.

## vql-import.py

Automatiza la importación de los archivos VQL generados (almacenados en ./vql_output) a Denodo Design Studio.
Utiliza Selenium para iniciar sesión, navegar por el menú de importación y subir cada archivo VQL de forma secuencial.

# Requisitos y Dependencias

```
cd client
python3 -m venv venv_parser
source venv_parser/bin/activate
pip install -r requirements.txt
```

# Configuración y Uso
1. Generación de Relaciones entre CSV
Utiliza el script databaseRelations-generator.py para analizar los archivos CSV y obtener un reporte de las relaciones entre ellos.
```
python client/scripts/databaseRelations-generator.py <directorio_csv>
```
Parámetro:
<directorio_csv>: Ruta al directorio que contiene los archivos CSV (por defecto, se usa ./jjoo en otros scripts).
3. Generación Interactiva de Vistas con Chatbot
Ejecuta chatbot-vql.py para iniciar el proceso interactivo de generación de vistas:

```
python client/scripts/chatbot-vql.py
```
Durante la ejecución se te solicitará:

Proveer el contexto de la base de datos.
Indicar los intereses principales del usuario.
Elegir cuántas vistas específicas y generales deseas generar.
El script generará archivos VQL en el directorio ./vql_output.

3. Generación de Scripts VQL desde CSV
Con description-generator.py puedes procesar cada archivo CSV para:

Obtener una muestra de datos (cabecera y filas de ejemplo).
Construir un prompt para inferir tipos de datos y descripciones de columnas.
Generar un script VQL que define la datasource, wrapper y tabla en Denodo.
```
python client/scripts/description-generator.py
```
Cada archivo VQL generado se guardará en ./vql_output.

4. Importación Automática de VQL a Denodo
Una vez generados los archivos VQL, utiliza vql-import.py para automatizar la importación en Denodo Design Studio.
