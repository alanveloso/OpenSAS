#!/bin/bash

# Script Master para configurar o ambiente completo do OpenSAS localmente
# Consolida: setup_environment.sh + setup_postgres_local.sh + setup_redis_local.sh + test_postgres_connection.py

set -e

echo "🚀 Configurando ambiente completo do OpenSAS..."
echo "=" * 50

# Verificar se estamos no diretório correto
if [ ! -f "run.py" ]; then
    echo "❌ Execute este script no diretório raiz do OpenSAS"
    exit 1
fi

# ============================================================================
# 1. INSTALAR POSTGRESQL
# ============================================================================
echo "📦 Passo 1: Instalando PostgreSQL..."

# Verificar se estamos no Ubuntu/Debian
if command -v apt-get &> /dev/null; then
    echo "📦 Instalando PostgreSQL via apt..."
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib postgresql-client
    
elif command -v yum &> /dev/null; then
    echo "📦 Instalando PostgreSQL via yum..."
    sudo yum install -y postgresql postgresql-server postgresql-contrib
    sudo postgresql-setup initdb
    
elif command -v dnf &> /dev/null; then
    echo "📦 Instalando PostgreSQL via dnf..."
    sudo dnf install -y postgresql postgresql-server postgresql-contrib
    sudo postgresql-setup --initdb
    
else
    echo "❌ Sistema não suportado. Por favor, instale PostgreSQL manualmente."
    exit 1
fi

# Iniciar e habilitar o serviço PostgreSQL
echo "🔧 Configurando serviço PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar se o serviço está rodando
if sudo systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL está rodando!"
else
    echo "❌ Erro ao iniciar PostgreSQL"
    exit 1
fi

# Criar usuário e banco de dados
echo "👤 Criando usuário e banco de dados..."
sudo -u postgres psql << EOF
-- Criar usuário
CREATE USER opensas_user WITH PASSWORD 'opensas_password';

-- Criar banco de dados
CREATE DATABASE opensas OWNER opensas_user;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE opensas TO opensas_user;

-- Conectar ao banco opensas
\c opensas

-- Criar extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar schema
CREATE SCHEMA IF NOT EXISTS opensas;
GRANT ALL PRIVILEGES ON SCHEMA opensas TO opensas_user;

-- Configurar search_path
ALTER DATABASE opensas SET search_path TO opensas, public;

-- Comentário sobre o banco
COMMENT ON DATABASE opensas IS 'Banco de dados para o sistema OpenSAS (Spectrum Access System)';

-- Sair
\q
EOF

echo "✅ Banco de dados configurado com sucesso!"

# Configurar acesso local (opcional - para desenvolvimento)
echo "🔧 Configurando acesso local..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" /etc/postgresql/*/main/postgresql.conf
sudo sed -i "s/local   all             all                                     peer/local   all             all                                     md5/" /etc/postgresql/*/main/pg_hba.conf

# Reiniciar PostgreSQL para aplicar mudanças
sudo systemctl restart postgresql

echo "✅ PostgreSQL configurado com sucesso!"

# ============================================================================
# 2. INSTALAR REDIS
# ============================================================================
echo "📦 Passo 2: Instalando Redis..."

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
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verificar se o serviço está rodando
if sudo systemctl is-active --quiet redis-server; then
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

# ============================================================================
# 3. CONFIGURAR PYTHON E DEPENDÊNCIAS
# ============================================================================
echo "🐍 Passo 3: Configurando Python e dependências..."

# Criar arquivo .env
echo "📝 Criando arquivo .env..."
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Arquivo .env criado!"
else
    echo "ℹ️  Arquivo .env já existe"
fi

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
if [ -d "venv" ]; then
    echo "ℹ️  Virtual environment já existe"
    source venv/bin/activate
else
    echo "🔧 Criando virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

pip install -r requirements.txt

# ============================================================================
# 4. TESTAR CONEXÕES
# ============================================================================
echo "🔍 Passo 4: Testando conexões..."

# Testar PostgreSQL
echo "🔍 Testando conexão com PostgreSQL..."
if PGPASSWORD=opensas_password psql -h localhost -U opensas_user -d opensas -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Conexão com PostgreSQL OK"
else
    echo "❌ Erro na conexão com PostgreSQL"
    echo "   Verifique: psql -h localhost -U opensas_user -d opensas"
fi

# ============================================================================
# 5. INICIALIZAR BANCO DE DADOS
# ============================================================================
echo "🗄️  Passo 5: Inicializando banco de dados..."
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
