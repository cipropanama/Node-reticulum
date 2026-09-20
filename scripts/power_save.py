#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Power Optimization Utility
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Reduce el consumo eléctrico del SBC (Raspberry Pi, Orange Pi, MangoPi)
desactivando salidas de video HDMI, LEDs de estado y periféricos innecesarios.
"""

import os
import sys
import glob
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def disable_hdmi():
    """Turns off HDMI output to save ~20-30mA of power."""
    success = False
    # 1. Raspberry Pi tvservice
    if os.path.exists("/usr/bin/tvservice"):
        try:
            res = subprocess.run(["/usr/bin/tvservice", "-o"], capture_output=True, text=True)
            if res.returncode == 0:
                logging.info("HDMI desactivado vía tvservice (-25mA).")
                success = True
        except Exception:
            pass

    # 2. Raspberry Pi vcgencmd
    if not success and os.path.exists("/usr/bin/vcgencmd"):
        try:
            subprocess.run(["/usr/bin/vcgencmd", "display_power", "0"], capture_output=True)
            logging.info("Pantalla HDMI apagada vía vcgencmd.")
            success = True
        except Exception:
            pass

    # 3. Generic Linux Framebuffer blanking
    fb_blank = "/sys/class/graphics/fb0/blank"
    if os.path.exists(fb_blank):
        try:
            with open(fb_blank, "w") as f:
                f.write("1\n")
            logging.info("Framebuffer HDMI suspendido.")
            success = True
        except Exception:
            pass

    return success

def disable_status_leds():
    """Turns off onboard LEDs (ACT, PWR) to save power and avoid night visibility."""
    led_paths = glob.glob("/sys/class/leds/*")
    disabled_count = 0
    for p in led_paths:
        trigger_path = os.path.join(p, "trigger")
        brightness_path = os.path.join(p, "brightness")
        try:
            if os.path.exists(trigger_path):
                with open(trigger_path, "w") as f:
                    f.write("none\n")
            if os.path.exists(brightness_path):
                with open(brightness_path, "w") as f:
                    f.write("0\n")
            disabled_count += 1
        except Exception:
            pass
    if disabled_count > 0:
        logging.info(f"LEDs de estado apagados ({disabled_count} LEDs).")
    return disabled_count

def disable_bluetooth():
    """Disables onboard Bluetooth if not in use."""
    try:
        subprocess.run(["rfkill", "block", "bluetooth"], capture_output=True)
        logging.info("Bluetooth desactivado vía rfkill.")
        return True
    except Exception:
        return False

def apply_power_saving(disable_bt=True):
    """Applies all power saving tweaks."""
    logging.info("Aplicando perfil de ahorro de energía CIPRO...")
    disable_hdmi()
    disable_status_leds()
    if disable_bt:
        disable_bluetooth()
    logging.info("✓ Perfil de bajo consumo aplicado.")

if __name__ == "__main__":
    apply_power_saving(disable_bt=True)
