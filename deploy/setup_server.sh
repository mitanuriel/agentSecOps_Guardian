#!/usr/bin/env bash
# =============================================================================
# deploy/setup_server.sh
# One-time bootstrap script — run this ONCE on your Hetzner server via SSH
# to prepare it for automated deployments.
#
# Usage:
#   ssh root@YOUR_SERVER_IP "bash -s" < deploy/setup_server.sh
# =============================================================================

set -euo pipefail

APP_DIR="/opt/agentsecops"
APP_USER="www-data"
REPO="https://github.com/mitanuriel/agentSecOps_Guardian.git"

echo "==> [1/6] Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq

echo "==> [2/6] Installing Python 3, pip, venv, git, curl..."
apt-get install -y -qq python3 python3-pip python3-venv git curl

echo "==> [3/6] Cloning repository into $APP_DIR..."
mkdir -p $APP_DIR
if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch main "$REPO" "$APP_DIR"
else
  echo "  Repo already exists, skipping clone."
fi
chown -R $APP_USER:$APP_USER $APP_DIR

echo "==> [4/6] Creating Python virtual environment..."
cd $APP_DIR
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt uvicorn fastapi python-multipart -q

echo "==> [5/6] Installing systemd service..."
cp $APP_DIR/deploy/agentsecops.service /etc/systemd/system/agentsecops.service
systemctl daemon-reload
systemctl enable agentsecops
systemctl restart agentsecops

echo "==> [6/6] Verifying service is healthy..."
sleep 3
if curl -sf http://localhost:8000/health > /dev/null; then
  echo ""
  echo "✅ Setup complete! Service is running at http://localhost:8000"
  echo "   Open port 8000 in Hetzner firewall, or set up nginx as a reverse proxy."
else
  echo "❌ Health check failed. Showing service logs:"
  journalctl -u agentsecops -n 40
  exit 1
fi
