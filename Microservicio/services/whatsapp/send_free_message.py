import httpx
from core.config import settings

# Función asíncrona para enviar un mensaje de texto libre a través de la API de WhatsApp
async def send_free_message(to: str, text: str):
    # Configura los encabezados necesarios para la autenticación y el formato del contenido
    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",  # Token de acceso desde el archivo .env
        "Content-Type": "application/json"  # Especifica que el contenido es JSON
    }

    # Define el cuerpo del mensaje en el formato requerido por la API de WhatsApp
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Número de teléfono del destinatario en formato internacional
        "type": "text",
        "text": {
            "body": text  # Contenido del mensaje
        }
    }

    # Realiza una solicitud POST utilizando un cliente asíncrono de HTTPX
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.whatsapp_api_url}/{settings.phone_number_id}/messages",  # URL del endpoint de mensajes
            headers=headers,  # Encabezados de la solicitud
            json=payload  # Datos en formato JSON
        )

    # Retorna la respuesta de la API para su procesamiento posterior
    return response
