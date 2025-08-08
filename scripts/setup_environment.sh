#!/bin/bash

# Script para configurar o ambiente completo do OpenSAS localmente

set -e

echo "🚀 Configurando ambiente completo do OpenSAS..."
echo "=" * 50

# Verificar se estamos no diretório correto
if [ ! -f "run.py" ]; then
    echo "❌ Execute este script no diretório raiz do OpenSAS"
    exit 1
fi

# 1. Instalar PostgreSQL
echo "📦 Passo 1: Instalando PostgreSQL..."
bash scripts/setup_postgres_local.sh

# 2. Instalar Redis
echo "📦 Passo 2: Instalando Redis..."
bash scripts/setup_redis_local.sh

# 3. Criar arquivo .env
echo "📝 Passo 3: Criando arquivo .env..."
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Arquivo .env criado!"
else
    echo "ℹ️  Arquivo .env já existe"
fi

# 4. Instalar dependências Python
echo "🐍 Passo 4: Instalando dependências Python..."
if [ -d "venv" ]; then
    echo "ℹ️  Virtual environment já existe"
    source venv/bin/activate
else
    echo "🔧 Criando virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

pip install -r requirements.txt

# 5. Testar conexão com PostgreSQL
echo "🔍 Passo 5: Testando conexão com PostgreSQL..."
python scripts/test_postgres_connection.py

# 6. Inicializar banco de dados
echo "🗄️  Passo 6: Inicializando banco de dados..."
python manage.py init

echo ""
echo "🎉 Configuração completa finalizada!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Ative o virtual environment: source venv/bin/activate"
echo "   2. Execute a API: python run.py"
echo "   3. Acesse a documentação: http://localhost:9000/docs"
echo "   4. Teste os endpoints da API"
echo ""
echo "🔧 Comandos úteis:"
echo "   - Status PostgreSQL: sudo systemctl status postgresql"
echo "   - Status Redis: sudo systemctl status redis"
echo "   - Conectar PostgreSQL: psql -h localhost -U opensas_user -d opensas"
echo "   - Testar Redis: redis-cli ping"
echo ""
echo "📝 Informações de conexão:"
echo "   PostgreSQL: postgresql://opensas_user:opensas_password@localhost:5432/opensas"
echo "   Redis: redis://localhost:6379"
