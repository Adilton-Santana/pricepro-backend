"""Serviço de IA para análise de precificação"""
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from .engine import AIEngine
from .prompts import SYSTEM_PROMPT, get_analysis_prompt

logger = logging.getLogger(__name__)

class AIService:
    """Serviço de análise de precificação com IA"""
    
    def __init__(self):
        self.engine = AIEngine()
    
    async def generate_full_analysis(
        self,
        product_data: Dict[str, Any],
        user_goal: str = "Equilibrar lucratividade e competitividade",
        desired_margin: float = 30.0
    ) -> Dict[str, Any]:
        """Gera análise completa de precificação
        
        Args:
            product_data: Dados do produto
            user_goal: Objetivo do empreendedor
            desired_margin: Margem desejada (%)
        
        Returns:
            Dict com análise completa
        """
        try:
            # Validar dados
            self._validate_product_data(product_data)
            
            # Gerar prompt
            prompt = get_analysis_prompt(product_data, user_goal, desired_margin)
            
            # Chamar a IA
            logger.info(f"Gerando análise de precificação para produto: {product_data.get('name')}")
            analysis = await self.engine.analyze_pricing(prompt, SYSTEM_PROMPT)
            
            # Enriquecer com metadados
            analysis["generated_at"] = datetime.utcnow().isoformat()
            analysis["product_name"] = product_data.get("name", "Produto")
            analysis["custo_total"] = self._calculate_total_cost(product_data)
            
            # Validar estrutura da resposta
            self._validate_analysis(analysis)
            
            logger.info("Análise gerada com sucesso")
            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao gerar análise completa: {str(e)}")
            raise
    
    def _validate_product_data(self, data: Dict[str, Any]) -> None:
        """Valida dados do produto"""
        required_fields = [
            'production_cost', 'fixed_expenses', 'variable_expenses',
            'taxes', 'marketplace_fee', 'payment_fee'
        ]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório ausente: {field}")
            
            if not isinstance(data[field], (int, float)):
                raise ValueError(f"Campo {field} deve ser numérico")
            
            if data[field] < 0:
                raise ValueError(f"Campo {field} não pode ser negativo")
    
    def _calculate_total_cost(self, data: Dict[str, Any]) -> float:
        """Calcula custo total do produto"""
        return (
            data.get('production_cost', 0) +
            data.get('fixed_expenses', 0) +
            data.get('variable_expenses', 0) +
            data.get('taxes', 0) +
            data.get('marketplace_fee', 0) +
            data.get('payment_fee', 0) +
            data.get('shipping_fee', 0) +
            data.get('advertising_fee', 0)
        )
    
    def _validate_analysis(self, analysis: Dict[str, Any]) -> None:
        """Valida estrutura da análise retornada"""
        required_fields = [
            'preco_recomendado', 'margem_recomendada', 'insights',
            'riscos', 'oportunidades', 'estrategia_sugerida', 'resumo_executivo'
        ]
        
        for field in required_fields:
            if field not in analysis:
                raise ValueError(f"Campo obrigatório ausente na análise: {field}")
        
        # Validar tipos
        if not isinstance(analysis['insights'], list) or len(analysis['insights']) < 2:
            raise ValueError("Insights deve ser uma lista com pelo menos 2 itens")
        
        if not isinstance(analysis['riscos'], list) or len(analysis['riscos']) < 1:
            raise ValueError("Riscos deve ser uma lista com pelo menos 1 item")
        
        if not isinstance(analysis['oportunidades'], list) or len(analysis['oportunidades']) < 1:
            raise ValueError("Oportunidades deve ser uma lista com pelo menos 1 item")
        
        if not isinstance(analysis['preco_recomendado'], (int, float)):
            raise ValueError("Preço recomendado deve ser numérico")
        
        if not isinstance(analysis['margem_recomendada'], (int, float)):
            raise ValueError("Margem recomendada deve ser numérica")
