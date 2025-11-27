"""
Módulo de Gerenciamento de JWT (JSON Web Tokens)

Responsável por:
- Criação de access tokens e refresh tokens
- Decodificação e validação de tokens
- Extração de informações do payload
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt
from .config import settings
import uuid


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso.
    
    Args:
        data: Dados a serem incluídos no payload do token (user_id, email, role, etc.)
        expires_delta: Tempo de expiração customizado (opcional)
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona informações ao payload
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    # Codifica o token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Cria um token JWT de refresh.
    
    Args:
        data: Dados a serem incluídos no payload do token (user_id)
        
    Returns:
        Token JWT de refresh codificado
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração (7 dias)
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Adiciona informações ao payload
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
        "jti": str(uuid.uuid4())  # ID único do token
    })
    
    # Codifica o token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_password_reset_token(email: str) -> str:
    """
    Cria um token JWT para recuperação de senha.
    
    Args:
        email: Email do usuário
        
    Returns:
        Token JWT para reset de senha
    """
    expire = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    
    to_encode = {
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "password_reset"
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict]:
    """
    Decodifica e valida um token JWT.
    
    Args:
        token: Token JWT a ser decodificado
        
    Returns:
        Payload do token se válido, None se inválido
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token_type(payload: Dict, expected_type: str) -> bool:
    """
    Verifica se o tipo do token corresponde ao esperado.
    
    Args:
        payload: Payload decodificado do token
        expected_type: Tipo esperado ("access", "refresh", "password_reset")
        
    Returns:
        True se o tipo é correto, False caso contrário
    """
    return payload.get("type") == expected_type
