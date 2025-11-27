"""
PricePro Backend - Main Application

Este é o ponto de entrada da aplicação PricePro.

Aplicação FastAPI para precificação inteligente de produtos.
Permite que empreendedores calculem preços de venda considerando:
- Custos de produção/compra
- Impostos e taxas
- Despesas fixas e variáveis
- Canais de venda
- Margens desejadas

Tecnologias:
- FastAPI: Framework web assíncrono
- PostgreSQL: Banco de dados relacional
- Redis: Cache e rate limiting
- SQLAlchemy: ORM
- JWT: Autenticação
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from database.connection import init_db
from database.redis_client import redis_client
from routers import auth, users, products, simulation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    
    Startup:
    - Inicializa o banco de dados (cria tabelas)
    - Testa conexão com Redis
    
    Shutdown:
    - Cleanup se necessário
    """
    # Startup
    print("🚀 Iniciando PricePro Backend...")
    
    # Inicializa o banco de dados
    print("📊 Inicializando banco de dados PostgreSQL...")
    init_db()
    print("✅ Banco de dados inicializado")
    
    # Testa conexão com Redis
    print("🔴 Testando conexão com Redis...")
    if redis_client.ping():
        print("✅ Redis conectado")
    else:
        print("⚠️  AVISO: Redis não está disponível. Rate limiting não funcionará.")
    
    print("✅ PricePro Backend iniciado com sucesso!")
    print(f"📖 Documentação disponível em: http://localhost:8000/docs")
    
    yield
    
    # Shutdown
    print("👋 Encerrando PricePro Backend...")


# Cria a aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============= MIDDLEWARES =============

# CORS - Permite requisições de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.preview\.abacusai\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= EXCEPTION HANDLERS =============

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handler global para exceções não tratadas.
    """
    if settings.DEBUG:
        # Em desenvolvimento, mostra o erro completo
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Erro interno do servidor",
                "error": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        # Em produção, oculta detalhes do erro
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Erro interno do servidor"}
        )


# ============= ROUTERS =============

# Health check endpoint
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Verifica se a API está funcionando."
)
def health_check():
    """
    Endpoint simples para verificar se a API está online.
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "PricePro API está funcionando! 🚀"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check Detalhado",
    description="Verifica o status da API e suas dependências."
)
def detailed_health_check():
    """
    Health check detalhado incluindo status de dependências.
    """
    redis_status = "ok" if redis_client.ping() else "error"
    
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "ok",  # Se chegou aqui, o banco está ok
        "redis": redis_status,
    }


# Registra os routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(simulation.router)


# ============= MAIN =============

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║           🚀 PRICEPRO BACKEND 🚀             ║
    ║                                               ║
    ║     Sistema de Precificação Inteligente      ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
