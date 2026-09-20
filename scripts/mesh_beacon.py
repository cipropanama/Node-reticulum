#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Mesh Beacon & Announce Daemon
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Emite periódicamente anuncios criptográficos (Announces) en la red de malla
Reticulum para que radios y usuarios con Sideband descubran automáticamente
la presencia del repetidor y las rutas hacia el nodo central.
"""

import os
import sys
import time
import json
import logging
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect
import battery_monitor
import environmental_sensor

CONFIG_FILE = "/etc/reticulum-node/node.json"
BEACON_IDENTITY_FILE = "/etc/reticulum-node/beacon.identity"
DEFAULT_INTERVAL_MINUTES = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Beacon] %(message)s"
)

def load_node_config():
    cfg = {
        "node_name": "CiproPanama-Emergencia-01",
        "beacon_interval_min": DEFAULT_INTERVAL_MINUTES,
        "enable_beacon": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    return cfg

def generate_beacon_payload(cfg):
    """Compiles a short compact telemetry payload for the announce."""
    stats = hardware_detect.get_system_stats()
    bat = battery_monitor.get_battery_info()
    env = environmental_sensor.get_environmental_info()
    
    bat_str = f"{bat['voltage_v']}V" if bat and bat.get("voltage_v") else "AC"
    press_str = f"{env['pressure_hpa']}hPa" if env and env.get("pressure_hpa") else ""
    storm_flag = " [ALERTA TORMENTA]" if env and env.get("storm_alert") else ""

    payload_text = f"[{cfg['node_name']}] Bat:{bat_str} CPU:{stats['cpu_temp']}°C {press_str}{storm_flag} | Cipropanama.org"
    return payload_text.encode("utf-8")

def send_announce():
    """Initializes RNS and sends a single Announce packet."""
    try:
        import RNS
    except ImportError:
        logging.error("Librería RNS (Reticulum) no instalada.")
        return False

    cfg = load_node_config()
    if not cfg.get("enable_beacon", True):
        logging.info("Anuncios de baliza deshabilitados en configuración.")
        return False

    try:
        r = RNS.Reticulum()
    except Exception as e:
        logging.warning(f"Error al conectar con instancia de Reticulum: {e}")

    # Load or create beacon identity
    try:
        os.makedirs(os.path.dirname(BEACON_IDENTITY_FILE), exist_ok=True)
        if os.path.exists(BEACON_IDENTITY_FILE):
            identity = RNS.Identity.from_file(BEACON_IDENTITY_FILE)
        else:
            identity = RNS.Identity()
            identity.to_file(BEACON_IDENTITY_FILE)
    except Exception:
        identity = RNS.Identity()

    dest = RNS.Destination(identity, RNS.Destination.IN, RNS.Destination.SINGLE, "cipro", "emergency", "beacon")
    app_data = generate_beacon_payload(cfg)
    
    dest.announce(app_data=app_data)
    logging.info(f"✓ Announce de malla emitido: {app_data.decode('utf-8', errors='ignore')}")
    return True

def run_loop():
    """Daemon loop emitting announces at configured intervals."""
    logging.info("Iniciando servicio de baliza periódica de malla (Mesh Beacon)...")
    while True:
        cfg = load_node_config()
        interval_sec = max(5, int(cfg.get("beacon_interval_min", DEFAULT_INTERVAL_MINUTES)) * 60)
        send_announce()
        time.sleep(interval_sec)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mesh Beacon Daemon")
    parser.add_argument("--oneshot", action="store_true", help="Send a single announce and exit")
    args = parser.parse_args()

    if args.oneshot:
        send_announce()
    else:
        run_loop()
