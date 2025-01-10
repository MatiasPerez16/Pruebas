from fastapi import APIRouter, HTTPException, Request, Depends
from core.security import get_current_user
from services.webhook.process_webhook_data import process_webhook_data

# Instancia del router para las rutas relacionadas con los webhooks
webhook_router = APIRouter()

# Ruta para recibir eventos enviados desde el webhook
@webhook_router.post("/")
async def receive_webhook(
    request: Request,  # Objeto de solicitud que contiene los datos enviados por el webhook
    current_user: str = Depends(get_current_user)  # Dependencia para autenticar al usuario actual
):
    """
    Endpoint para recibir y procesar eventos del webhook de Meta.
    """
    try:
        # Extrae el contenido JSON de la solicitud
        data = await request.json()
        # Procesa los datos del webhook utilizando la función correspondiente
        result = await process_webhook_data(data)
        return result
    except Exception as e:
        # Maneja errores al procesar los datos del webhook
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")
