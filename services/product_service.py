"""
Serviço de Produto

Responsável por toda a lógica de negócio relacionada a produtos:
- Criação e gestão de produtos
- Validações de negócio
- Verificação de permissões
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status

from repositories.product_repository import ProductRepository
from schemas.product import ProductCreate, ProductUpdate
from models.product import Product


class ProductService:
    """
    Serviço para gerenciar operações de produtos.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepository(db)
    
    def create_product(self, user_id: int, product_data: ProductCreate) -> Product:
        """
        Cria um novo produto.
        
        Args:
            user_id: ID do usuário dono do produto
            product_data: Dados do produto
            
        Returns:
            Produto criado
        """
        return self.product_repo.create(user_id, product_data)
    
    def get_product(self, product_id: int, user_id: int) -> Optional[Product]:
        """
        Busca um produto por ID.
        Verifica se o usuário tem permissão para acessar.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário solicitante
            
        Returns:
            Produto encontrado ou None
            
        Raises:
            HTTPException: Se produto não pertence ao usuário
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None
        
        # Verifica se o produto pertence ao usuário
        if product.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este produto"
            )
        
        return product
    
    def list_user_products(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """
        Lista produtos de um usuário com filtros opcionais.
        
        Args:
            user_id: ID do usuário
            skip: Número de registros a pular
            limit: Número máximo de registros
            category: Filtro por categoria (opcional)
            search: Busca por nome (opcional)
            
        Returns:
            Lista de produtos
        """
        if search:
            return self.product_repo.search_by_name(user_id, search)
        elif category:
            return self.product_repo.get_by_category(user_id, category)
        else:
            return self.product_repo.get_by_user(user_id, skip, limit)
    
    def update_product(
        self,
        product_id: int,
        user_id: int,
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Atualiza dados de um produto.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário solicitante
            product_data: Dados a serem atualizados
            
        Returns:
            Produto atualizado ou None se não encontrado
            
        Raises:
            HTTPException: Se produto não pertence ao usuário
        """
        # Verifica permissão
        product = self.get_product(product_id, user_id)
        if not product:
            return None
        
        return self.product_repo.update(product_id, product_data)
    
    def delete_product(self, product_id: int, user_id: int) -> bool:
        """
        Deleta um produto.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário solicitante
            
        Returns:
            True se deletado com sucesso, False se não encontrado
            
        Raises:
            HTTPException: Se produto não pertence ao usuário
        """
        # Verifica permissão
        product = self.get_product(product_id, user_id)
        if not product:
            return False
        
        return self.product_repo.delete(product_id)
    
    def count_user_products(self, user_id: int) -> int:
        """
        Conta o número de produtos de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Número de produtos
        """
        return self.product_repo.count_by_user(user_id)
