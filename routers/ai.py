"""
Router de IA

Endpoints para análise de precificação com IA.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from database.connection import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.ai import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    AISuggestionHistoryResponse,
    AISuggestionDetailResponse
)
from services.ai_service_main import AIServiceMain

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
    responses={
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão"},
        500: {"description": "Erro interno do servidor"}
    }
)

ai_service = AIServiceMain()


@router.post(
    "/analyze",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Gerar análise de precificação com IA",
    description="""
    Gera uma análise completa de precificação usando IA.
    
    Pode receber:
    - `product_id`: Para analisar um produto existente
    - Ou dados manuais completos do produto
    
    Retorna recomendações de preço, insights, riscos e oportunidades.
    """
)
async def analyze_product(
    request: AIAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analisa produto e retorna recomendações de precificação.
    
    Args:
        request: Dados da requisição (product_id ou dados manuais)
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        AIAnalysisResponse com análise completa
    
    Raises:
        HTTPException 400: Dados inválidos
        HTTPException 404: Produto não encontrado
        HTTPException 403: Sem permissão
        HTTPException 500: Erro na análise
    """
    try:
        logger.info(f"Usuário {current_user.id} solicitou análise de IA")
        
        analysis = await ai_service.analyze_product(
            db=db,
            user_id=current_user.id,
            request=request
        )
        
        return analysis
        
    except ValueError as e:
        logger.warning(f"Erro de validação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao gerar análise: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar análise de IA. Tente novamente."
        )


@router.get(
    "/history",
    response_model=List[AISuggestionHistoryResponse],
    summary="Listar histórico de análises",
    description="""
    Retorna o histórico de análises de precificação do usuário.
    
    Suporta paginação com `limit` e `offset`.
    """
)
def get_history(
    limit: int = Query(10, ge=1, le=50, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista histórico de análises do usuário.
    
    Args:
        limit: Limite de resultados (1-50)
        offset: Offset para paginação
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        Lista de AISuggestionHistoryResponse
    """
    try:
        history = ai_service.get_history(
            db=db,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        return history
        
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico de análises"
        )


@router.get(
    "/history/{suggestion_id}",
    response_model=AISuggestionDetailResponse,
    summary="Detalhes de uma análise",
    description="""
    Retorna os detalhes completos de uma análise específica.
    
    Inclui todos os insights, riscos, oportunidades e recomendações.
    """
)
def get_suggestion_detail(
    suggestion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna detalhes de uma sugestão específica.
    
    Args:
        suggestion_id: ID da sugestão
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        AISuggestionDetailResponse
    
    Raises:
        HTTPException 404: Sugestão não encontrada
    """
    try:
        suggestion = ai_service.get_suggestion_detail(
            db=db,
            user_id=current_user.id,
            suggestion_id=suggestion_id
        )
        
        if not suggestion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Análise não encontrada"
            )
        
        return suggestion
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar sugestão: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar detalhes da análise"
        )
