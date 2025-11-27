"""
Schemas para Requisições e Respostas da IA
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class AIAnalysisRequest(BaseModel):
    """
    Schema para requisição de análise de IA.
    
    Pode ser enviado um product_id OU dados manuais.
    """
    # Opção 1: Usar produto existente
    product_id: Optional[int] = Field(None, description="ID do produto a ser analisado")
    
    # Opção 2: Dados manuais
    product_name: Optional[str] = Field(None, max_length=255, description="Nome do produto")
    category: Optional[str] = Field(None, max_length=100, description="Categoria do produto")
    production_cost: Optional[float] = Field(None, ge=0, description="Custo de produção")
    fixed_expenses: Optional[float] = Field(None, ge=0, description="Despesas fixas")
    variable_expenses: Optional[float] = Field(None, ge=0, description="Despesas variáveis")
    taxes: Optional[float] = Field(None, ge=0, description="Impostos")
    marketplace_fee: Optional[float] = Field(None, ge=0, description="Taxa de marketplace")
    payment_fee: Optional[float] = Field(None, ge=0, description="Taxa de pagamento")
    shipping_fee: Optional[float] = Field(0, ge=0, description="Frete")
    advertising_fee: Optional[float] = Field(0, ge=0, description="Taxa de publicidade")
    
    # Parâmetros da análise
    user_goal: str = Field(
        "Equilibrar lucratividade e competitividade",
        max_length=500,
        description="Objetivo do empreendedor"
    )
    desired_margin: float = Field(
        30.0,
        ge=0,
        le=1000,
        description="Margem de lucro desejada (%)"
    )
    
    @field_validator('product_name', 'category', mode='after')
    @classmethod
    def validate_manual_data(cls, v, info):
        """Valida que dados manuais estão completos se product_id não for fornecido"""
        if info.data.get('product_id') is None:
            if info.field_name in ['product_name', 'category'] and not v:
                raise ValueError(f"{info.field_name} é obrigatório quando product_id não é fornecido")
        return v
    
    class Config:
        json_json_schema_extra = {
            "example": {
                "product_id": 1,
                "user_goal": "Maximizar lucro mantendo competitividade",
                "desired_margin": 35.0
            }
        }


class SensitivityPoint(BaseModel):
    """Ponto de sensibilidade preço x lucro"""
    preco: float = Field(..., description="Preço do produto")
    lucro: float = Field(..., description="Lucro por unidade")
    margem: float = Field(..., description="Margem de lucro (%)")


class AIAnalysisResponse(BaseModel):
    """
    Schema para resposta da análise de IA.
    """
    # Recomendações principais
    preco_recomendado: float = Field(..., description="Preço recomendado")
    margem_recomendada: float = Field(..., description="Margem recomendada (%)")
    preco_minimo: Optional[float] = Field(None, description="Preço mínimo sugerido")
    preco_premium: Optional[float] = Field(None, description="Preço premium sugerido")
    
    # Análises
    insights: List[str] = Field(..., description="Lista de insights")
    riscos: List[str] = Field(..., description="Lista de riscos identificados")
    oportunidades: List[str] = Field(..., description="Lista de oportunidades")
    
    # Estratégia
    estrategia_sugerida: str = Field(..., description="Estratégia comercial sugerida")
    resumo_executivo: str = Field(..., description="Resumo executivo da análise")
    
    # Dados adicionais
    pontos_sensibilidade: Optional[List[SensitivityPoint]] = Field(
        None,
        description="Pontos de sensibilidade preço x lucro"
    )
    product_name: str = Field(..., description="Nome do produto analisado")
    custo_total: float = Field(..., description="Custo total considerado")
    generated_at: str = Field(..., description="Data/hora da geração")
    
    class Config:
        json_schema_extra = {
            "example": {
                "preco_recomendado": 150.00,
                "margem_recomendada": 35.5,
                "preco_minimo": 120.00,
                "preco_premium": 180.00,
                "insights": [
                    "A margem de 35% é competitiva para o segmento",
                    "Considere estratégias de upsell",
                    "O custo de publicidade está otimizado"
                ],
                "riscos": [
                    "Margem pode ser apertada em períodos de promoção",
                    "Dependência de marketplace pode impactar lucratividade"
                ],
                "oportunidades": [
                    "Redução de custos de frete pode aumentar margem",
                    "Venda direta pode melhorar rentabilidade"
                ],
                "estrategia_sugerida": "Posicionar como produto de valor médio-alto...",
                "resumo_executivo": "Análise completa indica viabilidade com margem saudável...",
                "product_name": "Produto Exemplo",
                "custo_total": 100.00,
                "generated_at": "2024-01-15T10:30:00"
            }
        }


class AISuggestionHistoryResponse(BaseModel):
    """
    Schema para histórico de sugestões da IA.
    """
    id: int
    product_id: Optional[int]
    product_name: str
    suggested_price: float
    suggested_margin: float
    minimum_price: Optional[float]
    premium_price: Optional[float]
    total_cost: float
    created_at: datetime
    
    # Resumos curtos para listagem
    insights_count: int
    risks_count: int
    opportunities_count: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 5,
                "product_name": "Produto Exemplo",
                "suggested_price": 150.00,
                "suggested_margin": 35.5,
                "minimum_price": 120.00,
                "premium_price": 180.00,
                "total_cost": 100.00,
                "created_at": "2024-01-15T10:30:00",
                "insights_count": 3,
                "risks_count": 2,
                "opportunities_count": 2
            }
        }


class AISuggestionDetailResponse(AIAnalysisResponse):
    """
    Schema para detalhes completos de uma sugestão salva.
    """
    id: int
    product_id: Optional[int]
    created_at: datetime
    user_goal: Optional[str]
    desired_margin: Optional[float]
    
    class Config:
        from_attributes = True
