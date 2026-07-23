# E-Certidão — Deploy AWS (EC2 + Nginx + Gunicorn + SQLite)

## Pré-requisitos

- EC2 Ubuntu 22.04+ (t3.micro serve)
- Porta 80 e 443 liberadas no Security Group
- Git configurado para puxar o repositório

## Deploy rápido

```bash
# 1. Clone o repositório
cd /home/ubuntu
git clone <URL_DO_SEU_REPO> site
cd site

# 2. Rode o script de setup
chmod +x deploy/setup.sh
sudo bash deploy/setup.sh

# 3. Edite o .env com suas chaves reais
nano .env

# 4. Reinicie o serviço
sudo systemctl restart ecertidao
```

## Comandos úteis

```bash
# Ver logs do gunicorn
tail -f /home/ubuntu/site/logs/error.log

# Reiniciar app
sudo systemctl restart ecertidao

# Status do app
sudo systemctl status ecertidao

# Ver logs do nginx
sudo tail -f /var/log/nginx/error.log

# Rodar migrations após atualizar código
source /home/ubuntu/site/venv/bin/activate
python manage.py migrate

# Coletar estáticos após mudar CSS/JS
python manage.py collectstatic --noinput
```

## Atualizar o site

```bash
cd /home/ubuntu/site
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
sudo systemctl restart ecertidao
```

## SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seudominio.com.br -d www.seudominio.com.br
```

O Certbot configura o Nginx automaticamente. Renovação é automática via cron.

## Estrutura de deploy

```
deploy/
├── nginx.conf          # Config do Nginx (reverse proxy)
├── gunicorn.service    # Systemd service (auto-restart)
└── setup.sh            # Script de instalação completa
.env.example            # Template de variáveis de ambiente
```
