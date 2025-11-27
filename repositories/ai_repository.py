"""
Repositório para AISuggestion

Gerencia operações de banco de dados relacionadas às sugestões de IA.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.ai_suggestion import AISuggestion


class AIRepository:
    """
    Repositório para gerenciar AISuggestion no banco de dados.
    """
    
    def create_suggestion(
        self,
        db: Session,
        user_id: int,
        product_id: Optional[int],
        product_name: str,
        analysis_data: dict,
        user_goal: Optional[str],
        desired_margin: Optional[float]
    ) -> AISuggestion:
        """
        Cria uma nova sugestão de IA.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            product_id: ID do produto (opcional)
            product_name: Nome do produto
            analysis_data: Dados da análise retornados pela IA
            user_goal: Objetivo do usuário
            desired_margin: Margem desejada
        
        Returns:
            AISuggestion criada
        """
        suggestion = AISuggestion(
            user_id=user_id,
            product_id=product_id,
            product_name=product_name,
            suggested_price=analysis_data.get('preco_recomendado'),
            suggested_margin=analysis_data.get('margem_recomendada'),
            minimum_price=analysis_data.get('preco_minimo'),
            premium_price=analysis_data.get('preco_premium'),
            total_cost=analysis_data.get('custo_total'),
            insights=analysis_data.get('insights', []),
            risks=analysis_data.get('riscos', []),
            opportunities=analysis_data.get('oportunidades', []),
            sensitivity_points=analysis_data.get('pontos_sensibilidade'),
            strategy=analysis_data.get('estrategia_sugerida'),
            executive_summary=analysis_data.get('resumo_executivo'),
            user_goal=user_goal,
            desired_margin=desired_margin
        )
        
        db.add(suggestion)
        db.commit()
        db.refresh(suggestion)
        
        return suggestion
    
    def get_by_id(self, db: Session, suggestion_id: int) -> Optional[AISuggestion]:
        """
        Busca sugestão por ID.
        
        Args:
            db: Sessão do banco de dados
            suggestion_id: ID da sugestão
        
        Returns:
            AISuggestion ou None
        """
        return db.query(AISuggestion).filter(AISuggestion.id == suggestion_id).first()
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ) -> List[AISuggestion]:
        """
        Lista sugestões de um usuário.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            limit: Limite de resultados
            offset: Offset para paginação
        
        Returns:
            Lista de AISuggestion
        """
        return (
            db.query(AISuggestion)
            .filter(AISuggestion.user_id == user_id)
            .order_by(desc(AISuggestion.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def get_by_product(
        self,
        db: Session,
        product_id: int,
        limit: int = 5
    ) -> List[AISuggestion]:
        """
        Lista sugestões para um produto específico.
        
        Args:
            db: Sessão do banco de dados
            product_id: ID do produto
            limit: Limite de resultados
        
        Returns:
            Lista de AISuggestion
        """
        return (
            db.query(AISuggestion)
            .filter(AISuggestion.product_id == product_id)
            .order_by(desc(AISuggestion.created_at))
            .limit(limit)
            .all()
        )
    
    def count_by_user(self, db: Session, user_id: int) -> int:
        """
        Conta total de sugestões de um usuário.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
        
        Returns:
            Total de sugestões
        """
        return db.query(AISuggestion).filter(AISuggestion.user_id == user_id).count()
    
    def delete(self, db: Session, suggestion_id: int) -> bool:
        """
        Deleta uma sugestão.
        
        Args:
            db: Sessão do banco de dados
            suggestion_id: ID da sugestão
        
        Returns:
            True se deletado, False se não encontrado
        """
        suggestion = self.get_by_id(db, suggestion_id)
        if suggestion:
            db.delete(suggestion)
            db.commit()
            return True
        return False
