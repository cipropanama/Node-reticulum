#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Dynamic NomadNet Telemetry Generator
Auspiciado por Cipropanama.org
"""

import os
import sys
import time
import subprocess
import datetime
import json
import re

# Add scripts directory to path to import hardware_detect
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect

CONFIG_FILE = "/etc/reticulum-node/node.json"
PAGES_TEMPLATE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "pages")

def get_node_config():
    """Loads node configuration or provides sensible defaults."""
    defaults = {
        "node_name": "Reticulum-Emergency-Node",
        "location": "No especificada / Móvil",
        "description": "Nodo de Emergencia Autónomo",
        "mode": "Transporte + Propagación LXMF",
        "lora_freq": "915.0",
        "lora_bw": "125",
        "lora_sf": "8",
        "enable_lxmf": True,
        "nomadnet_pages_dir": "/var/nomadnet/pages"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception:
            pass
    return defaults

def get_rns_status_summary():
    """Runs rnstatus or parses rns logs to get active interfaces and identity."""
    identity = "Generando..."
    active_interfaces = "Consultando..."
    
    # Check if rnstatus command is available
    try:
        res = subprocess.run(["rnstatus"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            lines = res.stdout.splitlines()
            interfaces = []
            for line in lines:
                if line.startswith("<") and ">" in line:
                    interfaces.append(line.split("<")[1].split(">")[0].strip())
            if interfaces:
                active_interfaces = ", ".join(interfaces[:4])
                if len(interfaces) > 4:
                    active_interfaces += f" (+{len(interfaces)-4} más)"
            else:
                active_interfaces = "En espera de tráfico"
    except Exception:
        active_interfaces = "RNS Daemon Activo"

    # Try to extract primary destination hash if nomadnet or rns is configured
    try:
        res = subprocess.run(["nomadnet", "--version"], capture_output=True, text=True, timeout=5)
    except Exception:
        pass

    # Read saved identity if available
    ident_file = "/etc/reticulum-node/identity.txt"
    if os.path.exists(ident_file):
        try:
            with open(ident_file, "r") as f:
                identity = f.read().strip()
        except Exception:
            pass
    elif os.path.exists(os.path.expanduser("~/.reticulum/identities/primary")):
        identity = "Criptográficamente Protegida (Local)"

    return identity, active_interfaces

def update_pages():
    """Renders templates with current dynamic telemetry and writes them to the NomadNet pages dir."""
    cfg = get_node_config()
    stats = hardware_detect.get_system_stats()
    identity, active_interfaces = get_rns_status_summary()
    
    try:
        import battery_monitor
        bat = battery_monitor.get_battery_status()
    except Exception:
        bat = {"status_str": "N/D"}
    
    out_dir = cfg.get("nomadnet_pages_dir", "/var/nomadnet/pages")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except PermissionError:
        user_pages = os.path.expanduser("~/.nomadnetwork/storage/pages")
        try:
            os.makedirs(user_pages, exist_ok=True)
            out_dir = user_pages
        except PermissionError:
            out_dir = "/tmp/nomadnet/pages"
            os.makedirs(out_dir, exist_ok=True)
    
    cpu_temp_str = f"{stats['cpu_temp']}°C" if stats['cpu_temp'] else "N/D"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    replacements = {
        "{NODE_NAME}": cfg["node_name"],
        "{NODE_LOCATION}": cfg["location"],
        "{NODE_DESCRIPTION}": cfg["description"],
        "{NODE_MODE}": cfg["mode"],
        "{NODE_IDENTITY}": identity,
        "{LXMF_STATUS}": "✅ ACTIVO (Store & Forward)" if cfg.get("enable_lxmf", True) else "❌ Deshabilitado",
        "{SBC_MODEL}": stats["model"],
        "{SBC_ARCH}": stats["arch"],
        "{CPU_TEMP}": cpu_temp_str,
        "{LOAD_AVG}": stats["load_avg"],
        "{RAM_USED}": f"{stats['ram_used_mb']} MB",
        "{RAM_TOTAL}": f"{stats['ram_total_mb']} MB",
        "{RAM_PERCENT}": f"{stats['ram_percent']}%",
        "{UPTIME}": stats["uptime"],
        "{BATTERY_STATUS}": bat["status_str"],
        "{ACTIVE_INTERFACES}": active_interfaces,
        "{LAST_TELEMETRY_UPDATE}": now_str,
        "{LORA_FREQ}": str(cfg.get("lora_freq", "915.0")),
        "{LORA_BW}": str(cfg.get("lora_bw", "125")),
        "{LORA_SF}": str(cfg.get("lora_sf", "8")),
    }

    # Render each template file from PAGES_TEMPLATE_DIR
    if os.path.exists(PAGES_TEMPLATE_DIR):
        for fname in os.listdir(PAGES_TEMPLATE_DIR):
            if fname.endswith(".mu") or fname.endswith(".txt"):
                src_path = os.path.join(PAGES_TEMPLATE_DIR, fname)
                dst_path = os.path.join(out_dir, fname)
                try:
                    with open(src_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    for k, v in replacements.items():
                        content = content.replace(k, str(v))
                    with open(dst_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error procesando {fname}: {e}", file=sys.stderr)

    print(f"[{now_str}] Telemetría de NomadNet actualizada exitosamente en: {out_dir}")

if __name__ == "__main__":
    update_pages()
