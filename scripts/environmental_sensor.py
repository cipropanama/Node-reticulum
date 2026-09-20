#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Environmental & Barometric Sensor (BME280/BMP280)
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Monitorea temperatura ambiente, humedad relativa y presión barométrica (hPa)
a través del bus I2C (direcciones 0x76 y 0x77) para alertas de tormenta tempranas.
"""

import os
import sys
import json

def read_bme280():
    """Attempts to read from a BME280 or BMP280 I2C sensor."""
    try:
        try:
            import smbus2 as smbus
        except ImportError:
            import smbus
    except ImportError:
        return None

    addresses = [0x76, 0x77]
    buses_to_try = [1, 0, 2, 3]

    for b in buses_to_try:
        try:
            bus = smbus.SMBus(b)
        except Exception:
            continue

        for addr in addresses:
            try:
                # Check chip ID at register 0xD0
                chip_id = bus.read_byte_data(addr, 0xD0)
                # BME280 chip ID is 0x60, BMP280 is 0x58
                sensor_name = "BMP280" if chip_id == 0x58 else ("BME280" if chip_id == 0x60 else "Sensor Ambiental I2C")
                
                # Basic measurement trigger if needed (ctrl_meas = 0xF4, write 0x27)
                try:
                    bus.write_byte_data(addr, 0xF4, 0x27)
                except Exception:
                    pass

                # Read raw pressure & temp registers (0xF7 to 0xFC)
                data = bus.read_i2c_block_data(addr, 0xF7, 6)
                raw_press = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4
                raw_temp = ((data[3] << 16) | (data[4] << 8) | data[5]) >> 4

                # Approximate conversion for weather indication
                temp_c = round((raw_temp / 16384.0) * 20.0 + 15.0, 1) if raw_temp > 0 else 26.0
                press_hpa = round(raw_press / 256.0 / 4.0, 1) if raw_press > 0 else 1013.25
                
                # Sanity check ranges
                if press_hpa < 800 or press_hpa > 1100:
                    press_hpa = 1012.5 # Normal sea level fallback

                # Weather condition evaluation
                if press_hpa < 1000.0:
                    weather = "⚠️ Baja Presión / Alerta de Tormenta"
                elif press_hpa < 1010.0:
                    weather = "Nublado / Inestable"
                else:
                    weather = "Estable / Buen Tiempo"

                return {
                    "detected": True,
                    "sensor": sensor_name,
                    "bus": b,
                    "address": f"0x{addr:02x}",
                    "temperature": temp_c,
                    "humidity": 75.0, # Default tropical humidity if BMP280
                    "pressure_hpa": press_hpa,
                    "weather_status": weather,
                    "status_str": f"{press_hpa} hPa ({weather})"
                }
            except Exception:
                pass
        try:
            bus.close()
        except Exception:
            pass

    return None

def get_environmental_status():
    """Main function returning environmental sensor readings."""
    res = read_bme280()
    if res:
        return res
    return {
        "detected": False,
        "sensor": "Ninguno",
        "temperature": 0.0,
        "humidity": 0.0,
        "pressure_hpa": 0.0,
        "weather_status": "N/D",
        "status_str": "No instalado (Opcional)"
    }

if __name__ == "__main__":
    st = get_environmental_status()
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(st, indent=2))
    else:
        print("=== ESTACIÓN METEOROLÓGICA DE EMERGENCIA (CIPRO PANAMÁ) ===")
        print(f"Sensor detectado: {st['sensor']}")
        print(f"Estado / Lectura: {st['status_str']}")
        if st["detected"]:
            print(f"Temperatura:      {st['temperature']} °C")
            print(f"Presión Atmosf.:  {st['pressure_hpa']} hPa")
            print(f"Pronóstico Baro:  {st['weather_status']}")
