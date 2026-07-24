# E-Certidao - Deploy AWS (EC2 + Nginx + Gunicorn + SQLite)

## Pre-requisitos

- EC2 Ubuntu 22.04+
- Portas 80 e 443 liberadas no Security Group
- Git configurado para puxar o repositorio

## Deploy rapido

Use a pasta `/home/ubuntu/E-certidao`, porque os arquivos de Gunicorn e Nginx apontam para esse caminho.

```bash
cd /home/ubuntu
git clone <URL_DO_SEU_REPO> E-certidao
cd E-certidao

chmod +x deploy/setup.sh deploy/update.sh
sudo bash deploy/setup.sh

nano .env
sudo systemctl restart ecertidao
```

## Atualizar o site na EC2

Sempre que puxar alteracoes do GitHub, rode o script abaixo. Ele aplica migrations, coleta arquivos estaticos, recarrega o Nginx e reinicia o Gunicorn.

```bash
cd /home/ubuntu/E-certidao
bash deploy/update.sh
```

Se o projeto estiver em outra pasta, informe o caminho:

```bash
APP_DIR=/caminho/do/projeto bash deploy/update.sh
```

## Comandos uteis

```bash
# Ver logs do Gunicorn
tail -f /home/ubuntu/E-certidao/logs/error.log

# Reiniciar app
sudo systemctl restart ecertidao

# Status do app
sudo systemctl status ecertidao

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Rodar migrations manualmente
source /home/ubuntu/E-certidao/venv/bin/activate
python manage.py migrate --noinput

# Coletar estaticos manualmente
python manage.py collectstatic --noinput
```

## SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d certidaobr.com -d www.certidaobr.com
```

## Estrutura de deploy

```text
deploy/
  nginx.conf
  gunicorn.service
  setup.sh
  update.sh
.env.example
```
