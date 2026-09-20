#!/usr/bin/env bash
# ==============================================================================
# RETICULUM EMERGENCY NODE - AUTO-INSTALLER UNIVERSAL
# Auspiciado por Cipropanama.org - https://cipropanama.org
# Compatible con: Raspberry Pi Zero W / 2W, Orange Pi Zero, MangoPi MQ-Pro
# ==============================================================================

set -e

# Colores de salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

INSTALL_DIR="/opt/reticulum-node"
PAGES_DIR="/var/nomadnet/pages"
CONFIG_DIR="/etc/reticulum-node"
REPO_URL="https://github.com/cipropanama/Node-reticulum.git"

banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║       🌐 INSTALADOR AUTOMÁTICO DE NODO DE EMERGENCIA RETICULUM             ║"
    echo "║                   Red de Resiliencia Comunitaria                           ║"
    echo "║                      Auspiciado por Cipropanama.org                        ║"
    echo "║                        https://cipropanama.org                             ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}[ERROR] Este instalador debe ejecutarse como root (con sudo).${NC}"
        echo -e "Ejemplo: ${BOLD}sudo bash install.sh${NC}"
        exit 1
    fi
}

detect_system() {
    echo -e "${CYAN}▶ Detectando arquitectura y sistema operativo...${NC}"
    ARCH=$(uname -m)
    OS="Desconocido"
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$PRETTY_NAME
    fi

    echo -e "  • Sistema Operativo: ${GREEN}$OS${NC}"
    echo -e "  • Arquitectura CPU:  ${GREEN}$ARCH${NC}"

    case "$ARCH" in
        armv6l)
            echo -e "  • Plataforma: ${YELLOW}Raspberry Pi Zero W / ARMv6${NC}"
            ;;
        armv7l)
            echo -e "  • Plataforma: ${YELLOW}Orange Pi Zero / ARMv7 32-bit${NC}"
            ;;
        aarch64)
            echo -e "  • Plataforma: ${YELLOW}Raspberry Pi Zero 2W / Orange Pi Zero 3 / ARM 64-bit${NC}"
            ;;
        riscv64)
            echo -e "  • Plataforma: ${YELLOW}MangoPi MQ-Pro / Allwinner D1 RISC-V 64-bit${NC}"
            ;;
        *)
            echo -e "  • Plataforma: ${YELLOW}Dispositivo SBC Genérico ($ARCH)${NC}"
            ;;
    esac
}

install_system_dependencies() {
    echo -e "\n${CYAN}▶ Actualizando repositorios e instalando paquetes del sistema...${NC}"
    export DEBIAN_FRONTEND=noninteractive
    
    apt-get update -y || true
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        python3-setuptools \
        python3-wheel \
        python3-serial \
        python3-cryptography \
        git \
        curl \
        jq \
        build-essential \
        libffi-dev \
        zlib1g-dev \
        tar \
        gzip

    # Agregar usuario al grupo dialout para acceso a puertos serie sin root
    if [ -n "$SUDO_USER" ]; then
        usermod -aG dialout "$SUDO_USER" || true
    fi
}

install_reticulum_stack() {
    echo -e "\n${CYAN}▶ Instalando Reticulum Network Stack, LXMF y NomadNet vía pip...${NC}"
    
    # Manejar flag --break-system-packages para Debian 12 / Bookworm / Ubuntu 24.04
    PIP_FLAGS=""
    if python3 -m pip install --help 2>&1 | grep -q -- "--break-system-packages"; then
        PIP_FLAGS="--break-system-packages"
    fi

    python3 -m pip install --upgrade pip $PIP_FLAGS || true
    python3 -m pip install --upgrade $PIP_FLAGS \
        rns \
        lxmf \
        nomadnet \
        pyserial \
        cryptography

    echo -e "${GREEN}✓ Paquetes de Reticulum instalados correctamente.${NC}"
}

