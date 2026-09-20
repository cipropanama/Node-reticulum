#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - LXMF Echo & Coverage Test Responder
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Bot automático y ligero de prueba de cobertura y eco sobre LXMF.
Permite a voluntarios y brigadistas en el terreno enviar 'ping' o 'test'
y recibir confirmación automática con telemetría y calidad de señal.
"""

import os
import sys
import time
import datetime
import json
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect
import battery_monitor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

CONFIG_FILE = "/etc/reticulum-node/node.json"

def load_node_name():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("node_name", "CiproPanama-Emergencia")
        except Exception:
            pass
    return "CiproPanama-Emergencia"

def run_echo_bot():
    try:
        import RNS
        import LXMF
    except ImportError:
        logging.error("RNS o LXMF no están instalados. Ejecute: pip install rns lxmf")
        sys.exit(1)

    node_name = load_node_name()
    display_name = f"{node_name} (Eco & Ping)"

    logging.info(f"Iniciando Bot de Eco LXMF para: {display_name}")
    
    # Initialize Reticulum
    rns = RNS.Reticulum()

    # Identity for Echo Bot
    identity_path = "/etc/reticulum-node/echo_identity"
    os.makedirs(os.path.dirname(identity_path), exist_ok=True)
    
    if os.path.exists(identity_path):
        identity = RNS.Identity.from_file(identity_path)
    else:
        identity = RNS.Identity()
        try:
            identity.to_file(identity_path)
        except Exception:
            pass

    # Create LXMF router & destination
    router = LXMF.LXMRouter(identity=identity, storagepath="/var/reticulum-node/lxmf_echo")
    destination = router.register_delivery_identity(identity, display_name=display_name)

    # Callback when a message is received
    def message_received(message):
        sender_hash = RNS.hexrep(message.source_hash, False)
        title = message.title_as_string()
        content = message.content_as_string()
        logging.info(f"Mensaje de prueba recibido desde <{sender_hash}>: '{title}' / '{content}'")

        # Collect current telemetry
        stats = hardware_detect.get_system_stats()
        bat = battery_monitor.get_battery_status()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        reply_body = (
            f"📡 CONFIRMACIÓN DE ECO - NODO DE EMERGENCIA\n"
            f"==========================================\n"
            f"✓ Tu mensaje fue recibido con éxito.\n"
            f"• Nodo:        {node_name}\n"
            f"• Hora local:  {now_str}\n"
            f"• Hardware:    {stats['model']}\n"
            f"• CPU / Temp:  {stats['cpu_temp']}°C | Uptime: {stats['uptime']}\n"
            f"• Batería:     {bat['status_str']}\n"
            f"------------------------------------------\n"
            f"¡Enlace de radio y alcance confirmados!\n"
            f"CIPRO Panamá — www.cipropanama.org\n"
            f"=========================================="
        )

        try:
            # Send reply
            reply = LXMF.LXMessage(
                destination=message.source_hash,
                source=destination,
                content=reply_body,
                title="Respuesta de Eco / Cobertura OK",
                desired_method=LXMF.LXMessage.DIRECT
            )
            router.handle_outbound(reply)
            logging.info(f"Respuesta de eco despachada hacia <{sender_hash}>.")
        except Exception as e:
            logging.error(f"Error al enviar respuesta de eco: {e}")

    # Attach receiver callback
    router.delivery_callback = message_received

    # Announce destination to the mesh
    destination.announce()
    logging.info(f"Bot de Eco activo y anunciado en la malla Reticulum. Hash: {RNS.hexrep(destination.hash, False)}")

    # Keep alive waiting on events (zero busy loop, sleep interval)
    try:
        while True:
            time.sleep(300)
            # Re-announce every 20 minutes
            destination.announce()
    except KeyboardInterrupt:
        logging.info("Bot de Eco detenido por el operador.")

if __name__ == "__main__":
    run_echo_bot()
