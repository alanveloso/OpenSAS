# 🚀 Configuração PostgreSQL para OpenSAS

## 🎯 Configuração Rápida

Para configurar o PostgreSQL localmente e executar a API OpenSAS:

### 1. Configuração Automática (Recomendada)
```bash
# Execute o script completo
bash scripts/setup_environment.sh
```

### 2. Ou configure manualmente:
```bash
# Instalar PostgreSQL
bash scripts/setup_postgres_local.sh

# Instalar Redis
bash scripts/setup_redis_local.sh

# Criar arquivo .env
cp env.example .env

# Ativar virtual environment
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Testar conexão
python scripts/test_postgres_connection.py

# Inicializar banco
python manage.py init
```

## 🚀 Executar a API

```bash
# Ativar virtual environment
source venv/bin/activate

# Executar API
python run.py
```

A API estará disponível em:
- **API**: http://localhost:9000
- **Documentação**: http://localhost:9000/docs
- **Health Check**: http://localhost:9000/health

## 🧪 Testar Configuração

```bash
# Teste rápido
bash scripts/quick_test.sh

# Teste detalhado
python scripts/test_postgres_connection.py
```

## 📋 Informações de Conexão

**PostgreSQL:**
- Host: `localhost`
- Porta: `5432`
- Banco: `opensas`
- Usuário: `opensas_user`
- Senha: `opensas_password`
- URL: `postgresql://opensas_user:opensas_password@localhost:5432/opensas`

**Redis:**
- Host: `localhost`
- Porta: `6379`
- URL: `redis://localhost:6379`

## 🔧 Comandos Úteis

```bash
# Status dos serviços
sudo systemctl status postgresql redis

# Conectar ao PostgreSQL
psql -h localhost -U opensas_user -d opensas

# Testar Redis
redis-cli ping

# Logs dos serviços
sudo journalctl -u postgresql -f
sudo journalctl -u redis -f
```

## 🆘 Troubleshooting

**Se PostgreSQL não conectar:**
```bash
sudo systemctl start postgresql
sudo systemctl restart postgresql
```

**Se Redis não conectar:**
```bash
sudo systemctl start redis
sudo systemctl restart redis
```

**Se virtual environment não existir:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📖 Documentação Completa

Para mais detalhes, consulte: `SETUP_LOCAL.md`
