"""
Serviço de Cálculo de Preços - Motor de Precificação Inteligente

Este é o CORE do PricePro!

Responsável por calcular preços de venda baseado em:
- Custos de produção/compra
- Impostos
- Despesas variáveis e fixas
- Taxas de canais de venda
- Margens desejadas

Calcula 3 tipos de preço:
1. Preço Mínimo: cobre todos os custos (margem zero)
2. Preço Ideal: inclui a margem desejada pelo usuário
3. Preço Premium: preço ideal + fator multiplicador extra
"""

from typing import Optional, List, Dict
from schemas.pricing import (
    PriceSimulationRequest,
    PriceCalculationResult,
    ChannelPriceBreakdown,
)
from schemas.product import SalesChannel
from models.product import Product


class PriceCalculationService:
    """
    Serviço para cálculo de preços.
    
    Este serviço implementa o motor de precificação inteligente do PricePro.
    """
    
    @staticmethod
    def calculate_from_simulation(
        simulation: PriceSimulationRequest
    ) -> PriceCalculationResult:
        """
        Calcula preços a partir de uma simulação.
        
        Args:
            simulation: Dados da simulação
            
        Returns:
            Resultado completo do cálculo de preços
        """
        return PriceCalculationService._calculate_prices(
            cost_price=simulation.cost_price,
            tax_percentage=simulation.tax_percentage,
            variable_costs=simulation.variable_costs,
            fixed_costs_allocated=simulation.fixed_costs_allocated,
            sales_channels=simulation.sales_channels,
            additional_fees=simulation.additional_fees,
            desired_margin_percentage=simulation.desired_margin_percentage,
            premium_factor=simulation.premium_factor
        )
    
    @staticmethod
    def calculate_from_product(
        product: Product,
        premium_factor: float = 1.3
    ) -> PriceCalculationResult:
        """
        Calcula preços a partir de um produto existente.
        
        Args:
            product: Produto com todos os dados de custo
            premium_factor: Fator multiplicador para preço premium
            
        Returns:
            Resultado completo do cálculo de preços
        """
        # Converte sales_channels de dict para SalesChannel objects
        sales_channels = None
        if product.sales_channels:
            sales_channels = [
                SalesChannel(**channel) for channel in product.sales_channels
            ]
        
        return PriceCalculationService._calculate_prices(
            cost_price=product.cost_price,
            tax_percentage=product.tax_percentage,
            variable_costs=product.variable_costs,
            fixed_costs_allocated=product.fixed_costs_allocated,
            sales_channels=sales_channels,
            additional_fees=product.additional_fees,
            desired_margin_percentage=product.desired_margin_percentage,
            premium_factor=premium_factor
        )
    
    @staticmethod
    def _calculate_prices(
        cost_price: float,
        tax_percentage: float,
        variable_costs: float,
        fixed_costs_allocated: float,
        sales_channels: Optional[List[SalesChannel]],
        additional_fees: float,
        desired_margin_percentage: float,
        premium_factor: float
    ) -> PriceCalculationResult:
        """
        Método interno que realiza o cálculo de preços.
        
        FÓRMULA DE PRECIFICAÇÃO:
        
        1. CUSTO TOTAL = custo_base + despesas_variaveis + taxas_adicionais
        2. PREÇO MÍNIMO = CUSTO_TOTAL / (1 - impostos/100)
        3. PREÇO IDEAL = CUSTO_TOTAL / (1 - impostos/100 - margem/100)
        4. PREÇO PREMIUM = PREÇO IDEAL * fator_premium
        
        Se houver canais de venda, ajusta o preço considerando as taxas de cada canal.
        """
        
        # ============= ETAPA 1: CALCULAR CUSTO TOTAL =============
        # Custo total = custo de aquisição + despesas variáveis + taxas adicionais
        total_variable_cost = cost_price + variable_costs + additional_fees
        
        # ============= ETAPA 2: CALCULAR PREÇOS GERAIS (SEM CANAL) =============
        
        # Preço Mínimo: cobre custos variáveis e impostos (margem = 0)
        # Fórmula: preço = custo / (1 - impostos/100)
        tax_decimal = tax_percentage / 100
        minimum_price = total_variable_cost / (1 - tax_decimal) if tax_decimal < 1 else total_variable_cost
        
        # Preço Ideal: cobre custos, impostos E margem desejada
        # Fórmula: preço = custo / (1 - impostos/100 - margem/100)
        margin_decimal = desired_margin_percentage / 100
        denominator = 1 - tax_decimal - margin_decimal
        
        if denominator <= 0:
            # Se impostos + margem >= 100%, não é possível calcular preço viável
            ideal_price = minimum_price * 2  # Fallback: dobra o preço mínimo
        else:
            ideal_price = total_variable_cost / denominator
        
        # Preço Premium: preço ideal com fator multiplicador
        premium_price = ideal_price * premium_factor
        
        # ============= ETAPA 3: CALCULAR LUCROS =============
        
        # Lucro = Preço - Custo Total - Impostos
        profit_minimum = minimum_price - total_variable_cost - (minimum_price * tax_decimal)
        profit_ideal = ideal_price - total_variable_cost - (ideal_price * tax_decimal)
        profit_premium = premium_price - total_variable_cost - (premium_price * tax_decimal)
        
        # ============= ETAPA 4: CALCULAR BREAK-EVEN =============
        # Break-even: quantas unidades preciso vender para cobrir despesas fixas?
        # Fórmula: unidades = despesas_fixas / lucro_por_unidade
        
        break_even_units = None
        if fixed_costs_allocated > 0 and profit_ideal > 0:
            break_even_units = fixed_costs_allocated / profit_ideal
        
        # ============= ETAPA 5: CALCULAR POR CANAL (SE APLICÁVEL) =============
        
        channel_breakdown = None
        if sales_channels and len(sales_channels) > 0:
            channel_breakdown = []
            
            for channel in sales_channels:
                channel_fee_decimal = channel.fee_percentage / 100
                
                # Ajusta preços considerando a taxa do canal
                # Fórmula: preço_final = preço_base / (1 - taxa_canal/100)
                channel_denominator = 1 - channel_fee_decimal
                
                if channel_denominator <= 0:
                    # Se taxa do canal >= 100%, usa preços base
                    channel_min = minimum_price
                    channel_ideal = ideal_price
                    channel_premium = premium_price
                else:
                    channel_min = minimum_price / channel_denominator
                    channel_ideal = ideal_price / channel_denominator
                    channel_premium = premium_price / channel_denominator
                
                # Lucro considerando taxa do canal
                channel_profit = channel_ideal - total_variable_cost - (channel_ideal * tax_decimal) - (channel_ideal * channel_fee_decimal)
                
                channel_breakdown.append(
                    ChannelPriceBreakdown(
                        channel=channel.channel,
                        fee_percentage=channel.fee_percentage,
                        minimum_price=round(channel_min, 2),
                        ideal_price=round(channel_ideal, 2),
                        premium_price=round(channel_premium, 2),
                        profit_per_unit_ideal=round(channel_profit, 2)
                    )
                )
        
        # ============= ETAPA 6: MONTAR BREAKDOWN DE CUSTOS =============
        
        cost_breakdown = {
            "custo_producao_compra": round(cost_price, 2),
            "despesas_variaveis": round(variable_costs, 2),
            "taxas_adicionais": round(additional_fees, 2),
            "custo_total_variavel": round(total_variable_cost, 2),
            "despesas_fixas_rateadas": round(fixed_costs_allocated, 2),
            "impostos_percentual": tax_percentage,
            "margem_desejada_percentual": desired_margin_percentage,
        }
        
        # ============= RETORNAR RESULTADO COMPLETO =============
        
        return PriceCalculationResult(
            minimum_price=round(minimum_price, 2),
            ideal_price=round(ideal_price, 2),
            premium_price=round(premium_price, 2),
            profit_per_unit_minimum=round(profit_minimum, 2),
            profit_per_unit_ideal=round(profit_ideal, 2),
            profit_per_unit_premium=round(profit_premium, 2),
            break_even_units=round(break_even_units, 2) if break_even_units else None,
            channel_breakdown=channel_breakdown,
            cost_breakdown=cost_breakdown
        )
