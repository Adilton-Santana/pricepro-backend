"""
Módulo de Segurança

Responsável por:
- Hash e verificação de senhas usando bcrypt
- Funções auxiliares de segurança
- Validação de força de senha
"""

from passlib.context import CryptContext
import re
from typing import Tuple

# Contexto para hash de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Gera um hash seguro da senha usando bcrypt.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash armazenado no banco
        
    Returns:
        True se a senha está correta, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Valida a força da senha baseado em critérios de segurança.
    
    Critérios:
    - Mínimo de 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    
    Args:
        password: Senha a ser validada
        
    Returns:
        Tupla (is_valid, message)
    """
    if len(password) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres"
    
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    
    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "A senha deve conter pelo menos um caractere especial"
    
    return True, "Senha válida"