setup_workspace_and_files() {
    echo -e "\n${CYAN}▶ Configurando directorios del sistema y scripts de administración...${NC}"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$PAGES_DIR"
    mkdir -p "$CONFIG_DIR"
    mkdir -p "/var/backups/reticulum-node"
    mkdir -p "/root/.reticulum"
    mkdir -p "/root/.nomadnetwork"

    # Si estamos instalando desde un repositorio clonado local
    CURRENT_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$CURRENT_SCRIPT_DIR/scripts/rns_wizard.py" ]; then
        cp -r "$CURRENT_SCRIPT_DIR"/* "$INSTALL_DIR/" || true
    else
        # Si fue ejecutado vía curl | bash, clonar el repositorio
        if [ ! -d "$INSTALL_DIR/.git" ]; then
            git clone "$REPO_URL" "$INSTALL_DIR" || {
                echo -e "${YELLOW}Advertencia: No se pudo clonar git directo, usando copia local.${NC}"
            }
        fi
    fi

    # Dar permisos de ejecución
    chmod +x "$INSTALL_DIR"/bin/* 2>/dev/null || true
    chmod +x "$INSTALL_DIR"/scripts/* 2>/dev/null || true
    chmod +x "$INSTALL_DIR"/watchdog/* 2>/dev/null || true

    # Crear enlaces simbólicos globales en /usr/local/bin
    ln -sf "$INSTALL_DIR/bin/rns-admin" /usr/local/bin/rns-admin
    ln -sf "$INSTALL_DIR/scripts/update_telemetry.py" /usr/local/bin/reticulum-telemetry
    ln -sf "$INSTALL_DIR/scripts/hardware_detect.py" /usr/local/bin/rns-hwdetect

    # Copiar páginas iniciales de NomadNet
    if [ -d "$INSTALL_DIR/pages" ]; then
        cp -r "$INSTALL_DIR/pages/"*.mu "$PAGES_DIR/" 2>/dev/null || true
    fi

    # Configuración de log rotate para proteger memoria SD en SBC
    cat << 'EOF' > /etc/logrotate.d/reticulum-node
/var/log/reticulum-watchdog.log {
    rotate 4
    weekly
    compress
    missingok
    notifempty
    maxsize 5M
}
EOF
}

setup_systemd_services() {
    echo -e "\n${CYAN}▶ Instalando servicios de inicio automático (systemd)...${NC}"
    
    if [ -d "$INSTALL_DIR/systemd" ]; then
        cp "$INSTALL_DIR/systemd/"*.service /etc/systemd/system/ 2>/dev/null || true
        cp "$INSTALL_DIR/systemd/"*.timer /etc/systemd/system/ 2>/dev/null || true
    fi

    systemctl daemon-reload
    systemctl enable rnsd.service || true
    systemctl enable nomadnet.service || true
    systemctl enable rns-watchdog.timer || true
    systemctl enable rns-telemetry.timer || true

    systemctl start rns-watchdog.timer || true
    systemctl start rns-telemetry.timer || true

    echo -e "${GREEN}✓ Servicios systemd configurados y activados.${NC}"
}

main() {
    banner
    check_root
    detect_system
    install_system_dependencies
    install_reticulum_stack
    setup_workspace_and_files
    setup_systemd_services

    echo -e "\n${GREEN}${BOLD}════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD} ¡INSTALACIÓN BASE COMPLETADA CON ÉXITO!${NC}"
    echo -e "${GREEN}${BOLD} Auspiciado por Cipropanama.org - https://cipropanama.org${NC}"
    echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════════════════════════════${NC}"
    
    if [ "$1" == "--non-interactive" ] || [ "$1" == "--update" ]; then
        echo -e "${YELLOW}Modo no interactivo. Puede configurar el nodo en cualquier momento con:${NC}"
        echo -e "  ${BOLD}sudo rns-admin${NC}"
        exit 0
    fi

    echo -e "\n${CYAN}Iniciando el asistente de configuración paso a paso...${NC}\n"
    sleep 2
    python3 "$INSTALL_DIR/scripts/rns_wizard.py"
}

main "$@"
