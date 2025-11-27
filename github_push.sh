#!/bin/bash

echo ""
echo "🚀 ===================================="
echo "    PUSH DO BACKEND PARA GITHUB"
echo "====================================="
echo ""

# Verificar se git está inicializado
if [ ! -d ".git" ]; then
    echo "🔧 Inicializando repositório Git..."
    git init
    echo "✅ Git inicializado!"
    echo ""
fi

# Adicionar todos os arquivos
echo "📋 Adicionando arquivos..."
git add .
echo "✅ Arquivos adicionados!"
echo ""

# Fazer commit
echo "📦 Criando commit..."
git commit -m "Deploy inicial do PricePro Backend para Railway"
echo "✅ Commit criado!"
echo ""

echo "👉 AGORA SIGA OS PASSOS ABAIXO:"
echo ""
echo "1️⃣ Crie um repositório no GitHub:"
echo "   https://github.com/new"
echo ""
echo "   - Nome: pricepro-backend"
echo "   - Tipo: Private"
echo "   - NÃO marque 'Initialize with README'"
echo ""
echo "2️⃣ Copie a URL do repositório (algo como):"
echo "   https://github.com/SEU-USUARIO/pricepro-backend.git"
echo ""
echo "3️⃣ Execute os comandos abaixo SUBSTITUINDO a URL:"
echo ""
echo "   git remote add origin https://github.com/SEU-USUARIO/pricepro-backend.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "⚠️  Se pedir senha, use um Personal Access Token:"
echo "   Crie em: https://github.com/settings/tokens"
echo "   Marque: 'repo' (Full control)"
echo ""
echo "4️⃣ Depois, siga o guia RAILWAY_WEB_DEPLOY.md"
echo ""
echo "====================================="
