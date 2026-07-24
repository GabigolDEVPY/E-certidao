#!/usr/bin/env bash
# Atualiza o codigo em producao e aplica tudo que o Django precisa apos git pull.
set -euo pipefail

APP_DIR="${APP_DIR:-/home/ubuntu/E-certidao}"
VENV="${VENV:-$APP_DIR/venv}"
SERVICE_NAME="${SERVICE_NAME:-ecertidao}"

cd "$APP_DIR"

echo "==> Atualizando codigo do Git..."
git pull --ff-only

echo "==> Instalando/atualizando dependencias..."
"$VENV/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "==> Rodando migrations..."
"$VENV/bin/python" "$APP_DIR/manage.py" migrate --noinput

echo "==> Coletando arquivos estaticos..."
"$VENV/bin/python" "$APP_DIR/manage.py" collectstatic --noinput

echo "==> Atualizando Nginx e servico..."
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/ecertidao
sudo cp "$APP_DIR/deploy/gunicorn.service" /etc/systemd/system/ecertidao.service
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl daemon-reload
sudo systemctl restart "$SERVICE_NAME"

echo "==> Atualizacao concluida."
