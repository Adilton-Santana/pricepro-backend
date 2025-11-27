"""
Model de Sugestão de IA

Armazena as análises e recomendações de precificação geradas pela IA.
"""

from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base


class AISuggestion(Base):
    """
    Model de Sugestão de IA.
    
    Armazena histórico de análises de precificação realizadas pela IA,
    incluindo recomendações de preço, insights, riscos e oportunidades.
    
    Atributos:
        id: Identificador único
        user_id: ID do usuário que solicitou a análise
        product_id: ID do produto analisado (opcional)
        product_name: Nome do produto no momento da análise
        suggested_price: Preço recomendado pela IA
        suggested_margin: Margem recomendada pela IA (%)
        minimum_price: Preço mínimo sugerido
        premium_price: Preço premium sugerido
        total_cost: Custo total considerado na análise
        insights: Lista de insights (JSON)
        risks: Lista de riscos identificados (JSON)
        opportunities: Lista de oportunidades (JSON)
        strategy: Estratégia comercial sugerida
        executive_summary: Resumo executivo da análise
        sensitivity_points: Pontos de sensibilidade preço x lucro (JSON)
        user_goal: Objetivo informado pelo usuário
        desired_margin: Margem desejada pelo usuário (%)
        created_at: Data/hora da análise
    
    Relacionamentos:
        user: Usuário que solicitou a análise
        product: Produto analisado (opcional)
    """
    
    __tablename__ = "ai_suggestions"
    
    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    product_name = Column(String(255), nullable=False)
    
    # Recomendações de preço
    suggested_price = Column(Float, nullable=False)
    suggested_margin = Column(Float, nullable=False)
    minimum_price = Column(Float, nullable=True)
    premium_price = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=False)
    
    # Análises (JSON)
    insights = Column(JSON, nullable=False)
    risks = Column(JSON, nullable=False)
    opportunities = Column(JSON, nullable=False)
    sensitivity_points = Column(JSON, nullable=True)
    
    # Textos descritivos
    strategy = Column(Text, nullable=True)
    executive_summary = Column(Text, nullable=True)
    
    # Parâmetros da análise
    user_goal = Column(String(500), nullable=True)
    desired_margin = Column(Float, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="ai_suggestions")
    product = relationship("Product", back_populates="ai_suggestions")
    
    def __repr__(self):
        return f"<AISuggestion(id={self.id}, product='{self.product_name}', price={self.suggested_price})>"
