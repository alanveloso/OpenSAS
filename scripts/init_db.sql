-- Script de inicialização do banco PostgreSQL para OpenSAS
-- Este script é executado automaticamente quando o container PostgreSQL é criado

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar schema se não existir
CREATE SCHEMA IF NOT EXISTS opensas;

-- Definir schema padrão
SET search_path TO opensas, public;

-- Comentário sobre o banco
COMMENT ON DATABASE opensas IS 'Banco de dados para o sistema OpenSAS (Spectrum Access System)';

-- Criar usuário específico para a aplicação (opcional)
-- CREATE USER opensas_app WITH PASSWORD 'opensas_app_password';
-- GRANT ALL PRIVILEGES ON SCHEMA opensas TO opensas_app;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA opensas TO opensas_app;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA opensas TO opensas_app;
