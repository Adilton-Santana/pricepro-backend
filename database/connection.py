"""
Configuração de Conexão com o Banco de Dados

Responsável por:
- Criar engine do SQLAlchemy
- Criar SessionLocal para gerenciar sessões do banco
- Fornecer Base declarativa para os models
- Dependency para obter sessões do banco nas rotas
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from core.config import settings

# Cria o engine do SQLAlchemy
# echo=True mostra os logs SQL (útil para debug)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_size=10,  # Número de conexões no pool
    max_overflow=20  # Conexões extras quando o pool está cheio
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa para os models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter uma sessão do banco de dados.
    
    Uso nas rotas:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    Deve ser chamado no startup da aplicação.
    """
    from models import user, product  # Importa todos os models
    Base.metadata.create_all(bind=engine)
