"""
Controller de Produto

Responsável por coordenar as operações de produtos entre routers e services.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional, Dict

from services.product_service import ProductService
from schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse


class ProductController:
    """
    Controller para operações de produtos.
    """
    
    @staticmethod
    def create_product(user_id: int, product_data: ProductCreate, db: Session) -> ProductResponse:
        """
        Cria um novo produto.
        
        Args:
            user_id: ID do usuário autenticado
            product_data: Dados do produto
            db: Sessão do banco de dados
            
        Returns:
            Produto criado
        """
        product_service = ProductService(db)
        product = product_service.create_product(user_id, product_data)
        
        return ProductResponse.from_orm(product)
    
    @staticmethod
    def get_product(product_id: int, user_id: int, db: Session) -> ProductResponse:
        """
        Obtém um produto por ID.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            
        Returns:
            Dados do produto
            
        Raises:
            HTTPException: Se produto não encontrado ou sem permissão
        """
        product_service = ProductService(db)
        product = product_service.get_product(product_id, user_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProductResponse.from_orm(product)
    
    @staticmethod
    def list_products(
        user_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> ProductListResponse:
        """
        Lista produtos do usuário com filtros.
        
        Args:
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            skip: Número de registros a pular
            limit: Número máximo de registros
            category: Filtro por categoria (opcional)
            search: Busca por nome (opcional)
            
        Returns:
            Lista de produtos com metadados de paginação
        """
        product_service = ProductService(db)
        
        products = product_service.list_user_products(
            user_id=user_id,
            skip=skip,
            limit=limit,
            category=category,
            search=search
        )
        
        total = product_service.count_user_products(user_id)
        
        return ProductListResponse(
            total=total,
            page=skip // limit + 1,
            page_size=len(products),
            products=[ProductResponse.from_orm(p) for p in products]
        )
    
    @staticmethod
    def update_product(
        product_id: int,
        user_id: int,
        product_data: ProductUpdate,
        db: Session
    ) -> ProductResponse:
        """
        Atualiza um produto.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário autenticado
            product_data: Dados a serem atualizados
            db: Sessão do banco de dados
            
        Returns:
            Produto atualizado
            
        Raises:
            HTTPException: Se produto não encontrado ou sem permissão
        """
        product_service = ProductService(db)
        product = product_service.update_product(product_id, user_id, product_data)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProductResponse.from_orm(product)
    
    @staticmethod
    def delete_product(product_id: int, user_id: int, db: Session) -> Dict:
        """
        Deleta um produto.
        
        Args:
            product_id: ID do produto
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            
        Returns:
            Mensagem de sucesso
            
        Raises:
            HTTPException: Se produto não encontrado ou sem permissão
        """
        product_service = ProductService(db)
        success = product_service.delete_product(product_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return {"message": "Produto deletado com sucesso"}
