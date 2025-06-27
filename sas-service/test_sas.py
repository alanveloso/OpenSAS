#!/usr/bin/env python3
"""
Script de teste para o SAS
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Testar health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Status: {response.json()}")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_authorize_sas():
    """Testar autorização de SAS"""
    print("\n🔍 Testando autorização de SAS...")
    try:
        data = {"sas_address": "0x1234567890123456789012345678901234567890"}
        response = requests.post(f"{BASE_URL}/sas/authorize", json=data)
        if response.status_code == 200:
            print("✅ SAS autorizado com sucesso")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Falha ao autorizar SAS: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao autorizar SAS: {e}")
        return False

def test_check_authorization():
    """Testar verificação de autorização"""
    print("\n🔍 Testando verificação de autorização...")
    try:
        sas_address = "0x1234567890123456789012345678901234567890"
        response = requests.get(f"{BASE_URL}/sas/{sas_address}/authorized")
        if response.status_code == 200:
            result = response.json()
            print("✅ Verificação de autorização OK")
            print(f"   SAS {sas_address}: {result['authorized']}")
            return True
        else:
            print(f"❌ Falha na verificação: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def test_registration():
    """Testar registro de CBSD"""
    print("\n🔍 Testando registro de CBSD...")
    try:
        data = {
            "fccId": "TEST-FCC-001",
            "userId": "TEST-USER-001",
            "cbsdSerialNumber": "TEST-SN-001",
            "callSign": "TESTCALL",
            "cbsdCategory": "A",
            "airInterface": "E_UTRA",
            "measCapability": ["EUTRA_CARRIER_RSSI"],
            "eirpCapability": 47,
            "latitude": 375000000,
            "longitude": 1224000000,
            "height": 30,
            "heightType": "AGL",
            "indoorDeployment": False,
            "antennaGain": 15,
            "antennaBeamwidth": 360,
            "antennaAzimuth": 0,
            "groupingParam": "",
            "cbsdAddress": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
        }
        response = requests.post(f"{BASE_URL}/v1.3/registration", json=data)
        if response.status_code == 200:
            print("✅ CBSD registrado com sucesso")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Falha no registro: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro no registro: {e}")
        return False

def test_grant():
    """Testar solicitação de grant"""
    print("\n🔍 Testando solicitação de grant...")
    try:
        data = {
            "fccId": "TEST-FCC-001",
            "cbsdSerialNumber": "TEST-SN-001",
            "channelType": "GAA",
            "maxEirp": 47,
            "lowFrequency": 3550000000,
            "highFrequency": 3700000000,
            "requestedMaxEirp": 47,
            "requestedLowFrequency": 3550000000,
            "requestedHighFrequency": 3700000000,
            "grantExpireTime": 1750726000
        }
        response = requests.post(f"{BASE_URL}/v1.3/grant", json=data)
        if response.status_code == 200:
            print("✅ Grant solicitado com sucesso")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Falha na solicitação de grant: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na solicitação de grant: {e}")
        return False

def test_heartbeat():
    """Testar heartbeat"""
    print("\n🔍 Testando heartbeat...")
    try:
        data = {
            "fccId": "TEST-FCC-001",
            "cbsdSerialNumber": "TEST-SN-001",
            "grantId": "grant_TEST-FCC-001_TEST-SN-001",
            "transmitExpireTime": 1750726000
        }
        response = requests.post(f"{BASE_URL}/v1.3/heartbeat", json=data)
        if response.status_code == 200:
            print("✅ Heartbeat executado com sucesso")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Falha no heartbeat: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro no heartbeat: {e}")
        return False

def test_stats():
    """Testar estatísticas"""
    print("\n🔍 Testando estatísticas...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            print("✅ Estatísticas obtidas com sucesso")
            print(f"   Stats: {response.json()}")
            return True
        else:
            print(f"❌ Falha ao obter estatísticas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
        return False

def test_events():
    """Testar eventos recentes"""
    print("\n🔍 Testando eventos recentes...")
    try:
        response = requests.get(f"{BASE_URL}/events/recent")
        if response.status_code == 200:
            result = response.json()
            print("✅ Eventos obtidos com sucesso")
            print(f"   Total de eventos: {result['count']}")
            return True
        else:
            print(f"❌ Falha ao obter eventos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao obter eventos: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("🧪 Iniciando testes do SAS...")
    print("=" * 50)
    
    tests = [
        test_health,
        test_authorize_sas,
        test_check_authorization,
        test_registration,
        test_grant,
        test_heartbeat,
        test_stats,
        test_events
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Pequena pausa entre testes
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! SAS está funcionando corretamente.")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 