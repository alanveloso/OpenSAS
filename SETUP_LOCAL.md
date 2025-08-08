# 🚀 Configuração Local do OpenSAS

Este guia explica como configurar o OpenSAS localmente com PostgreSQL e Redis.

## 📋 Pré-requisitos

- Linux (Ubuntu/Debian, CentOS/RHEL, ou Fedora)
- Python 3.8+
- Acesso sudo para instalar serviços

## 🎯 Configuração Rápida

### Opção 1: Configuração Automática (Recomendada)

Execute o script de configuração completa:

```bash
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

Se preferir configurar manualmente:

#### 1. Instalar PostgreSQL
```bash
bash scripts/setup_postgres_local.sh
```

#### 2. Instalar Redis
```bash
bash scripts/setup_redis_local.sh
```

#### 3. Configurar ambiente Python
```bash
# Criar virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

#### 4. Criar arquivo .env
```bash
cp env.example .env
```

#### 5. Testar conexão
```bash
python scripts/test_postgres_connection.py
```

#### 6. Inicializar banco
```bash
python manage.py init
```

## 🔧 Configurações de Banco de Dados

### PostgreSQL

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

### Redis

**Informações de Conexão:**
- Host: `localhost`
- Porta: `6379`
- URL: `redis://localhost:6379`

**Comandos Úteis:**
```bash
# Status do serviço
sudo systemctl status redis

# Testar conexão
redis-cli ping

# Reiniciar serviço
sudo systemctl restart redis
```

## 🚀 Executando a API

### 1. Ativar Virtual Environment
```bash
source venv/bin/activate
```

### 2. Executar API
```bash
python run.py
```

### 3. Acessar Documentação
- **API**: http://localhost:9000
- **Documentação**: http://localhost:9000/docs
- **Health Check**: http://localhost:9000/health

## 🧪 Testando a API

### 1. Autorizar SAS
```bash
curl -X POST "http://localhost:9000/sas/authorize" \
  -H "Content-Type: application/json" \
  -d '{"sas_address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"}'
```

### 2. Registrar CBSD
```bash
curl -X POST "http://localhost:9000/v1.3/registration" \
  -H "Content-Type: application/json" \
  -H "X-SAS-Address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266" \
  -d '{
    "fccId": "FCC-TEST-001",
    "userId": "USER-TEST-001",
    "cbsdSerialNumber": "CBSD-TEST-001",
    "callSign": "CALL1",
    "cbsdCategory": "A",
    "airInterface": "LTE",
    "measCapability": ["CAT_A"],
    "eirpCapability": 30,
    "latitude": 10,
    "longitude": 20,
    "height": 5,
    "heightType": "AGL",
    "indoorDeployment": false,
    "antennaGain": 15,
    "antennaBeamwidth": 60,
    "antennaAzimuth": 90,
    "groupingParam": "group1",
    "cbsdAddress": "ADDR1"
  }'
```

### 3. Solicitar Grant
```bash
curl -X POST "http://localhost:9000/v1.3/grant" \
  -H "Content-Type: application/json" \
  -H "X-SAS-Address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266" \
  -d '{
    "fccId": "FCC-TEST-001",
    "cbsdSerialNumber": "CBSD-TEST-001",
    "channelType": "GAA",
    "maxEirp": 30,
    "lowFrequency": 3550000000,
    "highFrequency": 3560000000,
    "requestedMaxEirp": 30,
    "requestedLowFrequency": 3550000000,
    "requestedHighFrequency": 3560000000,
    "grantExpireTime": 9999999999
  }'
```

## 🔍 Troubleshooting

### Problemas com PostgreSQL

**Erro: "connection refused"**
```bash
# Verificar se o serviço está rodando
sudo systemctl status postgresql

# Iniciar o serviço
sudo systemctl start postgresql

# Verificar logs
sudo journalctl -u postgresql
```

**Erro: "authentication failed"**
```bash
# Verificar configuração de autenticação
sudo cat /etc/postgresql/*/main/pg_hba.conf

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### Problemas com Redis

**Erro: "connection refused"**
```bash
# Verificar se o serviço está rodando
sudo systemctl status redis

# Iniciar o serviço
sudo systemctl start redis

# Verificar logs
sudo journalctl -u redis
```

### Problemas com Python

**Erro: "ModuleNotFoundError"**
```bash
# Verificar se o virtual environment está ativo
which python

# Reinstalar dependências
pip install -r requirements.txt
```

## 📊 Monitoramento

### Verificar Status dos Serviços
```bash
# PostgreSQL
sudo systemctl status postgresql

# Redis
sudo systemctl status redis

# API (se estiver rodando)
curl http://localhost:9000/health
```

### Verificar Logs
```bash
# PostgreSQL logs
sudo journalctl -u postgresql -f

# Redis logs
sudo journalctl -u redis -f

# API logs (se estiver rodando)
tail -f logs/sas_service.log
```

## 🗄️ Backup e Restore

### Backup do PostgreSQL
```bash
# Backup completo
pg_dump -h localhost -U opensas_user -d opensas > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup apenas dados
pg_dump -h localhost -U opensas_user -d opensas --data-only > data_backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore do PostgreSQL
```bash
# Restore completo
psql -h localhost -U opensas_user -d opensas < backup_file.sql

# Restore apenas dados
psql -h localhost -U opensas_user -d opensas < data_backup_file.sql
```

## 🧹 Limpeza

### Remover Dados
```bash
# Resetar banco de dados
python manage.py reset

# Ou conectar e limpar manualmente
psql -h localhost -U opensas_user -d opensas -c "TRUNCATE TABLE events, grants, cbsds, sas_authorizations CASCADE;"
```

### Desinstalar Serviços (se necessário)
```bash
# Parar serviços
sudo systemctl stop postgresql redis

# Desabilitar serviços
sudo systemctl disable postgresql redis

# Desinstalar (Ubuntu/Debian)
sudo apt-get remove --purge postgresql* redis-server

# Desinstalar (CentOS/RHEL)
sudo yum remove postgresql* redis
```

## 📝 Notas Importantes

1. **Segurança**: As senhas padrão são para desenvolvimento. Em produção, use senhas fortes.
2. **Portas**: Certifique-se de que as portas 5432 (PostgreSQL) e 6379 (Redis) estão disponíveis.
3. **Firewall**: Configure o firewall se necessário.
4. **Backup**: Faça backups regulares dos dados importantes.
5. **Logs**: Monitore os logs para detectar problemas.

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs dos serviços
2. Teste as conexões individualmente
3. Verifique se todas as dependências estão instaladas
4. Consulte a documentação do PostgreSQL e Redis
