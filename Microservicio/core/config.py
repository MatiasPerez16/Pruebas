from pydantic import BaseSettings

# Clase para gestionar la configuración del microservicio
class Settings(BaseSettings):
    meta_access_token: str  # Token de acceso para interactuar con la API de WhatsApp
    phone_number_id: str  # ID del número de teléfono registrado en la API de WhatsApp
    whatsapp_api_url: str  # URL base de la API de WhatsApp
    secret_key: str  # Clave secreta utilizada para firmar los tokens JWT
    algorithm: str  # Algoritmo usado para firmar y verificar los tokens JWT
    access_token_expire_minutes: int  # Tiempo de expiración de los tokens de acceso (en minutos)

    # Configuración para cargar las variables desde un archivo .env
    class Config:
        env_file = ".env"  # Indica que las variables se cargarán desde un archivo .env

# Instancia de la configuración, accesible en todo el microservicio
settings = Settings()
