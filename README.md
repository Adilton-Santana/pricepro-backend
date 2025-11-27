# PricePro Backend

Sistema de precificação inteligente para empreendedores.

---

## 🚀 Deploy em Produção (RECOMENDADO)

### **Railway - Deploy Automático**

```bash
cd /home/ubuntu/pricepro_backend
./railway_deploy.sh
```

✅ **Pronto!** O script fará tudo automaticamente:
- Criar projeto no Railway
- Provisionar PostgreSQL gratuito
- Configurar variáveis de ambiente
- Fazer deploy
- Gerar URL pública

📖 **Guia Detalhado**: Ver `RAILWAY_QUICKSTART.md`

---

## 💻 Desenvolvimento Local

### **Requisitos:**
- Python 3.9+
- PostgreSQL (ou usar Railway)
- Redis (opcional)

### **Instalação:**

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Configure DATABASE_URL e SECRET_KEY

# Rodar backend
python main.py
```

### **Sem Redis:**
✅ Backend funciona sem Redis!
- Usa cache em memória automaticamente
- Perfeito para desenvolvimento

---

## 📚 Documentação

- **Railway Deploy**: `RAILWAY_QUICKSTART.md` ⭐ (Recomendado)
- **Deploy Manual**: `DEPLOY_GUIDE.md`
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ Tecnologias

- FastAPI (Framework)
- PostgreSQL (Database)
- Redis (Cache - Opcional)
- SQLAlchemy (ORM)
- JWT (Autenticação)

---

## 🏛️ Estrutura

```
pricepro_backend/
├── main.py                   # Entry point
├── requirements.txt          # Dependências Python
├── railway.json             # Config Railway
├── railway_deploy.sh        # Script de deploy
├── core/                    # Configurações
├── database/               # Conexões DB
│   └── redis_client.py     # Cache (Redis/Memória)
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic schemas
├── routers/                # API endpoints
├── services/               # Business logic
└── utils/                  # Utilitários
```

---

## 🌐 Acesso via Preview URL

### **Opção Recomendada: Railway**

1. Deploy backend no Railway:
   ```bash
   ./railway_deploy.sh
   ```

2. Obter URL pública:
   ```bash
   railway domain
   # Exemplo: https://pricepro-backend-production.up.railway.app
   ```

3. Atualizar frontend:
   ```bash
   cd ../pricepro_frontend/nextjs_space
   nano .env
   # Adicionar: NEXT_PUBLIC_API_URL=https://sua-url-railway.app
   yarn build
   ```

✅ **Pronto! Acesse via preview URL!**

---

## 🔧 Configuração

### **Variáveis de Ambiente Essenciais:**

```env
# Database (Railway fornece automaticamente)
DATABASE_URL=postgresql://user:password@host:5432/db

# Security (OBRIGATÓRIO)
SECRET_KEY=seu_secret_super_seguro

# App
APP_NAME=PricePro
DEBUG=False
```

### **Gerar SECRET_KEY:**
```bash
openssl rand -hex 32
```

---

## 🔍 Features

- ✅ Autenticação JWT com refresh tokens
- ✅ Rate limiting automático
- ✅ Cache inteligente (Redis/Memória)
- ✅ CRUD completo de produtos
- ✅ Simulação de precificação avançada
- ✅ Documentação interativa (Swagger)
- ✅ Validação de dados (Pydantic)
- ✅ Clean Architecture

---

## 📊 Status

- Backend: ✅ Produção-ready
- Database: ✅ PostgreSQL integrado
- Cache: ✅ Redis opcional (funciona sem)
- Deploy: ✅ Railway automático
- Docs: ✅ Swagger + ReDoc

---

## 🚦 Endpoints Principais

- `POST /auth/register` - Registro de usuários
- `POST /auth/login` - Login
- `GET /products` - Listar produtos
- `POST /products` - Criar produto
- `POST /simulation` - Simular preços

**Ver documentação completa**: `/docs`

---

## 🆘 Suporte

- **Railway**: Ver `RAILWAY_QUICKSTART.md`
- **Deploy Manual**: Ver `DEPLOY_GUIDE.md`
- **API Docs**: http://localhost:8000/docs
