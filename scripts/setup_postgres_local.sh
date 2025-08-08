#!/bin/bash

# Script para configurar PostgreSQL localmente para OpenSAS
# Este script instala e configura o PostgreSQL no sistema Linux

set -e

echo "🚀 Configurando PostgreSQL localmente para OpenSAS..."

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
echo ""
echo "📋 Informações de conexão:"
echo "   Host: localhost"
echo "   Porta: 5432"
echo "   Banco: opensas"
echo "   Usuário: opensas_user"
echo "   Senha: opensas_password"
echo ""
echo "🔗 String de conexão:"
echo "   postgresql://opensas_user:opensas_password@localhost:5432/opensas"
echo ""
echo "📝 Para testar a conexão:"
echo "   psql -h localhost -U opensas_user -d opensas"
echo ""
echo "🎉 Configuração concluída! Agora você pode executar a API OpenSAS."
