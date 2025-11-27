"""
Model de Produto

Representa a tabela 'products' no banco de dados PostgreSQL.
Contém todas as informações necessárias para precificação de produtos.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base


class Product(Base):
    """
    Model de Produto.
    
    Armazena todas as informações necessárias para cálculo de preço:
    - Custos de produção/compra
    - Impostos e taxas
    - Despesas fixas e variáveis
    - Canais de venda com taxas específicas
    - Margens desejadas
    
    Atributos:
        id: Identificador único
        user_id: ID do usuário dono do produto
        name: Nome do produto
        category: Categoria do produto
        description: Descrição detalhada
        
        # Custos
        cost_price: Custo de produção ou compra
        tax_percentage: Percentual de impostos (ex: 15.5 para 15,5%)
        variable_costs: Despesas variáveis por unidade
        fixed_costs_allocated: Despesas fixas rateadas para este produto
        
        # Taxas e canais
        sales_channels: JSON com lista de canais e suas taxas
            Exemplo: [{"channel": "Loja Física", "fee_percentage": 0}, 
                      {"channel": "Marketplace", "fee_percentage": 15}]
        
        additional_fees: Taxas adicionais (maquininha, embalagem, etc.)
        
        # Margens
        desired_margin_percentage: Margem de lucro desejada (ex: 30 para 30%)
        
        # Metadata
        is_active: Indica se o produto está ativo
        created_at: Data/hora de criação
        updated_at: Data/hora da última atualização
    
    Relacionamentos:
        owner: Usuário dono do produto
    """
    
    __tablename__ = "products"
    
    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Informações básicas
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    
    # Custos
    cost_price = Column(Float, nullable=False)  # Custo de produção/compra
    tax_percentage = Column(Float, default=0.0, nullable=False)  # Percentual de impostos
    variable_costs = Column(Float, default=0.0, nullable=False)  # Despesas variáveis por unidade
    fixed_costs_allocated = Column(Float, default=0.0, nullable=False)  # Despesas fixas rateadas
    
    # Canais de venda e taxas
    # Exemplo: [{"channel": "Loja Física", "fee_percentage": 0}, {"channel": "Online", "fee_percentage": 10}]
    sales_channels = Column(JSON, nullable=True)  
    
    # Taxas adicionais (maquininha, embalagem, frete, etc.)
    additional_fees = Column(Float, default=0.0, nullable=False)
    
    # Margem desejada
    desired_margin_percentage = Column(Float, default=30.0, nullable=False)  # Margem desejada em %
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relacionamentos
    owner = relationship("User", back_populates="products")
    ai_suggestions = relationship("AISuggestion", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', owner_id={self.user_id})>"
