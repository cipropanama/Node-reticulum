#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Printable Enclosure Datasheet Generator
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Genera una ficha técnica limpia y lista para imprimir en formato HTML y texto
para plastificar y pegar en el interior de la caja estanca (gabinete IP67) del nodo.
"""

import os
import sys
import json
import datetime
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect
import battery_monitor

CONFIG_FILE = "/etc/reticulum-node/node.json"
OUTPUT_HTML = "/etc/reticulum-node/FICHA_TECNICA_NODO.html"
OUTPUT_TXT = "/etc/reticulum-node/FICHA_TECNICA_NODO.txt"

def load_config():
    defaults = {
        "node_name": "CiproPanama-Emergencia-01",
        "location": "Panamá Centro / Móvil",
        "description": "Nodo de Enlace y Mensajería de Emergencia",
        "lora_freq": "915.0",
        "lora_bw": "125",
        "lora_sf": "8",
        "lora_cr": "5",
        "lora_txpower": "17",
        "rnode_port": "/dev/ttyUSB0",
        "enable_transport": True,
        "enable_lxmf": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                defaults.update(json.load(f))
        except Exception:
            pass
    return defaults

def get_node_identity_hash():
    dest_hash = "Desconocido (Ejecute rns-admin)"
    try:
        res = subprocess.run(["rnstatus"], capture_output=True, text=True, timeout=5)
        for line in res.stdout.splitlines():
            if "Destination" in line or "Identity" in line:
                dest_hash = line.strip().split(":")[-1].strip()
                break
    except Exception:
        pass
    return dest_hash

def generate_datasheet():
    cfg = load_config()
    stats = hardware_detect.get_system_stats()
    ident = get_node_identity_hash()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Generate Plain Text Version
    txt_content = f"""
================================================================================
        📡 FICHA TÉCNICA DE NODO DE EMERGENCIA RETICULUM (CIPRO PANAMÁ)
                   Tecnología para ayudar — www.cipropanama.org
================================================================================

1. IDENTIFICACIÓN DEL NODO:
   • Nombre:         {cfg['node_name']}
   • Ubicación:      {cfg['location']}
   • Misión:         {cfg['description']}
   • ID Reticulum:   {ident}
   • Modo:           Transporte Activo + Buzón Store & Forward LXMF

2. PARÁMETROS DE RADIO LORA (RNODE):
   • Frecuencia:     {cfg['lora_freq']} MHz
   • Ancho de Banda: {cfg['lora_bw']} kHz
   • Spreading F.:   SF {cfg['lora_sf']}
   • Coding Rate:    CR {cfg['lora_cr']} (4/{cfg['lora_cr']})
   • Potencia TX:    {cfg['lora_txpower']} dBm
   • Puerto Serie:   {cfg.get('rnode_port', '/dev/ttyUSB0')}

3. ALIMENTACIÓN Y SENSORES:
   • MicroPC (SBC):  {stats['model']} ({stats['arch']})
   • Alimentación:   12V LiFePO4 / Solar -> Step-Down a 5.1V
   • Bus I2C Compartido: Pines SDA:3, SCL:5, 3.3V:1, GND:6
   • Sensor Batería: INA219 (Dir 0x40)
   • Sensor Clima:   BME280 / BMP280 (Dir 0x76/0x77)
   • Enlace Hub:     rns.cipropanama.org:4242

4. GUÍA RÁPIDA PARA RESCATISTAS Y BRIGADISTAS EN CAMPO:
   - Para enviar mensajes: Abre la app Sideband / NomadNet en tu móvil o radio.
   - Sintoniza tu radio LoRa a {cfg['lora_freq']} MHz (SF{cfg['lora_sf']}, BW{cfg['lora_bw']}).
   - Bot de prueba de alcance y eco: Envía 'ping' a '{cfg['node_name']} (Eco & Ping)'.
   - Soporte y Emergencias: info@cipropanama.org | www.cipropanama.org

Fecha de Generación de Ficha: {now_str}
================================================================================
"""

    # 2. Generate Clean Printable HTML Version
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Ficha Técnica: {cfg['node_name']}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 1.5cm;
      color: #111;
      line-height: 1.4;
      font-size: 11pt;
    }}
    .header {{
      border-bottom: 2px solid #0056b3;
      padding-bottom: 8px;
      margin-bottom: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    h1 {{
      font-size: 16pt;
      margin: 0;
      color: #0056b3;
    }}
    .subtitle {{
      font-size: 10pt;
      color: #555;
      font-weight: bold;
    }}
    .grid {{
      display: flex;
      gap: 20px;
      margin-bottom: 15px;
    }}
    .box {{
      flex: 1;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 10px 12px;
      background: #fafafa;
    }}
    .box h2 {{
      font-size: 11pt;
      margin-top: 0;
      margin-bottom: 8px;
      border-bottom: 1px solid #ddd;
      padding-bottom: 4px;
      color: #222;
    }}
    ul {{
      margin: 0;
      padding-left: 18px;
    }}
    li {{
      margin-bottom: 4px;
    }}
    .badge {{
      background: #e1f0ff;
      border: 1px solid #99c7ff;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-weight: bold;
    }}
    .footer {{
      margin-top: 20px;
      border-top: 1px solid #ddd;
      padding-top: 8px;
      font-size: 8.5pt;
      color: #666;
      text-align: center;
    }}
    @media print {{
      body {{ margin: 0.8cm; }}
      .box {{ background: white; }}
    }}
  </style>
</head>
<body>

  <div class="header">
    <div>
      <h1>📡 FICHA TÉCNICA DEL NODO DE EMERGENCIA</h1>
      <div class="subtitle">CIPRO Panamá — Tecnología para ayudar (www.cipropanama.org)</div>
    </div>
    <div style="text-align: right; font-size: 9pt; color: #666;">
      GABINETE ESTANCO IP67<br>
      Ficha: {now_str[:10]}
    </div>
  </div>

  <div class="grid">
    <div class="box">
      <h2>🏷️ Datos del Nodo</h2>
      <ul>
        <li><strong>Nombre:</strong> {cfg['node_name']}</li>
        <li><strong>Ubicación:</strong> {cfg['location']}</li>
        <li><strong>Misión:</strong> {cfg['description']}</li>
        <li><strong>Modo:</strong> Transporte Activo + LXMF</li>
        <li><strong>ID Reticulum:</strong> <span class="badge">{ident}</span></li>
      </ul>
    </div>

    <div class="box">
      <h2>📻 Parámetros de Radio LoRa</h2>
      <ul>
        <li><strong>Frecuencia:</strong> <span class="badge">{cfg['lora_freq']} MHz</span></li>
        <li><strong>Ancho de Banda:</strong> {cfg['lora_bw']} kHz</li>
        <li><strong>Spreading Factor:</strong> SF {cfg['lora_sf']}</li>
        <li><strong>Coding Rate:</strong> CR 4/{cfg['lora_cr']}</li>
        <li><strong>Potencia TX:</strong> {cfg['lora_txpower']} dBm</li>
      </ul>
    </div>
  </div>

  <div class="grid">
    <div class="box">
      <h2>⚡ Hardware y Alimentación</h2>
      <ul>
        <li><strong>SBC (Placa):</strong> {stats['model']} ({stats['arch']})</li>
        <li><strong>Alimentación:</strong> Batería LiFePO4 12V / Panel Solar</li>
        <li><strong>Sensores I2C:</strong> INA219 (Batería) + BME280 (Clima/Barómetro) en SDA:Pin 3, SCL:Pin 5</li>
        <li><strong>Servidor Central:</strong> rns.cipropanama.org (Puerto 4242)</li>
      </ul>
    </div>

    <div class="box">
      <h2>🆘 Instrucciones para Brigadistas</h2>
      <ul>
        <li>Abre la app <strong>Sideband</strong> o <strong>NomadNet</strong> en tu móvil/radio.</li>
        <li>Configura tu transceptor en <strong>{cfg['lora_freq']} MHz (SF{cfg['lora_sf']}, BW{cfg['lora_bw']})</strong>.</li>
        <li>Envía un mensaje con la palabra <code>ping</code> al destino del nodo para verificar alcance y batería.</li>
      </ul>
    </div>
  </div>

  <div class="footer">
    CIPRO Panamá — Proyecto liberado bajo Licencia MIT. Contacto: info@cipropanama.org | www.cipropanama.org
  </div>

</body>
</html>
"""

    out_html = OUTPUT_HTML
    out_txt = OUTPUT_TXT
    try:
        os.makedirs(os.path.dirname(out_html), exist_ok=True)
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt_content)
    except PermissionError:
        user_dir = os.path.expanduser("~/.reticulum")
        os.makedirs(user_dir, exist_ok=True)
        out_html = os.path.join(user_dir, "FICHA_TECNICA_NODO.html")
        out_txt = os.path.join(user_dir, "FICHA_TECNICA_NODO.txt")
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt_content)

    print(f"\n\033[1;32m✓ Ficha técnica generada exitosamente:\033[0m")
    print(f"  • Formato Imprimible HTML: \033[36m{out_html}\033[0m")
    print(f"  • Formato Texto Plano:     \033[36m{out_txt}\033[0m")
    print("\nPuedes abrir el archivo HTML en tu navegador e imprimirlo (Ctrl + P) para plastificarlo.")

if __name__ == "__main__":
    generate_datasheet()
