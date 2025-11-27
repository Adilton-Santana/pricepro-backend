"""
Schemas Pydantic para Motor de Precificação

Define os schemas de validação de dados para operações de precificação:
- Simulação de preço
- Resultado de cálculo de preços
- Break-even analysis
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from schemas.product import SalesChannel


class PriceSimulationRequest(BaseModel):
    """
    Schema para solicitação de simulação de preço.
    
    Permite que o usuário simule preços sem precisar criar um produto.
    """
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
        description="Despesas fixas rateadas"
    )
    
    # Canais e taxas
    sales_channels: Optional[List[SalesChannel]] = Field(
        default=None,
        description="Lista de canais de venda com suas taxas"
    )
    additional_fees: float = Field(
        default=0.0,
        ge=0,
        description="Taxas adicionais"
    )
    
    # Margem
    desired_margin_percentage: float = Field(
        default=30.0,
        ge=0,
        le=1000,
        description="Margem de lucro desejada em %"
    )
    
    # Fator premium (para preço premium)
    premium_factor: float = Field(
        default=1.3,
        ge=1.0,
        le=10.0,
        description="Fator multiplicador para preço premium (ex: 1.3 = +30%)"
    )


class ChannelPriceBreakdown(BaseModel):
    """
    Schema para breakdown de preço por canal de venda.
    """
    channel: str
    fee_percentage: float
    minimum_price: float
    ideal_price: float
    premium_price: float
    profit_per_unit_ideal: float


class PriceCalculationResult(BaseModel):
    """
    Schema de resposta para cálculo de preços.
    
    Retorna três preços calculados:
    - Preço Mínimo: cobre todos os custos, margem zero
    - Preço Ideal: inclui a margem desejada
    - Preço Premium: preço ideal com fator multiplicador extra
    
    Também inclui análise de lucro e break-even.
    """
    # Preços calculados (sem canal específico)
    minimum_price: float = Field(..., description="Preço mínimo (cobre todos os custos)")
    ideal_price: float = Field(..., description="Preço ideal (inclui margem desejada)")
    premium_price: float = Field(..., description="Preço premium (ideal + fator extra)")
    
    # Análise de lucro
    profit_per_unit_minimum: float = Field(..., description="Lucro por unidade no preço mínimo")
    profit_per_unit_ideal: float = Field(..., description="Lucro por unidade no preço ideal")
    profit_per_unit_premium: float = Field(..., description="Lucro por unidade no preço premium")
    
    # Break-even (apenas despesas fixas)
    break_even_units: Optional[float] = Field(
        None,
        description="Unidades necessárias para cobrir despesas fixas (break-even)"
    )
    
    # Breakdown por canal (se aplicável)
    channel_breakdown: Optional[List[ChannelPriceBreakdown]] = Field(
        None,
        description="Breakdown de preços por canal de venda"
    )
    
    # Detalhamento dos custos
    cost_breakdown: Dict[str, float] = Field(
        ...,
        description="Detalhamento dos custos considerados no cálculo"
    )


class ProductPriceCalculation(BaseModel):
    """
    Schema para cálculo de preço de um produto existente.
    """
    product_id: int = Field(..., description="ID do produto")
    premium_factor: float = Field(
        default=1.3,
        ge=1.0,
        le=10.0,
        description="Fator multiplicador para preço premium"
    )
