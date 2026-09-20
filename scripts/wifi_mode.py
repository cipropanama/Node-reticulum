#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Tactical Hotspot & WiFi Mode Manager
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Permite alternar entre:
1. Modo Torre / Estación Fija (WiFi Cliente conectado a router o red externa).
2. Modo Táctico Móvil (Crea un Punto de Acceso WiFi 'CIPRO-RESCUE-NODE'
   para que rescatistas y brigadistas con móviles se conecten directamente).
"""

import os
import sys
import subprocess
import shutil

HOTSPOT_SSID = "CIPRO-RESCUE-NODE"
HOTSPOT_IP = "10.0.0.1/24"

def is_root():
    return os.geteuid() == 0

def get_current_wifi_status():
    """Detects active WiFi connections and AP state."""
    if shutil.which("nmcli"):
        try:
            res = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE,DEVICE,STATE", "connection", "show", "--active"], capture_output=True, text=True)
            for line in res.stdout.splitlines():
                if "wireless" in line or "wifi" in line:
                    parts = line.split(":")
                    if "Hotspot" in parts[0] or "CIPRO" in parts[0] or "ap" in parts[0].lower():
                        return "HOTSPOT_AP", parts[0]
                    return "CLIENTE", parts[0]
        except Exception:
            pass
    return "DESCONOCIDO / DESCONECTADO", None

def enable_tactical_hotspot(ssid=HOTSPOT_SSID, password=None):
    """Creates a local WiFi Hotspot for field operators."""
    if not is_root():
        print("\033[31mSe requieren privilegios de superusuario (sudo) para configurar la red WiFi.\033[0m")
        return False

    print(f"\n\033[36mActivando Punto de Acceso Táctico WiFi: '{ssid}'...\033[0m")

    # 1. Try NetworkManager (Standard on Raspberry Pi OS Bookworm, Ubuntu, Armbian)
    if shutil.which("nmcli"):
        try:
            # Delete existing hotspot connection if already defined
            subprocess.run(["nmcli", "connection", "delete", "CiproHotspot"], capture_output=True)
            
            cmd = ["nmcli", "device", "wifi", "hotspot", "ssid", ssid]
            if password and len(password) >= 8:
                cmd += ["password", password]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"\033[32m✓ Punto de acceso '{ssid}' activado con éxito.\033[0m")
                print(f"  Los brigadistas pueden conectarse a la red WiFi '{ssid}'")
                print(f"  y acceder a NomadNet en la dirección IP local de la Raspberry Pi.")
                return True
            else:
                print(f"\033[33mNota nmcli: {res.stderr.strip()}\033[0m")
        except Exception as e:
            print(f"Error al usar nmcli: {e}")

    # 2. Direct message for manual fallback
    print(f"\033[33mPara entornos sin NetworkManager, use hostapd o raspi-config para configurar el AP.\033[0m")
    return False

def disable_hotspot_restore_client():
    """Restores standard WiFi client mode."""
    if not is_root():
        print("\033[31mSe requieren privilegios de superusuario (sudo).\033[0m")
        return False

    print("\n\033[36mRestaurando Modo Estación / Cliente WiFi...\033[0m")
    if shutil.which("nmcli"):
        try:
            subprocess.run(["nmcli", "connection", "down", "Hotspot"], capture_output=True)
            subprocess.run(["nmcli", "connection", "down", "CiproHotspot"], capture_output=True)
            subprocess.run(["nmcli", "device", "wifi", "rescan"], capture_output=True)
            print("\033[32m✓ Modo Punto de Acceso desactivado. Interfaz lista para conectarse a redes existentes.\033[0m")
            return True
        except Exception as e:
            print(f"Error al restaurar: {e}")
    return False

def interactive_menu():
    mode, conn = get_current_wifi_status()
    print("================================================================================")
    print("      🚐 GESTOR DE MODO WIFI TÁCTICO / PUNTO DE ACCESO (CIPRO PANAMÁ)           ")
    print("================================================================================")
    print(f"Estado WiFi Actual: \033[1;36m{mode}\033[0m" + (f" ({conn})" if conn else ""))
    print("\nSeleccione una opción:")
    print("  [1] 📶 Activar Modo Táctico Móvil (Punto de Acceso WiFi 'CIPRO-RESCUE-NODE')")
    print("  [2] 🌐 Volver a Modo Cliente (Conectarse a red WiFi de infraestructura/router)")
    print("  [3] 🔍 Ver Redes WiFi Disponibles en el Área")
    print("  [4] Salir")

    opt = input("\nOpción [1-4]: ").strip()
    if opt == "1":
        pwd = input("Ingrese contraseña WiFi (deje vacío para red abierta de emergencia): ").strip()
        enable_tactical_hotspot(password=pwd if pwd else None)
    elif opt == "2":
        disable_hotspot_restore_client()
    elif opt == "3":
        if shutil.which("nmcli"):
            subprocess.run(["nmcli", "device", "wifi", "list"])
        else:
            print("Comando nmcli no disponible para escanear redes.")

if __name__ == "__main__":
    interactive_menu()
