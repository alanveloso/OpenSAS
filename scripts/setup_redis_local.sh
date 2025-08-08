#!/bin/bash

# Script para instalar e configurar Redis localmente para OpenSAS

set -e

echo "🚀 Configurando Redis localmente para OpenSAS..."

# Verificar se estamos no Ubuntu/Debian
if command -v apt-get &> /dev/null; then
    echo "📦 Instalando Redis via apt..."
    sudo apt-get update
    sudo apt-get install -y redis-server
    
elif command -v yum &> /dev/null; then
    echo "📦 Instalando Redis via yum..."
    sudo yum install -y redis
    
elif command -v dnf &> /dev/null; then
    echo "📦 Instalando Redis via dnf..."
    sudo dnf install -y redis
    
else
    echo "❌ Sistema não suportado. Por favor, instale Redis manualmente."
    exit 1
fi

# Iniciar e habilitar o serviço Redis
echo "🔧 Configurando serviço Redis..."
sudo systemctl start redis
sudo systemctl enable redis

# Verificar se o serviço está rodando
if sudo systemctl is-active --quiet redis; then
    echo "✅ Redis está rodando!"
else
    echo "❌ Erro ao iniciar Redis"
    exit 1
fi

# Testar conexão Redis
echo "🔍 Testando conexão Redis..."
if redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis respondeu corretamente!"
else
    echo "❌ Erro ao conectar com Redis"
    exit 1
fi

echo "✅ Redis configurado com sucesso!"
echo ""
echo "📋 Informações de conexão:"
echo "   Host: localhost"
echo "   Porta: 6379"
echo "   URL: redis://localhost:6379"
echo ""
echo "📝 Para testar a conexão:"
echo "   redis-cli ping"
echo ""
echo "🎉 Configuração concluída!"
