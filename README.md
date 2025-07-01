# OpenSAS - Spectrum Access System

Sistema de Acesso ao Espectro (SAS) compatível com WINNF TS-0096/3003 (SAS-SAS).

## 🚀 Funcionalidades

### Endpoints Implementados

#### Endpoints Públicos (WINNF TS-0096)
- **POST /v1.3/registration** - Registro de CBSD
- **POST /v1.3/grant** - Solicitação de grant de espectro
- **GET /v1.3/cbsd/{cbsd_id}** - Obter registro CBSD
- **POST /v1.3/cbsd/{cbsd_id}** - Atualizar registro CBSD
- **GET /v1.3/zone/{zone_id}** - Obter registro de zona
- **POST /v1.3/zone/{zone_id}** - Atualizar registro de zona
- **GET /v1.3/dump** - Full activity dump

#### Endpoints Administrativos
- **POST /sas/authorize** - Autorizar SAS
- **POST /sas/revoke** - Revogar SAS
- **GET /sas/{sas_address}/authorized** - Verificar autorização SAS

#### Endpoints de Monitoramento
- **GET /health** - Health check
- **GET /stats** - Estatísticas do sistema
- **GET /events/recent** - Eventos recentes

## 📋 Pré-requisitos

- Python 3.8+
- pip
- SQLite (incluído no Python)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd OpenSAS
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

## 🚀 Execução

### Desenvolvimento
```bash
python run.py
```

### Produção
```bash
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000
```

A API estará disponível em:
- **API**: http://localhost:9000
- **Documentação**: http://localhost:9000/docs
- **Health Check**: http://localhost:9000/health

## 🧪 Benchmarks JMeter

O projeto inclui benchmarks JMeter para testar a performance dos endpoints.

### Executar Benchmarks

1. Certifique-se de que o JMeter está instalado
2. Execute todos os benchmarks:
```bash
bash scripts/run_all_benchmarks.sh
```

Os resultados serão salvos em subpastas dentro de `results/` para cada cenário (low, medium, high, stress). A cada execução, a pasta anterior é movida para backup automaticamente.

#### Níveis de Carga
- **Low**: 2 usuários, 5 iterações
- **Medium**: 10 usuários, 10 iterações
- **High**: 50 usuários, 20 iterações
- **Stress**: 200 usuários, 50 iterações

## 📊 Estrutura do Projeto

```
OpenSAS/
├── src/
│   ├── api/
│   │   └── main.py              # Endpoints da API
│   ├── config/
│   │   └── settings.py          # Configurações
│   └── models/
│       ├── database.py          # Configuração do banco
│       ├── cbsd.py             # Modelo CBSD
│       ├── grant.py            # Modelo Grant
│       ├── sas_auth.py         # Modelo SAS Authorization
│       └── event.py            # Modelo Event
├── scripts/
│   └── run_all_benchmarks.sh   # Script para rodar todos os benchmarks
├── requirements.txt
├── run.py                      # Script de execução da API
├── manage.py                   # Script de administração do banco
```

## 🔧 Configuração

As configurações podem ser alteradas no arquivo `src/config/settings.py` ou através de variáveis de ambiente:

- `HOST`: Host do servidor (padrão: 0.0.0.0)
- `PORT`: Porta do servidor (padrão: 9000)
- `DEBUG`: Modo debug (padrão: False)
- `DATABASE_URL`: URL do banco de dados
- `LOG_LEVEL`: Nível de log (padrão: INFO)

## 📝 Modelos de Dados

### CBSD (Citizen Broadband Radio Service Device)
- Identificação FCC
- Número de série
- Categoria (A ou B)
- Interface aérea
- Capacidades de medição
- Localização (latitude, longitude, altura)
- Parâmetros da antena

### Grant (Concessão de Espectro)
- ID único da concessão
- Tipo de canal (GAA, PAL)
- Frequências (baixa, alta)
- Potência máxima (EIRP)
- Tempo de expiração
- Estado (GRANTED, AUTHORIZED, TERMINATED)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.

## 🗂️ Organização dos Resultados por Tipo de Requisição

Após rodar os benchmarks, você pode organizar os resultados `.jtl` em subpastas por tipo de requisição (ex: Authorize, Registration, Grant, etc.) usando o script:

```bash
python3 scripts/organize_results_by_request_type.py
```

Esse script percorre todas as pastas em `results/`, lê cada arquivo `.jtl` e separa as linhas por tipo de requisição (coluna `label`). Para cada tipo, é criada uma subpasta dentro do cenário correspondente, contendo um arquivo `.jtl` apenas com as linhas daquele tipo. O arquivo original é mantido intacto.

Exemplo de estrutura após rodar o script:

```
results/
  sas_full_flow_high/
    run_1_20250701_091324.jtl
    Authorize/
      run_1_20250701_091324.jtl
    Registration/
      run_1_20250701_091324.jtl
    ...
``` 