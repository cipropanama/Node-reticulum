#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Interactive Configuration Wizard
Auspiciado por Cipropanama.org
Permite configurar y reconfigurar paso a paso el nodo Reticulum, RNodes,
módems, transporte, mensajería de emergencia LXMF y páginas NomadNet.
"""

import os
import sys
import json
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect

CONFIG_DIR = "/etc/reticulum-node"
NODE_JSON = os.path.join(CONFIG_DIR, "node.json")

# ANSI Color formatting
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_RED = "\033[31m"
C_MAGENTA = "\033[35m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"{C_CYAN}{C_BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║            🌐 ASISTENTE DE CONFIGURACIÓN - NODO RETICULUM                  ║")
    print("║                   Red de Emergencia y Resiliencia                          ║")
    print("║                      Auspiciado por Cipropanama.org                        ║")
    print("║                        https://cipropanama.org                             ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{C_RESET}")

def prompt(text, default=""):
    if default:
        p_text = f"{C_BOLD}{text}{C_RESET} [{C_GREEN}{default}{C_RESET}]: "
    else:
        p_text = f"{C_BOLD}{text}{C_RESET}: "
    try:
        val = input(p_text).strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C_YELLOW}Operación cancelada por el usuario.{C_RESET}")
        sys.exit(0)

def prompt_bool(text, default=True):
    def_str = "S/n" if default else "s/N"
    p_text = f"{C_BOLD}{text}{C_RESET} ({def_str}): "
    try:
        val = input(p_text).strip().lower()
        if not val:
            return default
        return val in ["s", "si", "y", "yes", "true", "1"]
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C_YELLOW}Operación cancelada por el usuario.{C_RESET}")
        sys.exit(0)

def prompt_choice(text, options, default_idx=0):
    print(f"\n{C_BOLD}{text}:{C_RESET}")
    for i, opt in enumerate(options):
        marker = f"{C_GREEN}*{C_RESET}" if i == default_idx else " "
        print(f"  {marker} [{i+1}] {opt['title']} - {C_CYAN}{opt.get('desc','')}{C_RESET}")
    while True:
        try:
            choice = input(f"Seleccione una opción [1-{len(options)}] [{default_idx+1}]: ").strip()
            if not choice:
                return default_idx
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
            print(f"{C_RED}Opción inválida. Intente de nuevo.{C_RESET}")
        except ValueError:
            print(f"{C_RED}Por favor ingrese un número válido.{C_RESET}")

def load_saved_config():
    if os.path.exists(NODE_JSON):
        try:
            with open(NODE_JSON, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_node_json(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(NODE_JSON, "w") as f:
        json.dump(cfg, f, indent=2)

def generate_rns_config(cfg, rns_conf_path):
    """Generates a clean, robust Reticulum config file based on user wizard choices."""
    os.makedirs(os.path.dirname(rns_conf_path), exist_ok=True)
    
    enable_transport = "yes" if cfg.get("enable_transport", True) else "no"
    share_instance = "yes" if cfg.get("share_instance", True) else "no"
    
    lines = [
        "# Reticulum Network Stack Configuration",
        "# Generado automáticamente por Reticulum Emergency Node Wizard",
        "# Auspiciado por Cipropanama.org - https://cipropanama.org",
        "",
        "[reticulum]",
        f"enable_transport = {enable_transport}",
        f"share_instance = {share_instance}",
        "shared_instance_port = 37428",
        "instance_control_port = 37429",
        "panic_on_interface_error = no",
        "",
        "[logging]",
        "loglevel = 4",
        "",
        "[interfaces]"
    ]

    # 1. Local Shared Interface
    lines.extend([
        "  [[Auto Local Interface]]",
        "    type = AutoInterface",
        "    enabled = yes",
        "    mode = full",
        ""
    ])

    # 2. RNode LoRa Interface
    if cfg.get("enable_rnode", False):
        port = cfg.get("rnode_port", "/dev/ttyUSB0")
        freq = int(float(cfg.get("lora_freq", "915.0")) * 1000000)
        bw = int(float(cfg.get("lora_bw", "125")) * 1000)
        txpower = int(cfg.get("lora_txpower", "17"))
        sf = int(cfg.get("lora_sf", "8"))
        cr = int(cfg.get("lora_cr", "5"))
        
        lines.extend([
            f"  [[RNode LoRa - {port}]]",
            "    type = RNodeInterface",
            "    enabled = yes",
            f"    port = {port}",
            f"    frequency = {freq}",
            f"    bandwidth = {bw}",
            f"    txpower = {txpower}",
            f"    spreadingfactor = {sf}",
            f"    codingrate = {cr}",
            "    flow_control = false",
            ""
        ])

    # 3. Serial KISS / TNC Modem Interface
    if cfg.get("enable_kiss", False):
        k_port = cfg.get("kiss_port", "/dev/ttyUSB1")
        k_speed = int(cfg.get("kiss_speed", "115200"))
        lines.extend([
            f"  [[Serial KISS Modem - {k_port}]]",
            "    type = KISSInterface",
            "    enabled = yes",
            f"    port = {k_port}",
            f"    speed = {k_speed}",
            "    databits = 8",
            "    parity = none",
            "    stopbits = 1",
            "    preamble = 150",
            "    txtail = 20",
            "    persistence = 64",
            "    slottime = 20",
            ""
        ])

    # 4. TCP Server (Backbone Local / WiFi / LAN)
    if cfg.get("enable_tcp_server", False):
        tcp_port = int(cfg.get("tcp_server_port", "4242"))
        lines.extend([
            "  [[TCP Server Interface]]",
            "    type = TCPServerInterface",
            "    enabled = yes",
            "    listen_ip = 0.0.0.0",
            f"    listen_port = {tcp_port}",
            ""
        ])

    # 5. TCP Client (Connect to Upstream Hub)
    if cfg.get("enable_tcp_client", False):
        target_host = cfg.get("tcp_target_host", "hub.reticulum.network")
        target_port = int(cfg.get("tcp_target_port", "4242"))
        lines.extend([
            f"  [[TCP Hub - {target_host}]]",
            "    type = TCPClientInterface",
            "    enabled = yes",
            f"    target_host = {target_host}",
            f"    target_port = {target_port}",
            ""
        ])

    with open(rns_conf_path, "w") as f:
        f.write("\n".join(lines) + "\n")

def generate_nomadnet_config(cfg, nomad_conf_path):
    """Generates NomadNet configuration with page directories and propagation node."""
    os.makedirs(os.path.dirname(nomad_conf_path), exist_ok=True)
    pages_dir = cfg.get("nomadnet_pages_dir", "/var/nomadnet/pages")
    node_name = cfg.get("node_name", "Reticulum-Emergency-Node")
    
    lines = [
        "# NomadNet Configuration File",
        "# Generado por Reticulum Emergency Node Wizard",
        "# Auspiciado por Cipropanama.org",
        "",
        "[nomadnet]",
        f"display_name = {node_name}",
        "enable_node = yes",
        "enable_microweb = yes",
        f"pages_path = {pages_dir}",
        "enable_propagation_node = yes" if cfg.get("enable_lxmf", True) else "enable_propagation_node = no",
        "",
        "[logging]",
        "loglevel = 4",
        ""
    ]
    with open(nomad_conf_path, "w") as f:
        f.write("\n".join(lines) + "\n")

def run_wizard():
    clear_screen()
    banner()
    
    saved = load_saved_config()
    stats = hardware_detect.get_system_stats()
    available_ports = hardware_detect.get_serial_ports()
    
    print(f"{C_GREEN}✓ Hardware detectado:{C_RESET} {stats['model']} ({stats['arch']})")
    if stats['cpu_temp']:
        print(f"{C_GREEN}✓ Temperatura CPU:{C_RESET}    {stats['cpu_temp']}°C")
    print(f"{C_GREEN}✓ Puertos Serie/USB:{C_RESET}  {len(available_ports)} detectados\n")
    
    cfg = {}
    
    # --- PASO 1: IDENTIDAD Y PROPÓSITO DEL NODO ---
    print(f"{C_MAGENTA}{C_BOLD}▶ PASO 1: Identidad del Nodo de Emergencia{C_RESET}")
    cfg["node_name"] = prompt("Nombre identificador del Nodo", saved.get("node_name", "CiproPanama-Emergencia-01"))
    cfg["location"] = prompt("Ubicación geográfica / Región", saved.get("location", "Panamá / Móvil"))
    cfg["description"] = prompt("Descripción / Misión del nodo", saved.get("description", "Punto de Enlace y Mensajería de Emergencia"))
    
    # --- PASO 2: MODO DE RED Y TRANSPORTE ---
    print(f"\n{C_MAGENTA}{C_BOLD}▶ PASO 2: Modo de Red y Enrutamiento (Transporte){C_RESET}")
    print("El modo transporte permite que este nodo funcione como repetidor activo en la malla,")
    print("retransmitiendo paquetes entre otros nodos aunque no sean su destino final.")
    cfg["enable_transport"] = prompt_bool("¿Habilitar modo TRANSPORTE (Repetidor/Router de malla)?", saved.get("enable_transport", True))
    cfg["share_instance"] = True

    # --- PASO 3: STORE-AND-FORWARD (MENSAJERÍA LXMF EN DIFERIDO) ---
    print(f"\n{C_MAGENTA}{C_BOLD}▶ PASO 3: Almacenamiento y Reenvío (Store-and-Forward LXMF){C_RESET}")
    print("Permite que el nodo guarde mensajes dirigidos a personas desconectadas y los entregue")
    print("automáticamente tan pronto como el destinatario vuelva a tener cobertura.")
    cfg["enable_lxmf"] = prompt_bool("¿Habilitar Nodo de Propagación de Mensajes LXMF?", saved.get("enable_lxmf", True))

    # --- PASO 4: INTERFACES DE COMUNICACIÓN ---
    print(f"\n{C_MAGENTA}{C_BOLD}▶ PASO 4: Configuración de Interfaces de Comunicación{C_RESET}")
    
    # RNode LoRa
    print(f"\n{C_CYAN}--- Interface LoRa (RNode) ---{C_RESET}")
    cfg["enable_rnode"] = prompt_bool("¿Desea configurar una interfaz LoRa (RNode por USB o UART)?", saved.get("enable_rnode", True))
    
    serial_ports_configured = []
    if cfg["enable_rnode"]:
        if available_ports:
            print("Puertos disponibles:")
            port_opts = [{"title": p["port"], "desc": f"[{p['type']}] {p['description']}"} for p in available_ports]
            port_opts.append({"title": "Ingresar puerto manualmente", "desc": "Ej. /dev/ttyUSB0 o /dev/serial0"})
            
            p_idx = prompt_choice("Seleccione el puerto del RNode LoRa", port_opts, 0)
            if p_idx < len(available_ports):
                cfg["rnode_port"] = available_ports[p_idx]["port"]
            else:
                cfg["rnode_port"] = prompt("Puerto del RNode", "/dev/ttyUSB0")
        else:
            cfg["rnode_port"] = prompt("Puerto del RNode (ej. /dev/ttyUSB0 o /dev/serial0)", saved.get("rnode_port", "/dev/ttyUSB0"))
        
        serial_ports_configured.append(cfg["rnode_port"])
        
        # Frecuencia LoRa
        freq_opts = [
            {"title": "915.0 MHz (América / Panamá ISM)", "desc": "Banda estándar recomendada para Panamá y América"},
            {"title": "868.0 MHz (Europa / África)", "desc": "Banda ISM Europea"},
            {"title": "433.0 MHz (Radioaficionados / ISM)", "desc": "Banda UHF"},
            {"title": "Personalizada", "desc": "Ingresar frecuencia específica"}
        ]
        f_idx = prompt_choice("Banda de frecuencia LoRa", freq_opts, 0)
        if f_idx == 0:
            cfg["lora_freq"] = "915.0"
        elif f_idx == 1:
            cfg["lora_freq"] = "868.0"
        elif f_idx == 2:
            cfg["lora_freq"] = "433.0"
        else:
            cfg["lora_freq"] = prompt("Frecuencia en MHz (ej: 915.0)", "915.0")
            
        cfg["lora_bw"] = prompt("Ancho de banda LoRa en kHz [125, 250, 500]", str(saved.get("lora_bw", "125")))
        cfg["lora_sf"] = prompt("Spreading Factor (Factor de dispersión) [7 a 12]", str(saved.get("lora_sf", "8")))
        cfg["lora_cr"] = prompt("Coding Rate [5 a 8]", str(saved.get("lora_cr", "5")))
        cfg["lora_txpower"] = prompt("Potencia de Transmisión TX en dBm [0 a 22]", str(saved.get("lora_txpower", "17")))

    # Serial KISS / TNC Modem
    print(f"\n{C_CYAN}--- Interface Módem Packet / KISS TNC ---{C_RESET}")
    cfg["enable_kiss"] = prompt_bool("¿Desea configurar un módem Packet Radio / TNC KISS por puerto serie?", saved.get("enable_kiss", False))
    if cfg["enable_kiss"]:
        cfg["kiss_port"] = prompt("Puerto del módem serie", saved.get("kiss_port", "/dev/ttyUSB1"))
        cfg["kiss_speed"] = prompt("Velocidad de baudios (Baudrate)", str(saved.get("kiss_speed", "115200")))
        serial_ports_configured.append(cfg["kiss_port"])

    # TCP Server (LAN / WiFi)
    print(f"\n{C_CYAN}--- Enlaces TCP / Red Local / WiFi ---{C_RESET}")
    cfg["enable_tcp_server"] = prompt_bool("¿Habilitar Servidor TCP local (para que otros clientes en la WiFi/LAN se conecten al nodo)?", saved.get("enable_tcp_server", True))
    if cfg["enable_tcp_server"]:
        cfg["tcp_server_port"] = prompt("Puerto de escucha TCP", str(saved.get("tcp_server_port", "4242")))

    # TCP Client (Upstream Hub)
    cfg["enable_tcp_client"] = prompt_bool("¿Desea conectar este nodo a un Hub Reticulum remoto (a través de Internet si está disponible)?", saved.get("enable_tcp_client", False))
    if cfg["enable_tcp_client"]:
        cfg["tcp_target_host"] = prompt("Dirección IP o Dominio del Hub", saved.get("tcp_target_host", "hub.reticulum.network"))
        cfg["tcp_target_port"] = prompt("Puerto del Hub", str(saved.get("tcp_target_port", "4242")))

    cfg["serial_ports"] = serial_ports_configured
    cfg["nomadnet_pages_dir"] = "/var/nomadnet/pages"

    # --- PASO 5: NOMADNET Y PÁGINA MICROWEB ---
    print(f"\n{C_MAGENTA}{C_BOLD}▶ PASO 5: Página NomadNet y Telemetría Cipropanama.org{C_RESET}")
    print(f"El nodo publicará la página Microweb oficial con el nombre '{cfg['node_name']}'")
    print("e incluirá telemetría en tiempo real (CPU, RAM, Uptime) y referencias a Cipropanama.org.")

    # Guardar Configuración
    print(f"\n{C_YELLOW}Guardando configuración y generando archivos del sistema...{C_RESET}")
    save_node_json(cfg)
    
    # RNS config target paths (root and user)
    user_home = os.path.expanduser("~")
    root_rns_path = "/root/.reticulum/config"
    user_rns_path = os.path.join(user_home, ".reticulum/config")
    
    generate_rns_config(cfg, root_rns_path)
    if user_home != "/root":
        generate_rns_config(cfg, user_rns_path)

    # NomadNet config target paths
    root_nomad_path = "/root/.nomadnetwork/config"
    user_nomad_path = os.path.join(user_home, ".nomadnetwork/config")
    generate_nomadnet_config(cfg, root_nomad_path)
    if user_home != "/root":
        generate_nomadnet_config(cfg, user_nomad_path)

    # Update NomadNet pages
    try:
        update_script = os.path.join(SCRIPT_DIR, "update_telemetry.py")
        subprocess.run([sys.executable, update_script], check=False)
    except Exception as e:
        print(f"{C_RED}Aviso al generar páginas: {e}{C_RESET}")

    print(f"{C_GREEN}{C_BOLD}✓ ¡Configuración guardada exitosamente!{C_RESET}")
    print(f"Archivos actualizados en: {CONFIG_DIR}, ~/.reticulum/ y ~/.nomadnetwork/")
    
    # Restart services if running under systemd
    if os.path.exists("/bin/systemctl"):
        restart = prompt_bool("\n¿Desea reiniciar los servicios de Reticulum y NomadNet ahora para aplicar los cambios?", True)
        if restart:
            print(f"{C_CYAN}Reiniciando servicios systemd...{C_RESET}")
            subprocess.run(["systemctl", "restart", "rnsd"], check=False)
            subprocess.run(["systemctl", "restart", "nomadnet"], check=False)
            print(f"{C_GREEN}✓ Servicios reiniciados.{C_RESET}")

    print(f"\n{C_BOLD}Para volver a este asistente en cualquier momento, ejecute:{C_RESET}")
    print(f"  {C_CYAN}sudo rns-admin{C_RESET}\n")

if __name__ == "__main__":
    run_wizard()
