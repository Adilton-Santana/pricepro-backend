"""
Schemas Pydantic do PricePro

Exporta todos os schemas para fácil importação.
"""

from schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    PasswordChange,
    PasswordResetRequest,
    PasswordReset,
)
from schemas.auth import (
    Token,
    TokenData,
    RefreshTokenRequest,
    LoginResponse,
    PasswordResetTokenResponse,
)
from schemas.product import (
    SalesChannel,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from schemas.pricing import (
    PriceSimulationRequest,
    PriceCalculationResult,
    ProductPriceCalculation,
    ChannelPriceBreakdown,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "PasswordChange",
    "PasswordResetRequest",
    "PasswordReset",
    # Auth schemas
    "Token",
    "TokenData",
    "RefreshTokenRequest",
    "LoginResponse",
    "PasswordResetTokenResponse",
    # Product schemas
    "SalesChannel",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
    # Pricing schemas
    "PriceSimulationRequest",
    "PriceCalculationResult",
    "ProductPriceCalculation",
    "ChannelPriceBreakdown",
]
