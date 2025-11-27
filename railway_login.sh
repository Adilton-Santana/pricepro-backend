#!/bin/bash

# Script para fazer login no Railway

echo "" 
echo "🔐 ===================================="
echo "    RAILWAY LOGIN - PASSO A PASSO"
echo "====================================="
echo ""
echo "📋 INSTRUÇÕES:"
echo ""
echo "1. Este comando vai abrir uma URL no seu navegador"
echo "2. Faça login na sua conta Railway"
echo "3. Autorize o acesso da CLI"
echo "4. Volte aqui e aguarde a confirmação"
echo ""
echo "⚠️  Se o navegador NÃO abrir automaticamente:"
echo "   - Copie a URL que aparecer"
echo "   - Cole no navegador manualmente"
echo "   - Complete o login"
echo ""
echo "🚀 Iniciando login..."
echo ""

railway login

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ===================================="
    echo "    LOGIN REALIZADO COM SUCESSO!"
    echo "====================================="
    echo ""
    echo "🎯 PRÓXIMO PASSO:"
    echo ""
    echo "Execute o script de deploy:"
    echo "./railway_deploy.sh"
    echo ""
else
    echo ""
    echo "❌ ===================================="
    echo "    ERRO NO LOGIN"
    echo "====================================="
    echo ""
    echo "🔧 SOLUÇÕES:"
    echo ""
    echo "1. Tente novamente: railway login"
    echo "2. Verifique se você tem uma conta no Railway"
    echo "3. Crie uma conta em: https://railway.app"
    echo ""
fi
