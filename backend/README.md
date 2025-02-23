# 📌 Documentación del Backend

## 📂 Descripción General
Este backend está desarrollado en **Flask** y proporciona un servicio REST para gestionar consultas y almacenamiento de conversaciones en una base de datos **SQLite**. Se conecta con un servicio de Denodo para obtener respuestas y almacena los mensajes en una tabla de historial.

---

## 🚀 **Instalación y Ejecución**

### **1️⃣ Requisitos Previos**
- Python 3.x
- Virtualenv (opcional pero recomendado)
- Dependencias listadas en `requirements.txt`

### **2️⃣ Instalación**
```bash
# Clonar el repositorio
cd backend

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### **4️⃣ Ejecución del Servidor**
```bash
python app.py
```
El servicio se ejecutará en `http://0.0.0.0:80/`.

---

## 📡 **Endpoints Disponibles**

### **1️⃣ Enviar Mensaje a Denodo (`POST /send`)**
#### **Descripción:**
Permite enviar una pregunta a Denodo y almacena la respuesta en la base de datos.

#### **Solicitud:**
```json
{
  "chat_id": "123",
  "message": "¿Quién ganó las Olimpiadas 2024?"
}
```

#### **Respuesta:**
```json
{
  "chat_id": "123",
  "pregunta": "¿Quién ganó las Olimpiadas 2024?",
  "respuesta": "El país ganador fue..."
}
```

---

### **2️⃣ Obtener Historial de un Chat (`GET /history/<chat_id>`)**
#### **Descripción:**
Recupera el historial de mensajes asociados a un `chat_id` específico.

#### **Ejemplo de Solicitud:**
```bash
curl -X GET http://localhost/history/123
```

#### **Ejemplo de Respuesta:**
```json
{
  "chat_id": "123",
  "mensajes": [
    {
      "msg_id": 1,
      "pregunta": "¿Quién ganó las Olimpiadas 2024?",
      "respuesta": "El país ganador fue...",
      "timestamp": "2025-02-23 12:34:56"
    }
  ]
}
```

---

### **3️⃣ Obtener Lista de Chats Disponibles (`GET /chats`)**
#### **Descripción:**
Obtiene una lista de todos los `chat_id` disponibles en la base de datos.

#### **Ejemplo de Solicitud:**
```bash
curl -X GET http://localhost/chats
```

#### **Ejemplo de Respuesta:**
```json
{
  "chats": ["123", "456", "789"]
}
```

---

## 🛠 **Detalles Técnicos**

### **1️⃣ Base de Datos SQLite**
El backend utiliza una base de datos **SQLite** para almacenar el historial de chats. La base de datos se encuentra en `data/history.db`.

#### **Estructura de la Tabla `chat_history`**
```sql
CREATE TABLE chat_history (
    chat_id TEXT NOT NULL,
    msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **2️⃣ Conexión con Denodo**
El backend realiza peticiones al servicio **Denodo** utilizando autenticación básica y parámetros específicos para la consulta.

```python
response = requests.get(
    DENODO_URL,
    params=params,
    auth=DENODO_AUTH,
    headers={"Accept": "application/json"},
)
```

Los parámetros enviados incluyen información sobre la consulta y la base de datos `jjoo`.

---

## 🔥 **Manejo de Errores**
- Se valida que los parámetros sean correctos antes de procesar las solicitudes.
- Si una solicitud a Denodo falla, se captura el error y se devuelve un código de error `500`.
- Si la base de datos tiene un problema, se captura la excepción y se devuelve una respuesta con el error.

---
