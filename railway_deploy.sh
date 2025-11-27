#!/bin/bash

# Script de Deploy Automatizado para Railway

set -e  # Para em caso de erro

echo "🚀 PricePro Backend - Deploy Automático no Railway"
echo "="*60
echo ""

# Verifica se Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI não encontrado. Instalando..."
    npm install -g @railway/cli
    echo "✅ Railway CLI instalado!"
fi

echo "🔑 Fazendo login no Railway..."
railway login

echo ""
echo "🏗️  Criando novo projeto..."
railway init

echo ""
echo "📦 Criando serviço PostgreSQL..."
echo "   (Railway vai provisionar automaticamente)"

echo ""
echo "⚙️  Configurando variáveis de ambiente..."
echo ""
echo "📝 IMPORTANTE: Defina um SECRET_KEY forte!"
read -p "Digite o SECRET_KEY (ou pressione Enter para gerar): " SECRET_KEY

if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "✅ SECRET_KEY gerado automaticamente: $SECRET_KEY"
fi

railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set APP_NAME="PricePro"
railway variables set DEBUG="False"
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set REFRESH_TOKEN_EXPIRE_DAYS="7"

echo ""
echo "🚀 Fazendo deploy..."
railway up

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "="*60
echo "🌐 Obtenha a URL pública:"
echo "   railway domain"
echo ""
echo "📊 Monitore os logs:"
echo "   railway logs"
echo ""
echo "⚙️  Gerencie no dashboard:"
echo "   railway open"
echo "="*60
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo "1. Copie a URL gerada"
echo "2. Atualize NEXT_PUBLIC_API_URL no frontend"
echo "3. Rebuild o frontend: cd ../pricepro_frontend/nextjs_space && yarn build"
echo ""
