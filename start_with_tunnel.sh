#!/bin/bash

# Script para iniciar o backend PricePro com túnel público (ngrok)

echo "🚀 Iniciando PricePro Backend com Túnel Público..."
echo ""

# Verifica se ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok não encontrado!"
    echo ""
    echo "📝 Para instalar ngrok:"
    echo "   1. Acesse: https://dashboard.ngrok.com/signup"
    echo "   2. Crie uma conta gratuita"
    echo "   3. Instale com:"
    echo "      curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null"
    echo "      echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list"
    echo "      sudo apt update && sudo apt install ngrok"
    echo "   4. Autentique com: ngrok authtoken YOUR_TOKEN"
    echo ""
    exit 1
fi

# Verifica se Redis está rodando
if ! redis-cli ping &> /dev/null; then
    echo "⚠️  Redis não está rodando. Iniciando..."
    redis-server --daemonize yes
    sleep 1
fi

# Inicia o backend em background
echo "🔄 Iniciando backend FastAPI..."
cd /home/ubuntu/pricepro_backend
python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend iniciado (PID: $BACKEND_PID)"
sleep 3

# Verifica se o backend está rodando
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "❌ Erro ao iniciar backend!"
    echo "Verifique backend.log para detalhes"
    exit 1
fi

echo "✅ Backend funcionando em http://localhost:8000"
echo ""
echo "🌐 Criando túnel público com ngrok..."
echo ""

# Inicia ngrok em background e captura a URL
ngrok http 8000 > /dev/null &
NGROK_PID=$!
sleep 3

# Obtém a URL pública do ngrok
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*')

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ Erro ao obter URL do ngrok!"
    echo "Verifique se ngrok está autenticado: ngrok authtoken YOUR_TOKEN"
    kill $BACKEND_PID $NGROK_PID 2>/dev/null
    exit 1
fi

echo ""
echo "✅ Túnel criado com sucesso!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 URL Pública do Backend:"
echo ""
echo "    $PUBLIC_URL"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 IMPORTANTE: Atualize o frontend com esta URL!"
echo ""
echo "   1. Edite o arquivo .env do frontend:"
echo "      nano /home/ubuntu/pricepro_frontend/nextjs_space/.env"
echo ""
echo "   2. Atualize a variável:"
echo "      NEXT_PUBLIC_API_URL=$PUBLIC_URL"
echo ""
echo "   3. Reinicie o frontend:"
echo "      cd /home/ubuntu/pricepro_frontend/nextjs_space"
echo "      yarn build"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔍 Monitore os logs:"
echo "   Backend: tail -f /home/ubuntu/pricepro_backend/backend.log"
echo "   ngrok: http://localhost:4040"
echo ""
echo "⏸️  Para parar:"
echo "   kill $BACKEND_PID $NGROK_PID"
echo ""
echo "✅ Pronto! Acesse seu frontend via URL de preview!"
echo ""

# Mantém o script rodando
echo "Pressione Ctrl+C para parar os serviços..."
trap "echo ''; echo '🛑 Parando serviços...'; kill $BACKEND_PID $NGROK_PID 2>/dev/null; echo '✅ Serviços parados'; exit 0" INT
wait
