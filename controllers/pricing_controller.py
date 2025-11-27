"""
Controller de Precificação

Responsável por coordenar as operações de cálculo de preços.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from services.price_calculation_service import PriceCalculationService
from services.product_service import ProductService
from schemas.pricing import PriceSimulationRequest, PriceCalculationResult, ProductPriceCalculation


class PricingController:
    """
    Controller para operações de precificação.
    """
    
    @staticmethod
    def calculate_simulation(simulation: PriceSimulationRequest) -> PriceCalculationResult:
        """
        Calcula preços baseado em uma simulação.
        
        Não requer produto cadastrado - usuário pode simular preços
        fornecendo os parâmetros diretamente.
        
        Args:
            simulation: Dados da simulação
            
        Returns:
            Resultado completo do cálculo de preços
        """
        return PriceCalculationService.calculate_from_simulation(simulation)
    
    @staticmethod
    def calculate_product_price(
        calculation: ProductPriceCalculation,
        user_id: int,
        db: Session
    ) -> PriceCalculationResult:
        """
        Calcula preços de um produto existente.
        
        Args:
            calculation: Dados do cálculo (product_id e premium_factor)
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            
        Returns:
            Resultado completo do cálculo de preços
            
        Raises:
            HTTPException: Se produto não encontrado ou sem permissão
        """
        product_service = ProductService(db)
        product = product_service.get_product(calculation.product_id, user_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return PriceCalculationService.calculate_from_product(
            product=product,
            premium_factor=calculation.premium_factor
        )
