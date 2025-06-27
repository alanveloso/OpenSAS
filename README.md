# SAS Registry (SAS-SAS Interface)

Este projeto implementa um Spectrum Access System (SAS) tradicional, com interface compatível com o padrão WINNF SAS-SAS (TS-0096/3003), para fins de benchmarking e integração. Não há dependências de blockchain ou smart contracts.

## Sumário
- [Arquitetura](#arquitetura)
- [Endpoints SAS-SAS](#endpoints-sas-sas)
- [Setup do Serviço Python](#setup-do-serviço-python)
- [Execução de Benchmarks JMeter](#execução-de-benchmarks-jmeter)
- [Testes Automatizados](#testes-automatizados)

---

## Arquitetura

```
┌───────────────┐    REST    ┌───────────────┐
│   SAS Peer    │◄──────────►│   SAS Python  │
└───────────────┘            └───────────────┘
```

- **SAS Python**: Serviço FastAPI/SQLAlchemy, persistência local (SQLite ou outro DB relacional).
- **Compatível com JMeter**: Endpoints e payloads compatíveis com planos de benchmark WINNF SAS-SAS.

---

## Endpoints SAS-SAS

- `GET /v1.3/cbsd/{id}`: Consulta informações de um CBSD
- `POST /v1.3/cbsd/{id}`: Atualiza informações de um CBSD
- `GET /v1.3/zone/{id}`: Consulta informações de uma zona
- `POST /v1.3/zone/{id}`: Atualiza informações de uma zona
- `GET /v1.3/dump`: Retorna dump de dados SAS

Todos os endpoints aceitam/retornam JSON conforme especificação WINNF.

---

## Setup do Serviço Python

```bash
cd sas-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

O serviço estará disponível em `http://localhost:8000`.

---

## Execução de Benchmarks JMeter

Os planos JMeter estão em `benchmark/jmeter/plans/`.

Exemplo de execução:
```bash
cd benchmark/jmeter/scripts
jmeter -n -t ../plans/sas_sas_zone_get_low.jmx -l ../plans/results_zone_get_low.jtl
```

Resultados são salvos em arquivos `.jtl` para análise posterior.

---

## Testes Automatizados

Testes unitários e de integração estão em `sas-service/` e `middleware/tests/`.

Exemplo de execução:
```bash
cd sas-service
pytest
```

---

## Observações
- Este projeto não utiliza blockchain, smart contracts ou qualquer dependência Ethereum/Besu.
- Foco total em benchmarking e interoperabilidade SAS-SAS.

---
