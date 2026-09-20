#!/usr/bin/env bash
# ==============================================================================
# RETICULUM EMERGENCY NODE - SCRIPT DE DESINSTALACIÓN
# Auspiciado por Cipropanama.org
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[ERROR] Debe ejecutar este script con privilegios root (sudo).${NC}"
    exit 1
fi

echo -e "${YELLOW}${BOLD}¿Está seguro de que desea desinstalar el Reticulum Emergency Node?${NC}"
read -p "Escriba 'SI' para confirmar: " confirm
if [ "$confirm" != "SI" ] && [ "$confirm" != "si" ]; then
    echo "Desinstalación cancelada."
    exit 0
fi

echo -e "\n${YELLOW}1. Deteniendo y deshabilitando servicios systemd...${NC}"
systemctl stop rnsd nomadnet rns-watchdog.timer rns-telemetry.timer 2>/dev/null || true
systemctl disable rnsd nomadnet rns-watchdog.timer rns-telemetry.timer 2>/dev/null || true

rm -f /etc/systemd/system/rnsd.service \
      /etc/systemd/system/nomadnet.service \
      /etc/systemd/system/rns-watchdog.* \
      /etc/systemd/system/rns-telemetry.*
systemctl daemon-reload

echo -e "${YELLOW}2. Eliminando ejecutables globales y enlaces...${NC}"
rm -f /usr/local/bin/rns-admin \
      /usr/local/bin/reticulum-telemetry \
      /usr/local/bin/rns-hwdetect

echo -e "${YELLOW}3. ¿Desea eliminar las configuraciones e identidades criptográficas (/root/.reticulum)?${NC}"
read -p "(s/N): " del_ident
if [ "$del_ident" == "s" ] || [ "$del_ident" == "S" ]; then
    rm -rf /root/.reticulum /root/.nomadnetwork /etc/reticulum-node /var/nomadnet
    echo -e "${GREEN}✓ Claves y configuraciones eliminadas.${NC}"
else
    echo -e "Las identidades y configuraciones se mantuvieron intactas en /root/.reticulum"
fi

rm -rf /opt/reticulum-node
echo -e "\n${GREEN}${BOLD}✓ Desinstalación completada con éxito.${NC}\n"
