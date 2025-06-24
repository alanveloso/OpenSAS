#!/bin/bash

echo "🧪 Teste Básico da API SAS Shared Registry (Sem Blockchain)"
echo "=========================================================="
echo ""

# Verificar se jq está instalado
if ! command -v jq &> /dev/null; then
    echo "❌ jq não está instalado. Instalando..."
    sudo apt-get update && sudo apt-get install -y jq
fi

# Função para aguardar um pouco entre requests
wait_a_bit() {
    echo "⏳ Aguardando 2 segundos..."
    sleep 2
}

# 1. Health Check
echo "1️⃣ Health Check"
echo "---------------"
curl -s http://localhost:8000/health | jq '.'
echo ""

wait_a_bit

# 2. Listar todos os CBSDs (funciona sem blockchain)
echo "2️⃣ Listar todos os CBSDs"
echo "------------------------"
curl -s http://localhost:8000/cbsd | jq '.'
echo ""

wait_a_bit

# 3. Ver eventos recentes (funciona sem blockchain)
echo "3️⃣ Ver eventos recentes"
echo "----------------------"
curl -s http://localhost:8000/events/recent | jq '.'
echo ""

wait_a_bit

# 4. Teste de erro - CBSD inexistente (funciona sem blockchain)
echo "4️⃣ Teste de erro - CBSD inexistente"
echo "------------------------------------"
curl -s http://localhost:8000/cbsd/999 | jq '.'
echo ""

wait_a_bit

# 5. Endpoint raiz
echo "5️⃣ Endpoint raiz"
echo "----------------"
curl -s http://localhost:8000/ | jq '.'
echo ""

echo "✅ Teste básico concluído!"
echo ""
echo "📋 Resultado:"
echo "   - ✅ Endpoints que funcionam sem blockchain testados"
echo "   - ⚠️  Endpoints que precisam de blockchain foram pulados"
echo ""
echo "🚀 Para testar com blockchain:"
echo "   1. Iniciar Hardhat: npx hardhat node"
echo "   2. Deploy contrato: npx hardhat run scripts/deploy-sas-shared-registry.js --network localhost"
echo "   3. Atualizar .env com endereço do contrato"
echo "   4. Reiniciar API: python3 run.py"
echo "   5. Executar teste completo: ./scripts/test_blockchain.sh"
echo ""
echo "📚 Documentação disponível em:"
echo "   - docs/API_DOCS.md"
echo "   - README.md" 