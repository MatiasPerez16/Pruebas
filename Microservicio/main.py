from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from routers.whatsapp import whatsapp_router
from routers.webhook import webhook_router
from routers.auth import auth_router
from core.config import settings
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from core.security import get_current_user

# Inicializa la instancia del microservicio usando FastAPI
app = FastAPI(
    title="Adherencia de Pacientes",
    description="API para manejar mensajes y webhooks relacionados con WhatsApp.",
    version="1.0.0",
)

# Incluye el router de autenticación bajo el prefijo "/auth".
# Este router proporciona los endpoints necesarios para autenticación y generación de tokens.
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Incluye el router para manejar mensajes, asegurando que los endpoints estén protegidos por autenticación.
app.include_router(
    whatsapp_router,
    prefix="/whatsapp",
    tags=["whatsapp"],
    dependencies=[Depends(get_current_user)],  # Aplica la dependencia para validar el token
)

# Incluye el router para manejar los webhooks, también protegido por autenticación.
app.include_router(
    webhook_router,
    prefix="/webhook",
    tags=["Webhook"],
    dependencies=[Depends(get_current_user)],  # Aplica la dependencia para validar el token
)

# Define un manejador de excepciones generales para capturar errores no controlados
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    # Devuelve una respuesta JSON con un mensaje de error interno y código 500
    return JSONResponse(
        status_code=500,
        content={"message": f"Error interno: {str(exc)}"}
    )

# Configura y ejecuta el servidor utilizando Hypercorn
async def run_server():
    """
    Configura y lanza el servidor con Hypercorn.
    """
    # Muestra en consola las variables de configuración cargadas desde el archivo .env
    print("Configuración cargada:")
    print(f"META_ACCESS_TOKEN: {settings.meta_access_token}")
    print(f"PHONE_NUMBER_ID: {settings.phone_number_id}")
    print(f"WHATSAPP_API_URL: {settings.whatsapp_api_url}")

    # Configura el servidor para escuchar en localhost:8000
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    # Ejecuta el servidor con la configuración especificada
    await serve(app, config)

# Ejecuta el servidor solo si este archivo es ejecutado directamente
if __name__ == "__main__":
    asyncio.run(run_server())
