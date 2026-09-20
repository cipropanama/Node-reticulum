#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Terminal QR Code Generator
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Genera códigos QR directamente en la consola para emparejar
dispositivos móviles (Sideband / NomadNet) en 1 segundo escaneando la pantalla.
"""

import os
import sys
import subprocess

def print_qr_code(data, title="CÓDIGO QR DE CONEXIÓN RÁPIDA (SIDEBAND / NOMADNET)"):
    """Prints an ASCII/Unicode QR code to the terminal."""
    print(f"\n\033[1;36m=== {title} ===\033[0m")
    print(f"\033[1mDato a escanear:\033[0m \033[32m{data}\033[0m\n")

    # 1. Try python-qrcode if available
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        print("\n\033[1;33mAbre Sideband o NomadNet en tu móvil y escanea el código QR anterior.\033[0m\n")
        return True
    except ImportError:
        pass

    # 2. Try qrencode cli command if installed
    if os.path.exists("/usr/bin/qrencode"):
        try:
            subprocess.run(["qrencode", "-t", "ANSIUTF8", data])
            print("\n\033[1;33mAbre Sideband o NomadNet en tu móvil y escanea el código QR anterior.\033[0m\n")
            return True
        except Exception:
            pass

    # 3. Fallback: Display plain text and install tip
    print("┌────────────────────────────────────────────────────────────┐")
    print("│ Para visualización gráfica del código QR en terminal,      │")
    print("│ instale qrencode: sudo apt-get install -y qrencode         │")
    print("└────────────────────────────────────────────────────────────┘")
    return False

if __name__ == "__main__":
    test_data = sys.argv[1] if len(sys.argv) > 1 else "reticulum://c4b901fa9e2a87d353689cbda"
    print_qr_code(test_data)
