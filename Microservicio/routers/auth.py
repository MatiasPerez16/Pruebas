from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import timedelta
from core.security import create_access_token

auth_router = APIRouter()

# Modelo para credenciales de usuario
class UserCredentials(BaseModel):
    username: str
    password: str

# Usuarios simulados 
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "testpassword",  # En producción, usa un hash
    }
}

@auth_router.post("/token")
async def login_for_access_token(credentials: UserCredentials):
    user = fake_users_db.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear un token de acceso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": credentials.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
