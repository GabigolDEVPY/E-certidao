#!/usr/bin/env bash
# deploy/setup.sh — roda uma vez na EC2 Ubuntu para configurar tudo
set -euo pipefail

APP_DIR="/home/ubuntu/E-certidao"
VENV="$APP_DIR/venv"

echo "==> Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

echo "==> Instalando dependências do sistema..."
sudo apt install -y python3 python3-venv python3-pip nginx git

echo "==> Criando venv..."
python3 -m venv "$VENV"

echo "==> Instalando dependências Python..."
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "==> Criando pasta de logs..."
mkdir -p "$APP_DIR/logs"

echo "==> Copiando .env.example para .env (edite depois!)..."
if [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    echo "    ATENÇÃO: edite $APP_DIR/.env com suas chaves reais!"
fi

echo "==> Rodando migrations..."
"$VENV/bin/python" "$APP_DIR/manage.py" migrate --noinput

echo "==> Coletando estáticos..."
"$VENV/bin/python" "$APP_DIR/manage.py" collectstatic --noinput

echo "==> Configurando Nginx..."
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/ecertidao
sudo ln -sf /etc/nginx/sites-available/ecertidao /etc/nginx/sites-enabled/ecertidao
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

echo "==> Configurando Gunicorn como serviço..."
sudo cp "$APP_DIR/deploy/gunicorn.service" /etc/systemd/system/ecertidao.service
sudo systemctl daemon-reload
sudo systemctl enable ecertidao
sudo systemctl start ecertidao

echo ""
echo "✅ Deploy concluído!"
echo "   - Edite /home/ubuntu/E-certidao/.env com suas chaves"
echo "   - Reinicie com: sudo systemctl restart ecertidao"
echo "   - Para SSL: sudo apt install certbot python3-certbot-nginx && sudo certbot --nginx"
