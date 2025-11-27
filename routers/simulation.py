"""
Router de Simulação de Preços

Endpoints relacionados a simulação de preços:
- POST /simulation/calculate - Simular cálculo de preços sem criar produto
"""

from fastapi import APIRouter, Depends

from core.dependencies import check_rate_limit
from controllers.pricing_controller import PricingController
from schemas.pricing import PriceSimulationRequest, PriceCalculationResult
from models.user import User

router = APIRouter(
    prefix="/simulation",
    tags=["Simulação de Preços"],
    dependencies=[Depends(check_rate_limit)]  # Rate limiting aplicado a todas as rotas
)


@router.post(
    "/calculate",
    response_model=PriceCalculationResult,
    summary="Simular cálculo de preços",
    description="Calcula preços baseado em parâmetros fornecidos, sem precisar criar um produto."
)
def calculate_simulation(
    simulation: PriceSimulationRequest
) -> PriceCalculationResult:
    """
    Simula o cálculo de preços.
    
    Esta rota permite que o usuário calcule preços sem precisar cadastrar um produto.
    Útil para testes e exploração da ferramenta.
    
    Parâmetros:
    - cost_price: Custo de produção/compra
    - tax_percentage: Impostos (%)
    - variable_costs: Despesas variáveis por unidade
    - fixed_costs_allocated: Despesas fixas rateadas
    - sales_channels: Lista de canais de venda com suas taxas (opcional)
    - additional_fees: Taxas adicionais (maquininha, embalagem, etc.)
    - desired_margin_percentage: Margem desejada (%)
    - premium_factor: Fator multiplicador para preço premium
    
    Retorna:
    - Preço Mínimo: cobre todos os custos (margem zero)
    - Preço Ideal: inclui a margem desejada
    - Preço Premium: preço ideal + fator multiplicador
    - Lucro por unidade em cada cenário
    - Break-even: unidades necessárias para cobrir despesas fixas
    - Breakdown por canal de venda (se fornecido)
    - Detalhamento dos custos considerados
    
    Exemplo de uso:
    ```json
    {
      "cost_price": 50.00,
      "tax_percentage": 15.0,
      "variable_costs": 5.00,
      "fixed_costs_allocated": 1000.00,
      "sales_channels": [
        {"channel": "Loja Física", "fee_percentage": 0},
        {"channel": "Marketplace", "fee_percentage": 15}
      ],
      "additional_fees": 3.00,
      "desired_margin_percentage": 30.0,
      "premium_factor": 1.3
    }
    ```
    """
    return PricingController.calculate_simulation(simulation)
