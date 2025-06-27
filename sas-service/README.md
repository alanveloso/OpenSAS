# SAS (Spectrum Access System)

Sistema SAS (Spectrum Access System) implementado como um serviço web compatível com WINNF TS-0096/3003 (SAS-SAS) e WINNF TS-0016 (SAS-CBSD).

## 🎯 Objetivo

Este SAS implementa:
- **Interface pública SAS-SAS** (WINNF TS-0096/3003): para comunicação entre sistemas SAS.
- **Interface administrativa interna**: para controle e gestão do sistema.
- **(Opcional) Interface SAS-CBSD**: para integração com CBSDs, se necessário.

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Outro SAS     │    │  SAS Service     │    │  Database       │
│                 │◄──►│  (FastAPI)       │◄──►│  (PostgreSQL/   │
│                 │    │                  │    │   SQLite)       │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Cache Layer     │
                       │  (Redis)         │
                       └──────────────────┘
```

## 🚀 Interfaces Disponíveis

### 1. Interface Pública SAS-SAS (WINNF TS-0096/3003)
> **Apenas estes endpoints devem ser expostos para comunicação entre SASs.**

- `GET /v1.3/cbsd/{id}` — Obter registro CBSD
- `POST /v1.3/cbsd/{id}` — Atualizar/criar registro CBSD
- `GET /v1.3/zone/{id}` — Obter registro de zona
- `POST /v1.3/zone/{id}` — Atualizar/criar registro de zona
- `GET /v1.3/dump` — Full activity dump

> **Obs:** Expanda para outros tipos (ex: `/coordination`, `/zone`, `/dump`) conforme o padrão WINNF.

### 2. Interface Administrativa Interna (NÃO faz parte do padrão WINNF SAS-SAS)
> **Apenas para uso interno/administração.**

- `POST /sas/authorize` — Autorizar SAS
- `POST /sas/revoke` — Revogar SAS
- `GET /sas/{sas_address}/authorized` — Verificar autorização de SAS

### 3. Monitoramento (opcional)
- `GET /health` — Health check
- `GET /stats` — Estatísticas do sistema
- `GET /events/recent` — Eventos recentes

### 4. (Opcional) Interface SAS-CBSD (WINNF TS-0016)
> **Não faz parte da interface SAS-SAS.**

- `POST /v1.3/registration`, `/grant`, `/heartbeat`, `/relinquishment`, `/deregistration`, ...

## ❗️ Diferença entre SAS-SAS e SAS-CBSD

| Interface         | Especificação         | Caminhos padrão SAS-SAS                | Caminhos padrão SAS-CBSD           |
|-------------------|----------------------|----------------------------------------|------------------------------------|
| SAS ↔ SAS         | WINNF-TS-0096/3003   | `/v1.3/cbsd/{id}`, `/zone/{id}`, ...   | —                                  |
| SAS ↔ CBSD        | WINNF-TS-0016        | —                                      | `/v1.3/registration`, `/grant`, ...|

- **SAS-SAS:** GET e POST, caminhos por tipo de registro (ex: `/cbsd/{id}`), comunicação entre SASs.
- **SAS-CBSD:** Apenas POST, caminhos por operação (ex: `/registration`), comunicação com dispositivos.

## 🛠️ Setup

```bash
cd sas-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py init
python run.py
```

## 📚 Exemplos de Uso (SAS-SAS)

**Obter registro CBSD:**
```bash
curl http://localhost:8000/v1.3/cbsd/TEST-SN-001
```

**Atualizar/criar registro CBSD:**
```bash
curl -X POST http://localhost:8000/v1.3/cbsd/TEST-SN-001 \
  -H "Content-Type: application/json" \
  -d '{
    "id": "TEST-SN-001",
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
    "indoorDeployment": false,
    "antennaGain": 15,
    "antennaBeamwidth": 360,
    "antennaAzimuth": 0,
    "groupingParam": "",
    "cbsdIdentifier": "CBSD-TEST-001"
  }'
```

**Obter registro de zona:**
```bash
curl http://localhost:8000/v1.3/zone/ZONE-001
```

**Full activity dump:**
```bash
curl http://localhost:8000/v1.3/dump
```

## 🔒 Interface Administrativa (exemplo)
```bash
curl -X POST http://localhost:8000/sas/authorize -H "Content-Type: application/json" -d '{"sas_address": "0x123..."}'
curl http://localhost:8000/sas/0x123.../authorized
```

## 📝 Observações
- **Apenas a interface SAS-SAS deve ser exposta para outros SASs.**
- Endpoints administrativos e SAS-CBSD são para uso interno ou integração opcional.
- Consulte a especificação WINNF TS-0096/3003 para detalhes completos dos endpoints SAS-SAS.

## 🔗 Links Úteis
- [WINNF TS-0096/3003 (SAS-SAS)](https://winnforum.org/) 
- [WINNF TS-0016 (SAS-CBSD)](https://winnforum.org/) 

## 🧪 Testes de Performance

### Executar Benchmarks
```bash
# Usar JMeter ou similar para testes de carga
jmeter -n -t test_plan.jmx -l results.jtl
```

### Métricas de Performance
- **Throughput**: Requisições/segundo
- **Response Time**: Tempo médio de resposta
- **Error Rate**: Taxa de erro
- **CPU/Memory**: Uso de recursos

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Banco de Dados
DATABASE_URL=sqlite:///./sas_service.db
# DATABASE_URL=postgresql://user:pass@localhost/sas_db

# Cache
REDIS_URL=redis://localhost:6379
CACHE_TTL=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/sas_service.log

# Performance
WORKERS=4
MAX_CONNECTIONS=1000
```

## 📁 Estrutura do Projeto

```
sas-service/
├── src/
│   ├── api/              # API REST FastAPI
│   ├── models/           # Modelos de dados
│   ├── services/         # Lógica de negócio
│   ├── database/         # Camada de dados
│   ├── cache/            # Camada de cache
│   └── utils/            # Utilitários
├── tests/                # Testes unitários
├── scripts/              # Scripts utilitários
├── logs/                 # Logs da aplicação
├── data/                 # Dados de exemplo
├── requirements.txt      # Dependências
├── run.py               # Ponto de entrada
└── README.md            # Este arquivo
```

## 🎯 Próximos Passos

1. **Implementar autenticação JWT**
2. **Adicionar rate limiting**
3. **Implementar métricas Prometheus**
4. **Containerização com Docker**
5. **Deploy em Kubernetes**
6. **Certificação WINNF**

## 📊 Especificações Técnicas

### CBRS Band
- **Frequência**: 3550-3700 MHz
- **Canais**: GAA (General Authorized Access) e PAL (Priority Access License)
- **EIRP**: Até 47 dBm/MHz

### CBSD Categories
- **Category A**: Dispositivos de baixa potência (≤ 30 dBm/MHz)
- **Category B**: Dispositivos de alta potência (≤ 47 dBm/MHz)

## 🔗 Links Úteis

- [Documentação da API](docs/API.md)
- [Guia de Performance](docs/PERFORMANCE.md)
- [Especificações WINNF](https://winnforum.org/) 