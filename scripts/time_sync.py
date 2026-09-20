#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Offline Time Sync & GPS Daemon
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)

Sincroniza la hora del sistema en nodos aislados sin conexión a Internet utilizando:
1. Módulo RTC por hardware I2C (DS3231 / DS1307 en dirección 0x68).
2. Módulo GPS NMEA por puerto serie (USB / UART).
3. Exporta coordenadas geográficas GPS para telemetría y páginas NomadNet.
"""

import os
import sys
import time
import glob
import json
import datetime
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

GPS_DATA_FILE = "/etc/reticulum-node/gps.json"
RTC_I2C_ADDRESS = 0x68

def bcd_to_dec(val):
    """Converts Binary Coded Decimal to integer."""
    return (val // 16 * 10) + (val % 16)

def dec_to_bcd(val):
    """Converts integer to Binary Coded Decimal."""
    return (val // 10 * 16) + (val % 10)

def read_rtc_ds3231():
    """Reads hardware clock time directly from DS3231 I2C register."""
    try:
        import smbus2
    except ImportError:
        try:
            import smbus as smbus2
        except ImportError:
            return None

    # Scan I2C buses (1 for Pi, 0 for Orange Pi)
    for bus_num in [1, 0, 2]:
        try:
            bus = smbus2.SMBus(bus_num)
            # Read first 7 registers (seconds, minutes, hours, day, date, month, year)
            data = bus.read_i2c_block_data(RTC_I2C_ADDRESS, 0x00, 7)
            bus.close()
            
            sec = bcd_to_dec(data[0] & 0x7F)
            minute = bcd_to_dec(data[1] & 0x7F)
            hour = bcd_to_dec(data[2] & 0x3F)
            day = bcd_to_dec(data[4] & 0x3F)
            month = bcd_to_dec(data[5] & 0x1F)
            year = 2000 + bcd_to_dec(data[6])
            
            dt = datetime.datetime(year, month, day, hour, minute, sec)
            return dt
        except Exception:
            continue
    return None

def set_system_time(dt):
    """Sets system time if current time is not synchronized (e.g. before 2024)."""
    current_year = datetime.datetime.now().year
    if current_year < 2024:
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\033[32m[TimeSync] Sincronizando hora del sistema a: {time_str}...\033[0m")
        try:
            subprocess.run(["date", "-s", time_str], check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"\033[31m[TimeSync] Error al ajustar fecha del sistema: {e}\033[0m")
    return False

def parse_nmea_coordinates(raw_val, direction):
    """Converts NMEA DDMM.MMMM to decimal degrees."""
    if not raw_val:
        return 0.0
    try:
        if direction in ['N', 'S']:
            deg = float(raw_val[:2])
            mins = float(raw_val[2:])
        else:
            deg = float(raw_val[:3])
            mins = float(raw_val[3:])
        decimal = deg + (mins / 60.0)
        if direction in ['S', 'W']:
            decimal = -decimal
        return round(decimal, 6)
    except Exception:
        return 0.0

def read_gps_serial(timeout_seconds=3):
    """Scans serial ports for GPS NMEA sentences."""
    try:
        import serial
    except ImportError:
        return None

    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*") + ["/dev/serial0", "/dev/ttyAMA0"]
    baudrates = [9600, 115200, 38400, 4800]

    for port in ports:
        if not os.path.exists(port):
            continue
        for baud in baudrates:
            try:
                ser = serial.Serial(port, baudrate=baud, timeout=0.8)
                start_t = time.time()
                while time.time() - start_t < timeout_seconds:
                    line = ser.readline().decode("latin1", errors="ignore").strip()
                    if line.startswith(("$GPRMC", "$GNRMC")):
                        parts = line.split(",")
                        if len(parts) >= 10:
                            status = parts[2]
                            time_raw = parts[1]
                            date_raw = parts[9]
                            lat_raw = parts[3]
                            lat_dir = parts[4]
                            lon_raw = parts[5]
                            lon_dir = parts[6]
                            
                            gps_info = {
                                "port": port,
                                "baud": baud,
                                "has_fix": (status == "A"),
                                "latitude": parse_nmea_coordinates(lat_raw, lat_dir) if status == "A" else None,
                                "longitude": parse_nmea_coordinates(lon_raw, lon_dir) if status == "A" else None,
                                "datetime": None
                            }
                            
                            if len(time_raw) >= 6 and len(date_raw) == 6:
                                try:
                                    h, m, s = int(time_raw[0:2]), int(time_raw[2:4]), int(time_raw[4:6])
                                    d, mo, y = int(date_raw[0:2]), int(date_raw[2:4]), 2000 + int(date_raw[4:6])
                                    gps_dt = datetime.datetime(y, mo, d, h, m, s)
                                    gps_info["datetime"] = gps_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                                    # Sync system clock if valid fix
                                    if status == "A":
                                        set_system_time(gps_dt)
                                except Exception:
                                    pass
                            
                            ser.close()
                            return gps_info
                ser.close()
            except Exception:
                pass
    return None

def run_sync():
    """Runs a full time synchronization & GPS detection check."""
    print("=== 🛰️ SINCRONIZACIÓN DE HORA OFFLINE Y GPS (CIPRO PANAMÁ) ===")
    
    # 1. Check RTC DS3231
    rtc_dt = read_rtc_ds3231()
    if rtc_dt:
        print(f"\033[32m✓ Módulo RTC por hardware DS3231 detectado en I2C (0x68).\033[0m")
        print(f"  Hora RTC: {rtc_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        set_system_time(rtc_dt)
    else:
        print("\033[33m• No se detectó módulo RTC DS3231 en bus I2C (0x68).\033[0m")

    # 2. Check GPS Serial
    print("Buscando módulos GPS serie en puertos locales...")
    gps_info = read_gps_serial(timeout_seconds=2)
    if gps_info:
        print(f"\033[32m✓ Receptor GPS detectado en {gps_info['port']} ({gps_info['baud']} bps).\033[0m")
        if gps_info["has_fix"]:
            print(f"  Posición Fix: Lat {gps_info['latitude']}, Lon {gps_info['longitude']}")
            print(f"  Hora GPS:     {gps_info['datetime']}")
            # Save to json file
            try:
                os.makedirs(os.path.dirname(GPS_DATA_FILE), exist_ok=True)
                with open(GPS_DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(gps_info, f, indent=2)
            except Exception:
                pass
        else:
            print("  Receptor buscando satélites (sin fix 3D aún)...")
    else:
        print("• No se detectó receptor GPS en los puertos serie.")

    print(f"Hora actual del sistema: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_sync()
