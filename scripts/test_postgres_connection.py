#!/usr/bin/env python3
"""
Script para testar a conexão com PostgreSQL
"""

import psycopg2
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config.settings import settings

def test_postgres_connection():
    """Testa a conexão com PostgreSQL"""
    print("🔍 Testando conexão com PostgreSQL...")
    
    try:
        # Tentar conectar usando a URL do settings
        print(f"📡 Tentando conectar: {settings.database_url}")
        
        conn = psycopg2.connect(settings.database_url)
        cursor = conn.cursor()
        
        # Teste básico
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conexão bem-sucedida!")
        print(f"📋 Versão do PostgreSQL: {version[0]}")
        
        # Teste de schema
        cursor.execute("SELECT current_schema();")
        schema = cursor.fetchone()
        print(f"📁 Schema atual: {schema[0]}")
        
        # Teste de extensões
        cursor.execute("SELECT extname FROM pg_extension;")
        extensions = cursor.fetchall()
        print(f"🔧 Extensões instaladas: {[ext[0] for ext in extensions]}")
        
        cursor.close()
        conn.close()
        
        print("🎉 Todos os testes passaram!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erro de conexão: {e}")
        print("\n💡 Possíveis soluções:")
        print("   1. Verifique se o PostgreSQL está rodando: sudo systemctl status postgresql")
        print("   2. Verifique se o usuário e senha estão corretos")
        print("   3. Verifique se o banco 'opensas' existe")
        print("   4. Execute: sudo systemctl restart postgresql")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_sqlalchemy_connection():
    """Testa a conexão via SQLAlchemy"""
    print("\n🔍 Testando conexão via SQLAlchemy...")
    
    try:
        from src.models.database import engine
        from sqlalchemy import text
        
        # Teste de conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ SQLAlchemy conectado! Teste: {row[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no SQLAlchemy: {e}")
        return False

def create_tables():
    """Cria as tabelas se não existirem"""
    print("\n🔨 Criando tabelas...")
    
    try:
        from src.models.database import Base, engine
        from sqlalchemy import text
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar tabelas criadas
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Tabelas criadas: {tables}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Configuração PostgreSQL para OpenSAS")
    print("=" * 50)
    
    # Teste 1: Conexão direta
    if not test_postgres_connection():
        sys.exit(1)
    
    # Teste 2: Conexão via SQLAlchemy
    if not test_sqlalchemy_connection():
        sys.exit(1)
    
    # Teste 3: Criação de tabelas
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 Todos os testes passaram! PostgreSQL está configurado corretamente.")
    print("\n📝 Próximos passos:")
    print("   1. Execute: python run.py")
    print("   2. Acesse: http://localhost:9000/docs")
    print("   3. Teste os endpoints da API")
