"""
Router de Produtos

Endpoints relacionados a gestão de produtos:
- POST /products - Criar novo produto
- GET /products - Listar produtos do usuário
- GET /products/{product_id} - Obter produto específico
- PUT /products/{product_id} - Atualizar produto
- DELETE /products/{product_id} - Deletar produto
- POST /products/{product_id}/calculate-price - Calcular preços do produto
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database.connection import get_db
from core.dependencies import get_current_user, check_rate_limit
from controllers.product_controller import ProductController
from controllers.pricing_controller import PricingController
from schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from schemas.pricing import ProductPriceCalculation, PriceCalculationResult
from models.user import User

router = APIRouter(
    prefix="/products",
    tags=["Produtos"],
    dependencies=[Depends(check_rate_limit)]  # Rate limiting aplicado a todas as rotas
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    description="Cria um novo produto para o usuário autenticado."
)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """
    Cria um novo produto.
    
    Campos principais:
    - name: Nome do produto
    - cost_price: Custo de produção/compra
    - tax_percentage: Impostos (%)
    - variable_costs: Despesas variáveis por unidade
    - fixed_costs_allocated: Despesas fixas rateadas
    - sales_channels: Lista de canais de venda com suas taxas
    - desired_margin_percentage: Margem desejada (%)
    """
    return ProductController.create_product(current_user.id, product_data, db)


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Listar produtos",
    description="Lista todos os produtos do usuário autenticado com filtros opcionais."
)
def list_products(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    search: Optional[str] = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProductListResponse:
    """
    Lista produtos do usuário.
    
    Filtros:
    - category: Filtrar por categoria
    - search: Buscar por nome (busca parcial)
    
    Paginação:
    - skip: Pular N primeiros registros
    - limit: Limitar a N registros (máximo 100)
    """
    return ProductController.list_products(
        user_id=current_user.id,
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        search=search
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obter produto",
    description="Obtém um produto específico por ID."
)
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """
    Obtém um produto por ID.
    
    Apenas o dono do produto pode acessá-lo.
    """
    return ProductController.get_product(product_id, current_user.id, db)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Atualizar produto",
    description="Atualiza os dados de um produto."
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """
    Atualiza um produto.
    
    Todos os campos são opcionais - apenas os campos fornecidos serão atualizados.
    Apenas o dono do produto pode atualizá-lo.
    """
    return ProductController.update_product(product_id, current_user.id, product_data, db)


@router.delete(
    "/{product_id}",
    summary="Deletar produto",
    description="Deleta um produto."
)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um produto.
    
    Apenas o dono do produto pode deletá-lo.
    AVISO: Esta ação é irreversível.
    """
    return ProductController.delete_product(product_id, current_user.id, db)


@router.post(
    "/{product_id}/calculate-price",
    response_model=PriceCalculationResult,
    summary="Calcular preços do produto",
    description="Calcula os preços (mínimo, ideal e premium) de um produto."
)
def calculate_product_price(
    product_id: int,
    premium_factor: float = Query(
        1.3,
        ge=1.0,
        le=10.0,
        description="Fator multiplicador para preço premium (ex: 1.3 = +30%)"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PriceCalculationResult:
    """
    Calcula os preços de um produto.
    
    Retorna:
    - Preço Mínimo: cobre todos os custos (margem zero)
    - Preço Ideal: inclui a margem desejada
    - Preço Premium: preço ideal + fator multiplicador
    - Lucro por unidade em cada cenário
    - Break-even: unidades necessárias para cobrir despesas fixas
    - Breakdown por canal de venda (se aplicável)
    """
    calculation = ProductPriceCalculation(
        product_id=product_id,
        premium_factor=premium_factor
    )
    return PricingController.calculate_product_price(calculation, current_user.id, db)
