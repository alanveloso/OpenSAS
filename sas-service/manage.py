#!/usr/bin/env python3
"""
Script para gerenciar o banco de dados do SAS
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models.database import Base, engine
from src.config.settings import settings

def init_db():
    """Inicializar banco de dados"""
    print("🔧 Inicializando banco de dados do SAS...")
    
    try:
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar conexão
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Teste simples de conexão
        result = db.execute(text("SELECT 1")).fetchone()
        if result:
            print("✅ Conexão com banco de dados estabelecida!")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        sys.exit(1)

def reset_db():
    """Resetar banco de dados (apagar todas as tabelas e recriar)"""
    print("⚠️  Resetando banco de dados...")
    
    try:
        # Apagar todas as tabelas
        Base.metadata.drop_all(bind=engine)
        print("🗑️  Tabelas removidas!")
        
        # Recriar tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas recriadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_db()
        elif command == "reset":
            reset_db()
        else:
            print("Comandos disponíveis:")
            print("  python manage.py init   - Inicializar banco")
            print("  python manage.py reset  - Resetar banco")
    else:
        # Comando padrão: inicializar
        init_db() 