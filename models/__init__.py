"""
Models do PricePro

Exporta todos os models SQLAlchemy para fácil importação.
"""

from models.user import User, UserRole
from models.product import Product
from models.ai_suggestion import AISuggestion

__all__ = [
    "User",
    "UserRole",
    "Product",
    "AISuggestion",
]
