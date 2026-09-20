#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Solar Battery & Power Monitor
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Monitorea el voltaje y nivel de la batería solar mediante sensores I2C (INA219)
o subsistemas de energía nativos (PMIC /sys/class/power_supply).
"""

import os
import sys
import glob
import json

def read_sysfs_battery():
    """Checks for native kernel power supply devices (AXP PMIC, PiJuice, etc)."""
    supplies = glob.glob("/sys/class/power_supply/*")
    for s in supplies:
        type_file = os.path.join(s, "type")
        if os.path.exists(type_file):
            try:
                with open(type_file, "r") as f:
                    if f.read().strip() == "Battery":
                        v_file = os.path.join(s, "voltage_now")
                        c_file = os.path.join(s, "capacity")
                        volt = 0.0
                        cap = 0
                        if os.path.exists(v_file):
                            with open(v_file, "r") as vf:
                                volt = round(int(vf.read().strip()) / 1000000.0, 2)
                        if os.path.exists(c_file):
                            with open(c_file, "r") as cf:
                                cap = int(cf.read().strip())
                        return {
                            "detected": True,
                            "type": "PMIC / Kernel",
                            "voltage": volt,
                            "current_ma": 0.0,
                            "power_mw": 0.0,
                            "percentage": cap,
                            "status_str": f"{volt}V ({cap}%)"
                        }
            except Exception:
                pass
    return None

def read_ina219_sensor():
    """Attempts to read voltage and current from an INA219 I2C module (addresses 0x40-0x45)."""
    # Try importing smbus or smbus2 if available
    try:
        try:
            import smbus2 as smbus
        except ImportError:
            import smbus
    except ImportError:
        return None

    ina_addresses = [0x40, 0x41, 0x44, 0x45]
    # Check available i2c buses (usually bus 1 on RPi / Orange Pi)
    buses_to_try = [1, 0, 2, 3]

    for b in buses_to_try:
        try:
            bus = smbus.SMBus(b)
        except Exception:
            continue

        for addr in ina_addresses:
            try:
                # Read Bus Voltage Register (Register 0x02)
                raw_v = bus.read_word_data(addr, 0x02)
                raw_v_be = ((raw_v & 0xFF) << 8) | ((raw_v >> 8) & 0xFF)
                voltage_mv = (raw_v_be >> 3) * 4
                voltage = round(voltage_mv / 1000.0, 2)

                # Try reading Shunt Voltage Register (Register 0x01)
                current_ma = 0.0
                power_mw = 0.0
                try:
                    raw_s = bus.read_word_data(addr, 0x01)
                    raw_s_be = ((raw_s & 0xFF) << 8) | ((raw_s >> 8) & 0xFF)
                    # Signed 16-bit
                    if raw_s_be > 32767:
                        raw_s_be -= 65536
                    shunt_mv = raw_s_be * 0.01 # 10 uV per LSB -> 0.01 mV
                    # Assuming Rshunt = 0.1 Ohm (Standard INA219 breakout): I (mA) = Vshunt (mV) / 0.1 Ohm = Vshunt * 10
                    current_ma = round(shunt_mv * 10.0, 1)
                    power_mw = round(abs(voltage * current_ma), 1)
                except Exception:
                    pass

                if voltage > 0.5:
                    # Estimate percentage for typical 12V Lead-Acid / LiFePO4 or 3.7V Li-ion
                    if voltage > 9.0: # 12V system
                        pct = max(0, min(100, int((voltage - 11.5) / (13.6 - 11.5) * 100)))
                    elif voltage > 3.0: # 3.7V / 4.2V system
                        pct = max(0, min(100, int((voltage - 3.3) / (4.2 - 3.3) * 100)))
                    else:
                        pct = 50

                    status_str = f"{voltage}V ({pct}%)"
                    if current_ma != 0.0:
                        status_str += f" | {current_ma:+.0f}mA ({power_mw/1000.0:.2f}W)"

                    return {
                        "detected": True,
                        "type": f"INA219 (I2C Bus {b}, 0x{addr:02x})",
                        "voltage": voltage,
                        "current_ma": current_ma,
                        "power_mw": power_mw,
                        "percentage": pct,
                        "status_str": status_str
                    }
            except Exception:
                pass
        try:
            bus.close()
        except Exception:
            pass

    return None

def get_battery_status():
    """Main function to retrieve battery and solar power metrics."""
    # 1. Try I2C INA219
    res = read_ina219_sensor()
    if res:
        return res

    # 2. Try native kernel PMIC
    res = read_sysfs_battery()
    if res:
        return res

    return {
        "detected": False,
        "type": "Ninguno",
        "voltage": 0.0,
        "current_ma": 0.0,
        "power_mw": 0.0,
        "percentage": 0,
        "status_str": "No instalado (Opcional)"
    }

get_battery_info = get_battery_status

if __name__ == "__main__":
    st = get_battery_status()
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(st, indent=2))
    else:
        print("=== MONITOR DE ENERGÍA SOLAR / BATERÍA (CIPRO PANAMÁ) ===")
        print(f"Sensor detectado: {st['type']}")
        print(f"Estado / Nivel:   {st['status_str']}")
        if st["detected"]:
            print(f"Voltaje medido:   {st['voltage']} V")
            print(f"Nivel estimado:   {st['percentage']} %")
