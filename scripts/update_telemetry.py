#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Unified NomadNet Telemetry & Sparkline Generator
Auspiciado por CIPRO Panamá (https://www.cipropanama.org)

Genera la página principal de NomadNet en un solo panel integrado (Dashboard)
con historial de 24 horas en micro-gráficos Unicode (sparklines) y métricas en vivo.
"""

import os
import sys
import time
import subprocess
import datetime
import json
import re

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect
import battery_monitor
import environmental_sensor

CONFIG_FILE = "/etc/reticulum-node/node.json"
HISTORY_FILE = "/var/reticulum-node/telemetry_history.json"
PAGES_TEMPLATE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "pages")

SPARK_CHARS = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

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

def get_history_file_path():
    """Gets an accessible path for history storage."""
    for path in [HISTORY_FILE, os.path.expanduser("~/.reticulum-node/telemetry_history.json"), "/tmp/telemetry_history.json"]:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            return path
        except Exception:
            continue
    return "/tmp/telemetry_history.json"

def load_history():
    """Loads historical telemetry data points."""
    path = get_history_file_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def save_history(history):
    """Saves updated historical data points (capped at 24 entries)."""
    path = get_history_file_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history[-24:], f, indent=2)
    except Exception:
        pass

def generate_sparkline(values):
    """Generates a compact Unicode sparkline from a numeric list."""
    if not values or len(values) < 2:
        return "────────────"
    
    clean_vals = [float(v) for v in values if v is not None]
    if not clean_vals:
        return "────────────"
    
    min_v = min(clean_vals)
    max_v = max(clean_vals)
    span = max_v - min_v
    
    if span == 0:
        return "▅" * len(clean_vals)
    
    spark = ""
    for v in clean_vals:
        idx = int(((v - min_v) / span) * (len(SPARK_CHARS) - 1))
        idx = max(0, min(len(SPARK_CHARS) - 1, idx))
        spark += SPARK_CHARS[idx]
    return spark

def generate_bar_gauge(percent, width=10):
    """Generates a text visual progress bar."""
    pct = max(0, min(100, int(percent)))
    filled = int(round((pct / 100.0) * width))
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {pct}%"

def get_rns_status_summary():
    """Runs rnstatus or parses rns logs to get active interfaces and identity."""
    identity = "Generando..."
    active_interfaces = "Consultando..."
    
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
    bat = battery_monitor.get_battery_status()
    env = environmental_sensor.get_environmental_status()
    
    # Update and save history
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    history = load_history()
    entry = {
        "timestamp": now.isoformat(),
        "time_str": now.strftime("%H:%M"),
        "voltage": bat.get("voltage", 0.0),
        "current_ma": bat.get("current_ma", 0.0),
        "cpu_temp": stats.get("cpu_temp", 40.0) if stats.get("cpu_temp") else 40.0,
        "pressure": env.get("pressure_hpa", 1013.25) if env.get("detected") else 1013.25,
        "ram_pct": stats.get("ram_percent", 0)
    }
    
    # Avoid duplicate rapid entries within 5 minutes
    if not history or (now.timestamp() - datetime.datetime.fromisoformat(history[-1]["timestamp"]).timestamp() >= 300):
        history.append(entry)
        save_history(history)
    else:
        history[-1] = entry
        save_history(history)

    # Compute sparklines
    volt_history = [e.get("voltage", 0.0) for e in history if e.get("voltage", 0.0) > 1.0]
    press_history = [e.get("pressure", 1013.0) for e in history if e.get("pressure", 0.0) > 800.0]
    temp_history = [e.get("cpu_temp", 40.0) for e in history if e.get("cpu_temp") is not None]

    spark_bat = generate_sparkline(volt_history[-12:]) if len(volt_history) >= 2 else "────────────"
    spark_press = generate_sparkline(press_history[-12:]) if len(press_history) >= 2 else "────────────"
    spark_temp = generate_sparkline(temp_history[-12:]) if len(temp_history) >= 2 else "────────────"
    
    bat_bar = generate_bar_gauge(bat.get("percentage", 0))
    ram_bar = generate_bar_gauge(stats.get("ram_percent", 0))
    
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
    
    cpu_temp_val = f"{stats['cpu_temp']}°C" if stats['cpu_temp'] else "N/D"
    
    # Format current and power
    curr_str = f"{bat.get('current_ma', 0.0):+.0f} mA" if bat.get("detected") else "N/D"
    pwr_str = f"{bat.get('power_mw', 0.0)/1000.0:.2f} W" if bat.get("detected") else "N/D"
    
    replacements = {
        "{NODE_NAME}": cfg["node_name"],
        "{NODE_LOCATION}": cfg["location"],
        "{NODE_DESCRIPTION}": cfg["description"],
        "{NODE_MODE}": cfg["mode"],
        "{NODE_IDENTITY}": identity,
        "{LXMF_STATUS}": "✅ ACTIVO (Store & Forward + Eco/Comandos)" if cfg.get("enable_lxmf", True) else "❌ Deshabilitado",
        "{SBC_MODEL}": stats["model"],
        "{SBC_ARCH}": stats["arch"],
        "{CPU_TEMP}": cpu_temp_val,
        "{CPU_SPARKLINE}": spark_temp,
        "{LOAD_AVG}": stats["load_avg"],
        "{RAM_USED}": f"{stats['ram_used_mb']} MB",
        "{RAM_TOTAL}": f"{stats['ram_total_mb']} MB",
        "{RAM_PERCENT}": f"{stats['ram_percent']}%",
        "{RAM_BAR}": ram_bar,
        "{UPTIME}": stats["uptime"],
        "{BATTERY_STATUS}": bat["status_str"],
        "{BATTERY_VOLT}": f"{bat.get('voltage', 0.0):.2f} V" if bat.get("detected") else "N/D",
        "{BATTERY_PCT}": f"{bat.get('percentage', 0)}%",
        "{BATTERY_BAR}": bat_bar,
        "{BATTERY_CURRENT}": curr_str,
        "{BATTERY_POWER}": pwr_str,
        "{BATTERY_SPARKLINE}": spark_bat,
        "{BARO_STATUS}": env["status_str"],
        "{ENV_TEMP}": f"{env.get('temperature', 0.0)} °C" if env.get("detected") else "N/D",
        "{ENV_HUMIDITY}": f"{env.get('humidity', 0.0)} %" if env.get("detected") else "N/D",
        "{ENV_PRESSURE}": f"{env.get('pressure_hpa', 0.0)} hPa" if env.get("detected") else "N/D",
        "{ENV_WEATHER}": env.get("weather_status", "N/D"),
        "{ENV_SPARKLINE}": spark_press,
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
