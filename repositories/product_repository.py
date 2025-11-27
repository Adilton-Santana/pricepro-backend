"""
Repository de Produto

Camada de acesso a dados para operações com produtos.
Responsável por todas as queries relacionadas à tabela products.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """
    Repository para operações de banco de dados com produtos.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, product_data: ProductCreate) -> Product:
        """
        Cria um novo produto no banco de dados.
        
        Args:
            user_id: ID do usuário dono do produto
            product_data: Dados do produto a ser criado
            
        Returns:
            Produto criado
        """
        # Converte lista de SalesChannel para dict para armazenar no JSON
        sales_channels_dict = None
        if product_data.sales_channels:
            sales_channels_dict = [
                channel.model_dump() for channel in product_data.sales_channels
            ]
        
        db_product = Product(
            user_id=user_id,
            name=product_data.name,
            category=product_data.category,
            description=product_data.description,
            cost_price=product_data.cost_price,
            tax_percentage=product_data.tax_percentage,
            variable_costs=product_data.variable_costs,
            fixed_costs_allocated=product_data.fixed_costs_allocated,
            sales_channels=sales_channels_dict,
            additional_fees=product_data.additional_fees,
            desired_margin_percentage=product_data.desired_margin_percentage
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca produto por ID.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Produto encontrado ou None
        """
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Busca todos os produtos de um usuário com paginação.
        
        Args:
            user_id: ID do usuário
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de produtos
        """
        return self.db.query(Product).filter(
            Product.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_category(self, user_id: int, category: str) -> List[Product]:
        """
        Busca produtos de um usuário por categoria.
        
        Args:
            user_id: ID do usuário
            category: Categoria dos produtos
            
        Returns:
            Lista de produtos
        """
        return self.db.query(Product).filter(
            Product.user_id == user_id,
            Product.category == category
        ).all()
    
    def search_by_name(self, user_id: int, name: str) -> List[Product]:
        """
        Busca produtos por nome (busca parcial).
        
        Args:
            user_id: ID do usuário
            name: Nome ou parte do nome do produto
            
        Returns:
            Lista de produtos
        """
        return self.db.query(Product).filter(
            Product.user_id == user_id,
            Product.name.ilike(f"%{name}%")
        ).all()
    
    def update(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """
        Atualiza dados de um produto.
        
        Args:
            product_id: ID do produto
            product_data: Dados a serem atualizados
            
        Returns:
            Produto atualizado ou None se não encontrado
        """
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None
        
        # Atualiza apenas os campos fornecidos
        update_data = product_data.model_dump(exclude_unset=True)
        
        # Converte sales_channels se fornecido
        if "sales_channels" in update_data and update_data["sales_channels"]:
            update_data["sales_channels"] = [
                channel.model_dump() if hasattr(channel, 'model_dump') else channel
                for channel in update_data["sales_channels"]
            ]
        
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int) -> bool:
        """
        Deleta um produto.
        
        Args:
            product_id: ID do produto
            
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False
        
        self.db.delete(db_product)
        self.db.commit()
        return True
    
    def count_by_user(self, user_id: int) -> int:
        """
        Conta o número de produtos de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Número de produtos
        """
        return self.db.query(Product).filter(Product.user_id == user_id).count()
    
    def is_owner(self, product_id: int, user_id: int) -> bool:
        """
        Verifica se um usuário é dono de um produto.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário
            
        Returns:
            True se é o dono, False caso contrário
        """
        product = self.get_by_id(product_id)
        if not product:
            return False
        return product.user_id == user_id
