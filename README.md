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
bash scripts/setup.sh
```

Este script irá:
1. ✅ Instalar PostgreSQL
2. ✅ Instalar Redis
3. ✅ Criar arquivo .env
4. ✅ Instalar dependências Python
5. ✅ Testar conexões
6. ✅ Inicializar banco de dados

### Opção 2: Instalação Manual Detalhada

#### Passo 1: Clone o Repositório
```bash
git clone https://github.com/alanveloso/OpenSAS
cd OpenSAS
```

#### Passo 2: Instalar PostgreSQL

**Ubuntu/Debian:**
```bash
# Atualizar repositórios
sudo apt-get update

# Instalar PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib postgresql-client

# Iniciar e habilitar o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar se está rodando
sudo systemctl status postgresql
```

**CentOS/RHEL:**
```bash
# Instalar PostgreSQL
sudo yum install -y postgresql postgresql-server postgresql-contrib

# Inicializar banco de dados
sudo postgresql-setup initdb

# Iniciar e habilitar o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Fedora:**
```bash
# Instalar PostgreSQL
sudo dnf install -y postgresql postgresql-server postgresql-contrib

# Inicializar banco de dados
sudo postgresql-setup --initdb

# Iniciar e habilitar o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Passo 3: Configurar PostgreSQL

```bash
# Conectar como usuário postgres
sudo -u postgres psql

# Criar usuário e banco de dados
CREATE USER opensas_user WITH PASSWORD 'opensas_password';
CREATE DATABASE opensas OWNER opensas_user;
GRANT ALL PRIVILEGES ON DATABASE opensas TO opensas_user;

# Conectar ao banco opensas
\c opensas

# Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

# Criar schema
CREATE SCHEMA IF NOT EXISTS opensas;
GRANT ALL PRIVILEGES ON SCHEMA opensas TO opensas_user;

# Configurar search_path
ALTER DATABASE opensas SET search_path TO opensas, public;

# Sair do psql
\q
```

#### Passo 4: Configurar Acesso Local (Opcional)

Para desenvolvimento, você pode configurar acesso local:

```bash
# Editar configuração do PostgreSQL
sudo nano /etc/postgresql/*/main/postgresql.conf
# Alterar: listen_addresses = 'localhost'

sudo nano /etc/postgresql/*/main/pg_hba.conf
# Alterar: local all all md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

#### Passo 5: Instalar Redis (Opcional)

**Ubuntu/Debian:**
```bash
sudo apt-get install -y redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**CentOS/RHEL:**
```bash
sudo yum install -y redis
sudo systemctl start redis
sudo systemctl enable redis
```

**Fedora:**
```bash
sudo dnf install -y redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### Passo 6: Configurar Ambiente Python

```bash
# Criar virtual environment
python3 -m venv venv

# Ativar virtual environment
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

#### Passo 7: Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar configurações (opcional)
nano .env
```

**Conteúdo recomendado do .env:**
```env
# Servidor
HOST=0.0.0.0
PORT=9000
DEBUG=false

# Banco de dados
DATABASE_URL=postgresql://opensas_user:opensas_password@localhost:5432/opensas

# Redis (opcional)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```

#### Passo 8: Testar Conexões

```bash
# Testar PostgreSQL
python scripts/test.sh

# Ou testar manualmente:
psql -h localhost -U opensas_user -d opensas -c "SELECT version();"
```

#### Passo 9: Inicializar Banco de Dados

```bash
# Ativar virtual environment (se necessário)
source venv/bin/activate

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
bash scripts/test.sh
```

### Teste Manual
```bash
# Testar PostgreSQL
psql -h localhost -U opensas_user -d opensas -c "SELECT 1;"

# Testar Redis
redis-cli ping

# Testar API
curl http://localhost:9000/health
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

# Ver logs
sudo journalctl -u postgresql -f
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
bash scripts/benchmark.sh
```

Os resultados serão salvos em subpastas dentro de `results/` para cada cenário (low, medium, high, stress, extreme).

#### Níveis de Carga Padronizados
- **LOW**: 2 threads x 10 loops = 120 requisições
- **MEDIUM**: 10 threads x 10 loops = 600 requisições
- **HIGH**: 30 threads x 10 loops = 1,800 requisições
- **STRESS**: 50 threads x 10 loops = 3,000 requisições
- **EXTREME**: 100 threads x 10 loops = 6,000 requisições

### Análise de Resultados

```bash
# Executar análise dos resultados
python scripts/analyze_results.py
```

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
│   ├── setup.sh                # Script de configuração completa
│   ├── test.sh                 # Script de teste e diagnóstico
│   ├── benchmark.sh            # Script de benchmarks JMeter
│   └── analyze_results.py      # Análise de resultados
├── plans/
│   ├── sas_full_flow_low.jmx   # Plano LOW
│   ├── sas_full_flow_medium.jmx # Plano MEDIUM
│   ├── sas_full_flow_high.jmx  # Plano HIGH
│   ├── sas_full_flow_stress.jmx # Plano STRESS
│   └── sas_full_flow_extreme.jmx # Plano EXTREME
├── results/                    # Resultados dos benchmarks
├── analysis_output/            # Gráficos e estatísticas
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

## 🔧 Troubleshooting

### Problemas Comuns

**1. Erro de conexão com PostgreSQL:**
```bash
# Verificar se o serviço está rodando
sudo systemctl status postgresql

# Verificar logs
sudo journalctl -u postgresql -f

# Reiniciar serviço
sudo systemctl restart postgresql
```

**2. Erro de permissão no PostgreSQL:**
```bash
# Verificar configuração de autenticação
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

**3. Erro de dependências Python:**
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

**4. Erro de porta em uso:**
```bash
# Verificar processos na porta 9000
sudo lsof -i :9000

# Matar processo se necessário
sudo kill -9 <PID>
```

### Comandos Úteis

```bash
# Status dos serviços
sudo systemctl status postgresql redis

# Logs em tempo real
sudo journalctl -u postgresql -f
sudo journalctl -u redis -f

# Testar conexões
psql -h localhost -U opensas_user -d opensas -c "SELECT 1;"
redis-cli ping

# Verificar estrutura do projeto
tree -L 2
``` 