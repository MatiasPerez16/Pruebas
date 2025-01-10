from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from core.config import settings

# Esquema OAuth2 para manejar tokens Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Genera un token JWT con la información proporcionada y un tiempo de expiración opcional.
    
    Args:
        data (dict): Datos que se incluirán en el token.
        expires_delta (timedelta, optional): Tiempo de expiración del token.
            Si no se proporciona, se usa el valor por defecto configurado.

    Returns:
        str: Token JWT firmado.
    """
    to_encode = data.copy()  # Copia los datos proporcionados
    # Determina la fecha de expiración del token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    # Agrega la fecha de expiración al contenido del token
    to_encode.update({"exp": expire})
    # Genera y firma el token con la clave secreta y el algoritmo configurado
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# Función para verificar y decodificar un token JWT
def verify_token(token: str):
    """
    Decodifica un token JWT y valida su contenido.
    
    Args:
        token (str): Token JWT a verificar.

    Returns:
        str: Nombre de usuario ("sub") extraído del token.

    Raises:
        HTTPException: Si el token no es válido o ha expirado.
    """
    try:
        # Decodifica el token usando la clave secreta y el algoritmo configurado
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")  # Extrae el campo "sub" del token
        # Verifica que el campo "sub" exista
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username  # Devuelve el usuario decodificado
    except JWTError:
        # Maneja errores en la decodificación del token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependencia para proteger endpoints con autenticación
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual a partir del token JWT proporcionado.

    Args:
        token (str): Token JWT extraído de la solicitud.

    Returns:
        str: Usuario autenticado.

    Raises:
        HTTPException: Si el token no es válido.
    """
    return verify_token(token)
