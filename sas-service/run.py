#!/usr/bin/env python3
"""
Script para executar a API do SAS
"""

import uvicorn
import os
import sys

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import settings

if __name__ == "__main__":
    print("🚀 Iniciando SAS (Spectrum Access System)...")
    print(f"📍 Host: {settings.host}")
    print(f"🔌 Porta: {settings.port}")
    print(f"🐛 Debug: {settings.debug}")
    print("")
    print("🌐 API disponível em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("")
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 