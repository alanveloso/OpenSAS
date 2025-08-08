#!/bin/bash

# Script de teste consolidado para verificar se o OpenSAS está funcionando
# Consolida: quick_test.sh + test_postgres_connection.py

set -e

echo "🧪 Teste Completo do OpenSAS"
echo "=" * 40

# Verificar se estamos no diretório correto
if [ ! -f "run.py" ]; then
    echo "❌ Execute este script no diretório raiz do OpenSAS"
    exit 1
fi

# ============================================================================
# 1. VERIFICAR SERVIÇOS
# ============================================================================
echo "📋 Verificando serviços..."

# PostgreSQL
if sudo systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL está rodando"
else
    echo "❌ PostgreSQL não está rodando"
    echo "   Execute: sudo systemctl start postgresql"
    exit 1
fi

# Redis
if sudo systemctl is-active --quiet redis; then
    echo "✅ Redis está rodando"
else
    echo "❌ Redis não está rodando"
    echo "   Execute: sudo systemctl start redis"
    exit 1
fi

# ============================================================================
# 2. VERIFICAR AMBIENTE PYTHON
# ============================================================================
echo "🐍 Verificando ambiente Python..."
if [ -d "venv" ]; then
    echo "✅ Virtual environment existe"
    source venv/bin/activate
else
    echo "❌ Virtual environment não existe"
    echo "   Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# ============================================================================
# 3. VERIFICAR CONFIGURAÇÃO
# ============================================================================
echo "📝 Verificando configuração..."
if [ -f ".env" ]; then
    echo "✅ Arquivo .env existe"
else
    echo "❌ Arquivo .env não existe"
    echo "   Execute: cp env.example .env"
    exit 1
fi

# ============================================================================
# 4. TESTAR CONEXÃO POSTGRESQL
# ============================================================================
echo "🔍 Testando conexão com PostgreSQL..."

# Teste básico de conexão
if python scripts/test_postgres_connection.py > /dev/null 2>&1; then
    echo "✅ Conexão com PostgreSQL OK"
else
    echo "❌ Erro na conexão com PostgreSQL"
    echo "   Execute: python scripts/test_postgres_connection.py"
    exit 1
fi

# ============================================================================
# 5. VERIFICAR API
# ============================================================================
echo "🌐 Verificando API..."
if curl -s http://localhost:9000/health > /dev/null 2>&1; then
    echo "✅ API está rodando"
    API_RUNNING=true
else
    echo "ℹ️  API não está rodando (normal se não foi iniciada)"
    API_RUNNING=false
fi

# ============================================================================
# 6. TESTE DETALHADO POSTGRESQL (OPCIONAL)
# ============================================================================
echo ""
echo "🔍 Teste detalhado PostgreSQL (opcional)..."
echo "Deseja executar teste detalhado? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Executando teste detalhado..."
    python scripts/test_postgres_connection.py
fi

echo ""
echo "🎉 Verificações básicas concluídas!"
echo ""

if [ "$API_RUNNING" = false ]; then
    echo "📋 Para iniciar a API:"
    echo "   1. source venv/bin/activate"
    echo "   2. python run.py"
    echo "   3. Acesse: http://localhost:9000/docs"
    echo ""
fi

echo "🔧 Comandos úteis:"
echo "   - Status serviços: sudo systemctl status postgresql redis"
echo "   - Testar PostgreSQL: psql -h localhost -U opensas_user -d opensas"
echo "   - Testar Redis: redis-cli ping"
echo "   - Logs PostgreSQL: sudo journalctl -u postgresql -f"
echo "   - Logs Redis: sudo journalctl -u redis -f"
echo ""
echo "📝 Informações de conexão:"
echo "   PostgreSQL: postgresql://opensas_user:opensas_password@localhost:5432/opensas"
echo "   Redis: redis://localhost:6379"
