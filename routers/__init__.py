"""
Routers do PricePro

Exporta todos os routers para fácil importação.
"""

from routers import auth, users, products, simulation, ai

__all__ = [
    "auth",
    "users",
    "products",
    "simulation",
    "ai",
]
