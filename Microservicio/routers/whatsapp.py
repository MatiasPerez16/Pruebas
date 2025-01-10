from fastapi import APIRouter, HTTPException, Depends
from core.security import get_current_user
from pydantic import BaseModel
from services.whatsapp.send_template_message import send_template_message
from services.whatsapp.send_free_message import send_free_message

# Instancia del router para las rutas relacionadas con WhatsApp
whatsapp_router = APIRouter()

# Modelo de datos para enviar mensajes basados en plantillas
class WhatsAppTemplateMessage(BaseModel):
    to: str  # Número de teléfono del destinatario en formato internacional
    template_name: str  # Nombre de la plantilla a utilizar
    language_code: str  # Código del idioma para la plantilla (e.g., "en_US")

# Modelo de datos para enviar mensajes de texto libre
class WhatsAppFreeMessage(BaseModel):
    to: str  # Número de teléfono del destinatario en formato internacional
    text: str  # Contenido del mensaje de texto libre

# Ruta para enviar mensajes basados en plantillas
@whatsapp_router.post("/send-template-message/")
async def send_template_message_route(
    message: WhatsAppTemplateMessage,  # Datos del mensaje basados en el modelo WhatsAppTemplateMessage
    current_user: str = Depends(get_current_user)  # Dependencia para autenticar al usuario actual
):
    # Llama a la función que interactúa con la API de WhatsApp para enviar el mensaje
    response = await send_template_message(
        to=message.to,
        template_name=message.template_name,
        language_code=message.language_code
    )
    # Verifica la respuesta de la API y devuelve un mensaje de éxito o un error
    if response.status_code == 200:
        return {"status": "Template message sent successfully", "response": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

# Ruta para enviar mensajes de texto libre
@whatsapp_router.post("/send-free-message/")
async def send_free_message_route(
    message: WhatsAppFreeMessage,  # Datos del mensaje basados en el modelo WhatsAppFreeMessage
    current_user: str = Depends(get_current_user)  # Dependencia para autenticar al usuario actual
):
    # Llama a la función que interactúa con la API de WhatsApp para enviar el mensaje
    response = await send_free_message(
        to=message.to,
        text=message.text
    )
    # Verifica la respuesta de la API y devuelve un mensaje de éxito o un error
    if response.status_code == 200:
        return {"status": "Free message sent successfully", "response": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
