#!/bin/bash

# Script de inicialização para Railway
# Garante que a porta $PORT seja usada corretamente

echo "🚀 Iniciando PricePro Backend"
echo "📍 Porta: $PORT"
echo "🌐 Host: 0.0.0.0"

exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
