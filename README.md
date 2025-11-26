# 🌱 Gestión de Riego Automatizado

Backend desarrollado en **Django + Django REST Framework** para gestionar un sistema de riego automatizado basado en sensores, zonas, válvulas y programación de riegos. Incluye autenticación, documentación automática y endpoints para administración del sistema.

---

## 🚀 Características principales

* **Autenticación JWT** (inicio de sesión seguro para usuarios).
* **API REST completa** para:

  * Gestión de zonas de riego.
  * Gestión de sensores.
  * Programación de riegos automatizados.
  * Válvulas y dispositivos.
  * Historial de riegos y logs del sistema.
* **Documentación automática** con Swagger .
* **Base de datos relacional**  MySQL .
* Arquitectura escalable y organizada: `services`, `serializers`, `views`, `models`.

---

## 🛠️ Tecnologías utilizadas

* **Python 3.12+**
* **Django 5**
* **Django REST Framework**
* **drf-yasg** (Swagger)
* **MySQL**
* ** pip**

---

## 📦 Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/gho0sth05/Gesti-n-Riego-Automatizado.git
cd Gesti-n-Riego-Automatizado
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz:

```
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
```

Si usas PostgreSQL:

```
DATABASE_URL=postgres://usuario:password@localhost:5432/riego_db
```

### 5️⃣ Aplicar migraciones

```bash
python manage.py migrate
```

### 6️⃣ Crear usuario administrador

```bash
python manage.py createsuperuser
```

### 7️⃣ Ejecutar servidor

```bash
python manage.py runserver
```


## 🧩 Estructura del proyecto

```
Gestión-Riego-Automatizado/
│
├── riego/                # App principal
│   ├── models.py         # Modelos de sensores, zonas, válvulas, riegos
│   ├── serializers.py    # Serializadores de DRF
│   ├── views.py          # Endpoints del API
│   ├── urls.py           # Rutas de la app
│   ├── services/         # Lógica de negocio
│   └── admin.py          # Panel administrativo
│
├── GestionRiego/         # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔐 Autenticación (JWT)

### Obtener token:

POST → `/api/token/`

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

### Actualizar token:

POST → `/api/token/refresh/`

---

## 📡 Endpoints principales

| Recurso  | Método     | URL                  | Descripción           |
| -------- | ---------- | -------------------- | --------------------- |
| Zonas    | GET/POST   | `/api/zonas/`        | Listar o crear        |
| Zonas    | PUT/DELETE | `/api/zonas/<id>/`   | Actualizar o eliminar |
| Sensores | GET        | `/api/sensores/`     | Sensores instalados   |
| Riegos   | POST       | `/api/programacion/` | Crear programación    |
| Válvulas | GET        | `/api/valvulas/`     | Estado de válvulas    |
| Logs     | GET        | `/api/logs/`         | Historial del sistema |

---

## 🧪 Tests

```bash
python manage.py test
```

---

## 👤 Autores

**Jeonardo Perche**
**Beicker Tapia**
**Karen Gonzalez**

---
