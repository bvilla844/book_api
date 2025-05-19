# FastAPI Auth API

Esta es una API desarrollada con FastAPI que incluye autenticación de usuarios con verificación por correo electrónico, tokens JWT (access y refresh), y envío de correos electrónicos usando Celery y un broker como Redis.

## 🚀 Características principales

- Registro de usuario (`/api/v1/auth/signup`)
- Verificación por correo (`/api/v1/auth/verify/{token}`)
- Login con tokens JWT (`/api/v1/auth/login`)
- Envío de correos con Celery y tareas en segundo plano (`send_email`)
- Tokens seguros con expiración y soporte para refresh tokens
- Estructura modular con routers, servicios y esquemas
- Base de datos asíncrona usando SQLAlchemy con `AsyncSession`

---

## 🛠️ Despliegue en Render

### 1. Crear un nuevo servicio **Web Service** en [https://dashboard.render.com](https://dashboard.render.com)

### 2. Configuración del repositorio
- Selecciona el repositorio donde tienes esta API.
- Elige **Python** como entorno de ejecución.
- Agrega el siguiente comando de inicio:

