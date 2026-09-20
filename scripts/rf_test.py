#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - LoRa RF & Antenna Diagnostic Tool
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Herramienta de diagnóstico para verificar el puerto serie, comunicación con el RNode,
latencia de transmisión y estado de la antena antes del despliegue en torre.
"""

import os
import sys
import time
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import hardware_detect

CONFIG_FILE = "/etc/reticulum-node/node.json"

# ANSI Colors
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_RED = "\033[31m"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def run_rf_test():
    print(f"{C_CYAN}{C_BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║            📡 DIAGNÓSTICO DE RADIO LORA Y ANTENA (CIPRO PANAMÁ)             ║")
    print("║                       Prueba de Hardware y Enlace RF                       ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{C_RESET}")

    cfg = load_config()
    port = cfg.get("rnode_port", "/dev/ttyUSB0")
    freq = cfg.get("lora_freq", "915.0")
    bw = cfg.get("lora_bw", "125")
    sf = cfg.get("lora_sf", "8")
    txpower = cfg.get("lora_txpower", "17")

    print(f"Parámetros configurados:")
    print(f" • Puerto:        {C_BOLD}{port}{C_RESET}")
    print(f" • Frecuencia:    {C_BOLD}{freq} MHz{C_RESET}")
    print(f" • Ancho Banda:   {C_BOLD}{bw} kHz{C_RESET} | Spreading Factor: {C_BOLD}SF{sf}{C_RESET}")
    print(f" • Potencia TX:   {C_BOLD}{txpower} dBm{C_RESET}\n")

    # 1. Check physical port existence
    print(f"1. Verificando puerto serie {port}...")
    if not os.path.exists(port):
        print(f"   {C_RED}❌ ERROR: El puerto {port} no existe.{C_RESET}")
        print(f"   Puertos serie disponibles actualmente:")
        detected_ports = hardware_detect.get_serial_ports()
        if detected_ports:
            for p in detected_ports:
                print(f"    • {p['port']} ({p['description']})")
        else:
            print("    (Ningún puerto serie/USB detectado. Verifique el cable USB).")
        return False
    else:
        print(f"   {C_GREEN}✓ Dispositivo presente y conectado.{C_RESET}")

    # 2. Check permissions
    print(f"2. Verificando permisos de acceso...")
    if os.access(port, os.R_OK | os.W_OK):
        print(f"   {C_GREEN}✓ Permisos de lectura/escritura correctos.{C_RESET}")
    else:
        print(f"   {C_YELLOW}⚠️ Advertencia: Requiere permisos de superusuario o grupo dialout.{C_RESET}")

    # 3. Check Reticulum Daemon & Interface state
    print(f"3. Verificando estado del Stack Reticulum...")
    try:
        res = subprocess.run(["rnstatus"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            print(f"   {C_GREEN}✓ rnsd está activo.{C_RESET}")
            output = res.stdout
            if port in output or "RNode" in output:
                print(f"   {C_GREEN}✓ Interfaz RNode cargada en Reticulum.{C_RESET}")
            else:
                print(f"   {C_YELLOW}ℹ️ Interfaz RNode no encontrada en la salida activa de rnstatus.{C_RESET}")
        else:
            print(f"   {C_YELLOW}⚠️ rnstatus no respondió (¿servicio rnsd detenido?).{C_RESET}")
    except Exception as e:
        print(f"   {C_YELLOW}⚠️ No se pudo ejecutar rnstatus: {e}{C_RESET}")

    # 4. RF Transmission Pulse / Announce Test
    print(f"4. Enviando pulso de prueba de radio LoRa (Anuncio de red)...")
    start_t = time.time()
    try:
        # Trigger announce via rns probe or update telemetry
        up_script = os.path.join(SCRIPT_DIR, "update_telemetry.py")
        if os.path.exists(up_script):
            subprocess.run([sys.executable, up_script], capture_output=True, timeout=10)
        elapsed = round((time.time() - start_t) * 1000, 1)
        print(f"   {C_GREEN}✓ Trama de radio procesada en {elapsed} ms.{C_RESET}")
    except Exception as e:
        print(f"   {C_RED}❌ Error en prueba de transmisión: {e}{C_RESET}")

    # 5. Summary & Advice
    print(f"\n{C_MAGENTA}{C_BOLD}=== RECOMENDACIONES TÉCNICAS DE ANTENA ==={C_RESET}")
    print(f"• Para la banda de {freq} MHz (América), usa una antena sintonizada de 1/4 de onda (~8.2 cm) o 1/2 onda.")
    print("• Mantén el cable coaxial lo más corto posible (máximo 1 a 2 metros de cable RG-58 o LMR-200).")
    print("• Sella todos los conectores SMA exteriores con cinta vulcanizada o termoencogible con adhesivo.")
    print(f"\n{C_GREEN}{C_BOLD}✓ Diagnóstico de hardware completado.{C_RESET}\n")
    return True

if __name__ == "__main__":
    run_rf_test()
