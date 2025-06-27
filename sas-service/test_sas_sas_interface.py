#!/usr/bin/env python3
"""
Testa a interface pública SAS-SAS (WINNF TS-0096/3003)
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/v1.3"

CBSD_ID = "TEST-SN-001"
ZONE_ID = "ZONE-001"

cbsd_payload = {
    "id": CBSD_ID,
    "fccId": "TEST-FCC-001",
    "userId": "TEST-USER-001",
    "cbsdSerialNumber": CBSD_ID,
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

zone_payload = {
    "id": ZONE_ID,
    "name": "Zone Example",
    "type": "protected",
    "geometry": {"type": "Polygon", "coordinates": [[[0,0],[1,0],[1,1],[0,1],[0,0]]]}
}

def test_get_cbsd_not_found():
    print("🔍 GET /v1.3/cbsd/{id} (não existe)")
    r = requests.get(f"{BASE_URL}/cbsd/{CBSD_ID}")
    assert r.status_code == 404
    print("✅ 404 para CBSD inexistente")

def test_post_cbsd():
    print("🔍 POST /v1.3/cbsd/{id}")
    r = requests.post(f"{BASE_URL}/cbsd/{CBSD_ID}", json=cbsd_payload)
    assert r.status_code == 200
    print("✅ CBSD criado/atualizado")

def test_get_cbsd():
    print("🔍 GET /v1.3/cbsd/{id}")
    r = requests.get(f"{BASE_URL}/cbsd/{CBSD_ID}")
    assert r.status_code == 200
    data = r.json()
    assert data["cbsd"]["id"] == CBSD_ID
    print("✅ CBSD recuperado com sucesso")

def test_post_zone():
    print("🔍 POST /v1.3/zone/{id}")
    r = requests.post(f"{BASE_URL}/zone/{ZONE_ID}", json=zone_payload)
    assert r.status_code == 200
    print("✅ Zona criada/atualizada")

def test_get_zone():
    print("🔍 GET /v1.3/zone/{id}")
    r = requests.get(f"{BASE_URL}/zone/{ZONE_ID}")
    assert r.status_code == 200
    data = r.json()
    assert data["zone"]["id"] == ZONE_ID
    print("✅ Zona recuperada com sucesso")

def test_get_dump():
    print("🔍 GET /v1.3/dump")
    r = requests.get(f"{BASE_URL}/dump")
    assert r.status_code == 200
    print("✅ Full activity dump retornado")

def main():
    print("🧪 Testando interface SAS-SAS (WINNF TS-0096/3003)...\n")
    tests = [
        test_get_cbsd_not_found,
        test_post_cbsd,
        test_get_cbsd,
        test_post_zone,
        test_get_zone,
        test_get_dump
    ]
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Falha: {test.__name__}")
            sys.exit(1)
    print(f"\n🎉 {passed}/{len(tests)} testes SAS-SAS passaram!")

if __name__ == "__main__":
    main() 