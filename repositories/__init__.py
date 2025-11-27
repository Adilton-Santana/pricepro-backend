"""
Repositories do PricePro

Exporta todos os repositories para fácil importação.
"""

from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

__all__ = [
    "UserRepository",
    "ProductRepository",
]
