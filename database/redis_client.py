"""
Cliente Redis para Cache e Rate Limiting

Responsável por:
- Gerenciar conexão com Redis
- Fornecer funções para cache
- Implementar rate limiting por usuário
- Gerenciar sessões de refresh tokens

NOTA: Se Redis não estiver disponível, usa cache em memória (modo degradado)
"""

import redis
from typing import Optional, Dict, Any
from core.config import settings
import json
import time
from datetime import datetime, timedelta


class InMemoryCache:
    """
    Cache em memória simples para quando Redis não está disponível.
    NÃO usar em produção com múltiplos workers!
    """
    
    def __init__(self):
        self._cache: Dict[str, tuple[Any, float]] = {}
    
    def set(self, key: str, value: Any, expire: int):
        """Salva no cache com expiração."""
        expires_at = time.time() + expire
        self._cache[key] = (value, expires_at)
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera do cache."""
        if key not in self._cache:
            return None
        
        value, expires_at = self._cache[key]
        
        # Verifica se expirou
        if time.time() > expires_at:
            del self._cache[key]
            return None
        
        return value
    
    def delete(self, key: str):
        """Remove do cache."""
        if key in self._cache:
            del self._cache[key]
    
    def exists(self, key: str) -> bool:
        """Verifica se existe."""
        return self.get(key) is not None
    
    def incr(self, key: str) -> int:
        """Incrementa contador."""
        current = self.get(key)
        if current is None:
            current = 0
        new_value = int(current) + 1
        # Se é a primeira vez, define expiração de 1 minuto
        if current == 0:
            self.set(key, new_value, 60)
        else:
            # Mantém a expiração existente
            _, expires_at = self._cache.get(key, (None, time.time() + 60))
            self._cache[key] = (new_value, expires_at)
        return new_value


class RedisClient:
    """
    Cliente singleton para gerenciar conexões Redis.
    Fallback para InMemoryCache se Redis não estiver disponível.
    """
    
    _instance = None
    _redis = None
    _use_memory_cache = False
    _memory_cache = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            try:
                # Tenta conectar ao Redis
                cls._redis = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                # Testa a conexão
                cls._redis.ping()
                print("✅ Redis conectado com sucesso!")
            except Exception as e:
                print(f"⚠️  Redis não disponível ({str(e)}). Usando cache em memória.")
                cls._use_memory_cache = True
                cls._memory_cache = InMemoryCache()
        return cls._instance
    
    def get_client(self):
        """Retorna o cliente Redis ou cache em memória."""
        if self._use_memory_cache:
            return self._memory_cache
        return self._redis
    
    def ping(self) -> bool:
        """Testa a conexão com o Redis."""
        if self._use_memory_cache:
            return True  # Cache em memória sempre "funciona"
        try:
            return self._redis.ping()
        except:
            return False
    
    # ============= Rate Limiting =============
    
    def check_rate_limit(self, user_id: int) -> bool:
        """
        Verifica se o usuário excedeu o limite de requisições.
        
        Implementa um rate limit de 200 requisições por minuto.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se ainda pode fazer requisições, False se excedeu o limite
        """
        key = f"rate_limit:user:{user_id}"
        
        if self._use_memory_cache:
            # Usa cache em memória
            current = self._memory_cache.incr(key)
            return current <= settings.RATE_LIMIT_REQUESTS
        else:
            # Usa Redis
            current = self._redis.incr(key)
            
            # Se é a primeira requisição, define o TTL
            if current == 1:
                self._redis.expire(key, settings.RATE_LIMIT_WINDOW)
            
            # Verifica se excedeu o limite
            return current <= settings.RATE_LIMIT_REQUESTS
    
    def get_rate_limit_remaining(self, user_id: int) -> int:
        """
        Retorna quantas requisições restam para o usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Número de requisições restantes
        """
        key = f"rate_limit:user:{user_id}"
        
        if self._use_memory_cache:
            current = self._memory_cache.get(key)
        else:
            current = self._redis.get(key)
        
        if current is None:
            return settings.RATE_LIMIT_REQUESTS
        
        remaining = settings.RATE_LIMIT_REQUESTS - int(current)
        return max(0, remaining)
    
    # ============= Session Management =============
    
    def save_refresh_token(self, user_id: int, token_jti: str, expires_in: int):
        """
        Salva o JTI do refresh token para validação.
        
        Args:
            user_id: ID do usuário
            token_jti: ID único do token (claim 'jti')
            expires_in: Tempo de expiração em segundos
        """
        key = f"refresh_token:{user_id}:{token_jti}"
        
        if self._use_memory_cache:
            self._memory_cache.set(key, "valid", expires_in)
        else:
            self._redis.setex(key, expires_in, "valid")
    
    def is_refresh_token_valid(self, user_id: int, token_jti: str) -> bool:
        """
        Verifica se um refresh token é válido.
        
        Args:
            user_id: ID do usuário
            token_jti: ID único do token
            
        Returns:
            True se o token é válido, False caso contrário
        """
        key = f"refresh_token:{user_id}:{token_jti}"
        
        if self._use_memory_cache:
            return self._memory_cache.exists(key)
        else:
            return self._redis.exists(key) > 0
    
    def invalidate_refresh_token(self, user_id: int, token_jti: str):
        """
        Invalida um refresh token (usado no logout).
        
        Args:
            user_id: ID do usuário
            token_jti: ID único do token
        """
        key = f"refresh_token:{user_id}:{token_jti}"
        
        if self._use_memory_cache:
            self._memory_cache.delete(key)
        else:
            self._redis.delete(key)
    
    # ============= Cache Genérico =============
    
    def set_cache(self, key: str, value: any, expire: int = 300):
        """
        Salva um valor no cache.
        
        Args:
            key: Chave do cache
            value: Valor a ser armazenado (será serializado como JSON)
            expire: Tempo de expiração em segundos (padrão: 5 minutos)
        """
        if self._use_memory_cache:
            self._memory_cache.set(key, json.dumps(value), expire)
        else:
            self._redis.setex(key, expire, json.dumps(value))
    
    def get_cache(self, key: str) -> Optional[any]:
        """
        Recupera um valor do cache.
        
        Args:
            key: Chave do cache
            
        Returns:
            Valor deserializado ou None se não existir
        """
        if self._use_memory_cache:
            value = self._memory_cache.get(key)
        else:
            value = self._redis.get(key)
        
        if value:
            return json.loads(value)
        return None
    
    def delete_cache(self, key: str):
        """
        Remove um valor do cache.
        
        Args:
            key: Chave do cache
        """
        if self._use_memory_cache:
            self._memory_cache.delete(key)
        else:
            self._redis.delete(key)


# Instância global do cliente Redis
redis_client = RedisClient()
