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
- PostgreSQL 12+ (recomendado) ou SQLite (desenvolvimento)
- Redis (opcional, para cache)

## 🛠️ Instalação

### Opção 1: Configuração Rápida (Recomendada)

Execute o script de configuração completa:

```bash
# Clone o repositório
git clone https://github.com/alanveloso/OpenSAS
cd OpenSAS

# Execute a configuração automática
bash scripts/setup_environment.sh
```

Este script irá:
1. ✅ Instalar PostgreSQL
2. ✅ Instalar Redis
3. ✅ Criar arquivo .env
4. ✅ Instalar dependências Python
5. ✅ Testar conexões
6. ✅ Inicializar banco de dados

### Opção 2: Configuração Manual

#### 1. Configurar PostgreSQL

```bash
# Instalar PostgreSQL
bash scripts/setup_postgres_local.sh

# Ou instalar manualmente:
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql postgresql-server
sudo postgresql-setup initdb

# Fedora
sudo dnf install postgresql postgresql-server
sudo postgresql-setup --initdb
```

#### 2. Configurar Redis (Opcional)

```bash
# Instalar Redis
bash scripts/setup_redis_local.sh

# Ou instalar manualmente:
# Ubuntu/Debian
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# Fedora
sudo dnf install redis
```

#### 3. Configurar Ambiente Python

```bash
# Criar virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp env.example .env
```

#### 4. Testar e Inicializar

```bash
# Testar conexão
python scripts/test_postgres_connection.py

# Inicializar banco de dados
python manage.py init
```

## 🚀 Execução

### Desenvolvimento
```bash
# Ativar virtual environment
source venv/bin/activate

# Executar API
python run.py
```

### Produção
```bash
# Com PostgreSQL
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000

# Com SQLite (desenvolvimento)
python run.py
```

A API estará disponível em:
- **API**: http://localhost:9000
- **Documentação**: http://localhost:9000/docs
- **Health Check**: http://localhost:9000/health

## 🧪 Testando a Configuração

### Teste Rápido
```bash
bash scripts/quick_test.sh
```

### Teste Detalhado
```bash
python scripts/test_postgres_connection.py
```

## 🔧 Configurações de Banco de Dados

### PostgreSQL (Recomendado)

**Informações de Conexão:**
- Host: `localhost`
- Porta: `5432`
- Banco: `opensas`
- Usuário: `opensas_user`
- Senha: `opensas_password`
- URL: `postgresql://opensas_user:opensas_password@localhost:5432/opensas`

**Comandos Úteis:**
```bash
# Status do serviço
sudo systemctl status postgresql

# Conectar ao banco
psql -h localhost -U opensas_user -d opensas

# Reiniciar serviço
sudo systemctl restart postgresql
```

### SQLite (Desenvolvimento)

Para desenvolvimento rápido, o sistema também suporta SQLite:

```bash
# Configurar para SQLite
export DATABASE_URL="sqlite:///./sas_service.db"
```

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
│   ├── setup_environment.sh    # Script de configuração completa
│   ├── setup_postgres_local.sh # Script para PostgreSQL
│   ├── setup_redis_local.sh    # Script para Redis
│   ├── test_postgres_connection.py # Teste de conexão
│   └── quick_test.sh          # Teste rápido
├── requirements.txt
├── run.py                      # Script de execução da API
├── manage.py                   # Script de administração do banco
├── env.example                 # Exemplo de variáveis de ambiente
├── SETUP_LOCAL.md             # Documentação detalhada
└── POSTGRES_SETUP.md          # Guia PostgreSQL
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