"""
Schemas Pydantic para Produto

Define os schemas de validação de dados para operações com produtos:
- Criação de produto
- Atualização de produto
- Resposta de produto
- Canal de venda
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SalesChannel(BaseModel):
    """
    Schema para canal de venda.
    
    Representa um canal de venda com sua taxa associada.
    Exemplo: Loja Física (0%), Marketplace (15%), E-commerce Próprio (5%)
    """
    channel: str = Field(..., min_length=1, max_length=100, description="Nome do canal de venda")
    fee_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Taxa percentual do canal (0-100)"
    )


class ProductBase(BaseModel):
    """
    Schema base para Produto com campos comuns.
    """
    name: str = Field(..., min_length=1, max_length=255, description="Nome do produto")
    category: Optional[str] = Field(None, max_length=100, description="Categoria do produto")
    description: Optional[str] = Field(None, description="Descrição detalhada")
    
    # Custos
    cost_price: float = Field(..., gt=0, description="Custo de produção ou compra")
    tax_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Percentual de impostos (0-100)"
    )
    variable_costs: float = Field(
        default=0.0,
        ge=0,
        description="Despesas variáveis por unidade"
    )
    fixed_costs_allocated: float = Field(
        default=0.0,
        ge=0,
        description="Despesas fixas rateadas para este produto"
    )
    
    # Canais e taxas
    sales_channels: Optional[List[SalesChannel]] = Field(
        default=None,
        description="Lista de canais de venda com suas taxas"
    )
    additional_fees: float = Field(
        default=0.0,
        ge=0,
        description="Taxas adicionais (maquininha, embalagem, etc.)"
    )
    
    # Margem
    desired_margin_percentage: float = Field(
        default=30.0,
        ge=0,
        le=1000,
        description="Margem de lucro desejada em % (0-1000)"
    )


class ProductCreate(ProductBase):
    """
    Schema para criação de produto.
    Herda todos os campos do ProductBase.
    """
    pass


class ProductUpdate(BaseModel):
    """
    Schema para atualização de produto.
    Todos os campos são opcionais.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    cost_price: Optional[float] = Field(None, gt=0)
    tax_percentage: Optional[float] = Field(None, ge=0, le=100)
    variable_costs: Optional[float] = Field(None, ge=0)
    fixed_costs_allocated: Optional[float] = Field(None, ge=0)
    sales_channels: Optional[List[SalesChannel]] = None
    additional_fees: Optional[float] = Field(None, ge=0)
    desired_margin_percentage: Optional[float] = Field(None, ge=0, le=1000)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """
    Schema de resposta para Produto.
    Inclui campos adicionais como ID, user_id e timestamps.
    """
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class ProductListResponse(BaseModel):
    """
    Schema de resposta para lista de produtos com paginação.
    """
    total: int
    page: int
    page_size: int
    products: List[ProductResponse]
