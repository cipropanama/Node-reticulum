#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - LXMF Command & Telemetry Responder
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Bot interactivo de telemetría, diagnóstico y prueba de eco sobre LXMF.
Permite a voluntarios y brigadistas consultar en tiempo real el estado del nodo:
- ping / eco
- status (resumen completo)
- bat / bateria / power
- env / clima / weather
- net / mesh / radio
- help / ayuda
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
import environmental_sensor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

CONFIG_FILE = "/etc/reticulum-node/node.json"

def load_node_config():
    defaults = {
        "node_name": "Reticulum-Emergency-Node",
        "location": "No especificada / Móvil",
        "lora_freq": "915.0",
        "lora_bw": "125",
        "lora_sf": "8"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception:
            pass
    return defaults

def build_response(command_str):
    """Parses incoming command string and returns title and content."""
    cmd = command_str.strip().lower()
    cfg = load_node_config()
    stats = hardware_detect.get_system_stats()
    bat = battery_monitor.get_battery_status()
    env = environmental_sensor.get_environmental_status()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Command: BAT / POWER
    if cmd in ["bat", "bateria", "batería", "power", "energia", "energía"]:
        title = f"🔋 Energía [{cfg['node_name']}]"
        curr_str = f"{bat.get('current_ma', 0.0):+.0f} mA" if bat.get("detected") else "N/D"
        pwr_str = f"{bat.get('power_mw', 0.0)/1000.0:.2f} W" if bat.get("detected") else "N/D"
        body = (
            f"🔋 ESTADO DE ENERGÍA SOLAR\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Nodo:      {cfg['node_name']}\n"
            f"• Sensor:    {bat['type']}\n"
            f"• Voltaje:   {bat.get('voltage', 0.0):.2f} V\n"
            f"• Nivel:     {bat.get('percentage', 0)} %\n"
            f"• Corriente: {curr_str}\n"
            f"• Consumo:   {pwr_str}\n"
            f"• Hora:      {now_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"CIPRO Panamá — www.cipropanama.org"
        )
        return title, body

    # Command: ENV / CLIMA / WEATHER
    elif cmd in ["env", "clima", "weather", "meteo", "sensor"]:
        title = f"⛅ Clima [{cfg['node_name']}]"
        body = (
            f"⛅ ESTACIÓN METEOROLÓGICA LOCAL\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Nodo:        {cfg['node_name']}\n"
            f"• Sensor:      {env['sensor']}\n"
            f"• Temperatura: {env.get('temperature', 0.0)} °C\n"
            f"• Humedad:     {env.get('humidity', 0.0)} %\n"
            f"• Presión:     {env.get('pressure_hpa', 0.0)} hPa\n"
            f"• Diagnóstico: {env.get('weather_status', 'N/D')}\n"
            f"• Hora:        {now_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"CIPRO Panamá — www.cipropanama.org"
        )
        return title, body

    # Command: NET / RADIO / MESH
    elif cmd in ["net", "mesh", "radio", "lora"]:
        title = f"📻 Radio [{cfg['node_name']}]"
        body = (
            f"📻 ESTADO DE RADIO Y RED RETICULUM\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Nodo:        {cfg['node_name']}\n"
            f"• Frecuencia:  {cfg['lora_freq']} MHz\n"
            f"• Ancho Banda: {cfg['lora_bw']} kHz\n"
            f"• Spreading F: SF{cfg['lora_sf']}\n"
            f"• Modo RNS:    Transporte / Mesh\n"
            f"• Hora:        {now_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"CIPRO Panamá — www.cipropanama.org"
        )
        return title, body

    # Command: HELP / AYUDA
    elif cmd in ["help", "ayuda", "?", "comandos"]:
        title = f"ℹ️ Comandos [{cfg['node_name']}]"
        body = (
            f"🤖 COMANDOS DISPONIBLES LXMF\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Envía cualquiera de estos textos:\n"
            f"• status : Resumen general de telemetría\n"
            f"• bat    : Voltaje, corriente y % batería\n"
            f"• env    : Clima, temp, humedad y presión\n"
            f"• net    : Parámetros LoRa y malla\n"
            f"• ping   : Prueba de alcance y eco\n"
            f"• help   : Este menú de ayuda\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"CIPRO Panamá — www.cipropanama.org"
        )
        return title, body

    # Default / Command: STATUS or PING / ECHO
    else:
        is_ping = (cmd in ["ping", "test", "eco", "echo", "hola"])
        title = f"📡 Telemetría [{cfg['node_name']}]" if not is_ping else f"✓ Eco OK [{cfg['node_name']}]"
        
        body = (
            f"📡 TELEMETRÍA NODO DE EMERGENCIA\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Nodo:        {cfg['node_name']}\n"
            f"• Ubicación:   {cfg['location']}\n"
            f"• Batería:     {bat['status_str']}\n"
            f"• Ambiente:    {env['status_str']}\n"
            f"• Hardware:    {stats['model']}\n"
            f"• CPU / Temp:  {stats['cpu_temp']}°C | RAM: {stats['ram_percent']}%\n"
            f"• Uptime:      {stats['uptime']}\n"
            f"• LoRa:        {cfg['lora_freq']} MHz (SF{cfg['lora_sf']})\n"
            f"• Hora local:  {now_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✓ Enlace confirmado por Reticulum Mesh\n"
            f"CIPRO Panamá — www.cipropanama.org"
        )
        return title, body

def run_responder_bot():
    try:
        import RNS
        import LXMF
    except ImportError:
        logging.error("RNS o LXMF no están instalados. Ejecute: pip install rns lxmf")
        sys.exit(1)

    cfg = load_node_config()
    display_name = f"{cfg['node_name']} (Bot Telemetría)"

    logging.info(f"Iniciando Bot de Telemetría y Comandos LXMF para: {display_name}")
    
    # Initialize Reticulum
    rns = RNS.Reticulum()

    # Identity for Bot
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
        logging.info(f"Mensaje recibido desde <{sender_hash}>: '{title}' / '{content}'")

        command_text = content if content.strip() else title
        resp_title, resp_body = build_response(command_text)

        try:
            reply = LXMF.LXMessage(
                destination=message.source_hash,
                source=destination,
                content=resp_body,
                title=resp_title,
                desired_method=LXMF.LXMessage.DIRECT
            )
            router.handle_outbound(reply)
            logging.info(f"Respuesta enviada hacia <{sender_hash}>: '{resp_title}'")
        except Exception as e:
            logging.error(f"Error al enviar respuesta LXMF: {e}")

    # Attach receiver callback
    router.delivery_callback = message_received

    # Announce destination to the mesh
    destination.announce()
    logging.info(f"Bot de Telemetría activo y anunciado en Reticulum. Hash: {RNS.hexrep(destination.hash, False)}")

    # Keep alive waiting on events
    try:
        while True:
            time.sleep(300)
            destination.announce()
    except KeyboardInterrupt:
        logging.info("Bot detenido por el operador.")

if __name__ == "__main__":
    run_responder_bot()
