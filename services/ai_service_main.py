"""
Serviço principal de IA

Orquestra as operações de análise de precificação com IA.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
import logging

from ai.service import AIService
from repositories.ai_repository import AIRepository
from repositories.product_repository import ProductRepository
from models.ai_suggestion import AISuggestion
from schemas.ai import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    AISuggestionHistoryResponse,
    AISuggestionDetailResponse
)

logger = logging.getLogger(__name__)


class AIServiceMain:
    """
    Serviço principal para operações de IA.
    """
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def analyze_product(
        self,
        db: Session,
        user_id: int,
        request: AIAnalysisRequest
    ) -> AIAnalysisResponse:
        """
        Analisa um produto e retorna recomendações de precificação.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário autenticado
            request: Dados da requisição
        
        Returns:
            AIAnalysisResponse com análise completa
        """
        try:
            # Preparar dados do produto
            product_data = await self._prepare_product_data(db, user_id, request)
            
            # Gerar análise com IA
            logger.info(f"Gerando análise de IA para usuário {user_id}")
            analysis = await self.ai_service.generate_full_analysis(
                product_data=product_data,
                user_goal=request.user_goal,
                desired_margin=request.desired_margin
            )
            
            # Salvar sugestão no banco
            ai_repository = AIRepository()
            ai_repository.create_suggestion(
                db=db,
                user_id=user_id,
                product_id=request.product_id,
                product_name=analysis['product_name'],
                analysis_data=analysis,
                user_goal=request.user_goal,
                desired_margin=request.desired_margin
            )
            
            logger.info("Análise gerada e salva com sucesso")
            
            # Converter para schema de resposta
            return AIAnalysisResponse(**analysis)
            
        except ValueError as e:
            logger.error(f"Erro de validação: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erro ao analisar produto: {str(e)}")
            raise Exception(f"Erro ao gerar análise: {str(e)}")
    
    async def _prepare_product_data(
        self,
        db: Session,
        user_id: int,
        request: AIAnalysisRequest
    ) -> Dict[str, Any]:
        """
        Prepara dados do produto para análise.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            request: Dados da requisição
        
        Returns:
            Dicionário com dados do produto
        """
        if request.product_id:
            # Buscar produto existente
            product_repository = ProductRepository(db)
            product = product_repository.get_by_id(db, request.product_id)
            
            if not product:
                raise ValueError(f"Produto {request.product_id} não encontrado")
            
            if product.user_id != user_id:
                raise ValueError("Você não tem permissão para analisar este produto")
            
            return {
                'name': product.name,
                'category': product.category,
                'production_cost': float(product.production_cost),
                'fixed_expenses': float(product.fixed_expenses),
                'variable_expenses': float(product.variable_expenses),
                'taxes': float(product.taxes),
                'marketplace_fee': float(product.marketplace_fee),
                'payment_fee': float(product.payment_fee),
                'shipping_fee': float(product.shipping_fee or 0),
                'advertising_fee': float(product.advertising_fee or 0)
            }
        else:
            # Usar dados manuais
            if not request.product_name:
                raise ValueError("Nome do produto é obrigatório")
            
            return {
                'name': request.product_name,
                'category': request.category or 'Não especificada',
                'production_cost': float(request.production_cost or 0),
                'fixed_expenses': float(request.fixed_expenses or 0),
                'variable_expenses': float(request.variable_expenses or 0),
                'taxes': float(request.taxes or 0),
                'marketplace_fee': float(request.marketplace_fee or 0),
                'payment_fee': float(request.payment_fee or 0),
                'shipping_fee': float(request.shipping_fee or 0),
                'advertising_fee': float(request.advertising_fee or 0)
            }
    
    def get_history(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ) -> List[AISuggestionHistoryResponse]:
        """
        Retorna histórico de análises do usuário.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            limit: Limite de resultados
            offset: Offset para paginação
        
        Returns:
            Lista de AISuggestionHistoryResponse
        """
        ai_repository = AIRepository()
        suggestions = ai_repository.get_by_user(db, user_id, limit, offset)
        
        return [
            AISuggestionHistoryResponse(
                id=s.id,
                product_id=s.product_id,
                product_name=s.product_name,
                suggested_price=s.suggested_price,
                suggested_margin=s.suggested_margin,
                minimum_price=s.minimum_price,
                premium_price=s.premium_price,
                total_cost=s.total_cost,
                created_at=s.created_at,
                insights_count=len(s.insights) if s.insights else 0,
                risks_count=len(s.risks) if s.risks else 0,
                opportunities_count=len(s.opportunities) if s.opportunities else 0
            )
            for s in suggestions
        ]
    
    def get_suggestion_detail(
        self,
        db: Session,
        user_id: int,
        suggestion_id: int
    ) -> Optional[AISuggestionDetailResponse]:
        """
        Retorna detalhes completos de uma sugestão.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            suggestion_id: ID da sugestão
        
        Returns:
            AISuggestionDetailResponse ou None
        """
        ai_repository = AIRepository()
        suggestion = ai_repository.get_by_id(db, suggestion_id)
        
        if not suggestion or suggestion.user_id != user_id:
            return None
        
        return AISuggestionDetailResponse(
            id=suggestion.id,
            product_id=suggestion.product_id,
            product_name=suggestion.product_name,
            preco_recomendado=suggestion.suggested_price,
            margem_recomendada=suggestion.suggested_margin,
            preco_minimo=suggestion.minimum_price,
            preco_premium=suggestion.premium_price,
            custo_total=suggestion.total_cost,
            insights=suggestion.insights or [],
            riscos=suggestion.risks or [],
            oportunidades=suggestion.opportunities or [],
            pontos_sensibilidade=suggestion.sensitivity_points,
            estrategia_sugerida=suggestion.strategy or "",
            resumo_executivo=suggestion.executive_summary or "",
            generated_at=suggestion.created_at.isoformat(),
            created_at=suggestion.created_at,
            user_goal=suggestion.user_goal,
            desired_margin=suggestion.desired_margin
        )
