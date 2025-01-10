import httpx
from core.config import settings

# Función asíncrona para enviar un mensaje basado en una plantilla de WhatsApp
async def send_template_message(to: str, template_name: str, language_code: str):
    # Configura los encabezados necesarios para la autenticación y el formato del contenido
    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",  # Token de acceso desde el archivo .env
        "Content-Type": "application/json"  # Especifica que el contenido es JSON
    }

    # Define el cuerpo del mensaje en el formato requerido por la API para enviar plantillas
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Número de teléfono del destinatario en formato internacional
        "type": "template",
        "template": {
            "name": template_name,  # Nombre de la plantilla definida en la API de WhatsApp
            "language": {
                "code": language_code  # Código del idioma de la plantilla (ej., "en_US" o "es_ES")
            }
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
