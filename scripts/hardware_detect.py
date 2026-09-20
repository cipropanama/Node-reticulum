#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Hardware & System Detection Utility
Auspiciado por Cipropanama.org
"""

import os
import sys
import glob
import platform
import subprocess
import json

def get_sbc_model():
    """Detects the specific Single Board Computer model."""
    # 1. Check device tree model
    dt_model_path = "/proc/device-tree/model"
    if os.path.exists(dt_model_path):
        try:
            with open(dt_model_path, "r", errors="ignore") as f:
                model = f.read().strip().replace('\x00', '')
                if model:
                    return model
        except Exception:
            pass

    # 2. Check /etc/armbian-release
    armbian_path = "/etc/armbian-release"
    if os.path.exists(armbian_path):
        try:
            with open(armbian_path, "r") as f:
                for line in f:
                    if line.startswith("BOARD_NAME="):
                        board = line.split("=")[1].strip().strip('"')
                        return f"Armbian ({board})"
        except Exception:
            pass

    # 3. Check /proc/cpuinfo
    cpuinfo_path = "/proc/cpuinfo"
    if os.path.exists(cpuinfo_path):
        try:
            with open(cpuinfo_path, "r") as f:
                content = f.read()
                if "Raspberry Pi" in content:
                    for line in content.splitlines():
                        if line.startswith("Model"):
                            return line.split(":", 1)[1].strip()
                        if line.startswith("Hardware"):
                            return f"Raspberry Pi ({line.split(':', 1)[1].strip()})"
                if "sun20i" in content or "Allwinner D1" in content or "riscv64" in platform.machine():
                    return "MangoPi MQ-Pro / Allwinner D1 (RISC-V)"
                if "sun8i" in content or "Allwinner H2" in content or "Allwinner H3" in content or "Allwinner H616" in content:
                    return "Orange Pi Zero Series"
        except Exception:
            pass

    # 4. Fallback to generic platform
    arch = platform.machine()
    system = platform.system()
    return f"Generic SBC / Linux ({system} {arch})"

def get_serial_ports():
    """Finds all available USB and Serial UART ports."""
    ports = []
    
    # Check USB to UART adapters
    usb_patterns = ["/dev/ttyUSB*", "/dev/ttyACM*"]
    for pat in usb_patterns:
        for p in sorted(glob.glob(pat)):
            desc = "USB Serial / Modem / RNode"
            ports.append({"port": p, "type": "USB", "description": desc})
            
    # Check Hardware UARTs (RPi, Orange Pi, MangoPi)
    uart_patterns = [
        "/dev/serial0", "/dev/serial1", "/dev/ttyAMA0", "/dev/ttyS0",
        "/dev/ttyS1", "/dev/ttyS2", "/dev/ttyS3", "/dev/ttyS5"
    ]
    for p in uart_patterns:
        if os.path.exists(p) and not any(item["port"] == p for item in ports):
            desc = "Hardware UART / Header Pins"
            ports.append({"port": p, "type": "UART", "description": desc})

    return ports

def get_cpu_temp():
    """Returns the current CPU temperature in Celsius."""
    temp_paths = [
        "/sys/class/thermal/thermal_zone0/temp",
        "/sys/devices/virtual/thermal/thermal_zone0/temp"
    ]
    for tp in temp_paths:
        if os.path.exists(tp):
            try:
                with open(tp, "r") as f:
                    raw = f.read().strip()
                    temp = float(raw) / 1000.0 if float(raw) > 1000 else float(raw)
                    return round(temp, 1)
            except Exception:
                pass
    return None

def get_system_stats():
    """Collects uptime, RAM, swap, CPU load and storage usage."""
    stats = {
        "model": get_sbc_model(),
        "arch": platform.machine(),
        "cpu_temp": get_cpu_temp(),
        "uptime": "Unknown",
        "ram_used_mb": 0,
        "ram_total_mb": 0,
        "ram_percent": 0,
        "disk_used_percent": 0,
        "load_avg": "0.00, 0.00, 0.00"
    }
    
    # Load avg
    try:
        load = os.getloadavg()
        stats["load_avg"] = f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
    except Exception:
        pass

    # Uptime
    if os.path.exists("/proc/uptime"):
        try:
            with open("/proc/uptime", "r") as f:
                uptime_sec = float(f.readline().split()[0])
                days = int(uptime_sec // 86400)
                hours = int((uptime_sec % 86400) // 3600)
                minutes = int((uptime_sec % 3600) // 60)
                if days > 0:
                    stats["uptime"] = f"{days}d {hours}h {minutes}m"
                else:
                    stats["uptime"] = f"{hours}h {minutes}m"
        except Exception:
            pass

    # RAM
    if os.path.exists("/proc/meminfo"):
        try:
            mem = {}
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().split()[0]
                        mem[key] = int(val)
            if "MemTotal" in mem and "MemAvailable" in mem:
                total_mb = round(mem["MemTotal"] / 1024)
                avail_mb = round(mem["MemAvailable"] / 1024)
                used_mb = total_mb - avail_mb
                stats["ram_total_mb"] = total_mb
                stats["ram_used_mb"] = used_mb
                stats["ram_percent"] = round((used_mb / total_mb) * 100, 1) if total_mb > 0 else 0
        except Exception:
            pass

    # Disk
    try:
        st = os.statvfs("/")
        total_disk = st.f_blocks * st.f_frsize
        avail_disk = st.f_bavail * st.f_frsize
        used_disk = total_disk - avail_disk
        if total_disk > 0:
            stats["disk_used_percent"] = round((used_disk / total_disk) * 100, 1)
    except Exception:
        pass

    return stats

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        data = {
            "system": get_system_stats(),
            "serial_ports": get_serial_ports()
        }
        print(json.dumps(data, indent=2))
    else:
        stats = get_system_stats()
        print(f"=== DETECCIÓN DE HARDWARE - RETICULUM NODE ===")
        print(f"Patrocinado por: Cipropanama.org")
        print(f"Modelo SBC:      {stats['model']}")
        print(f"Arquitectura:    {stats['arch']}")
        print(f"Temp. CPU:       {stats['cpu_temp']}°C" if stats['cpu_temp'] else "Temp. CPU:       N/D")
        print(f"Uptime:          {stats['uptime']}")
        print(f"RAM:             {stats['ram_used_mb']} MB / {stats['ram_total_mb']} MB ({stats['ram_percent']}%)")
        print(f"Disco (/):       {stats['disk_used_percent']}% en uso")
        print(f"Carga CPU:       {stats['load_avg']}")
        print("\n--- Puertos Serie / RNode Detectados ---")
        ports = get_serial_ports()
        if ports:
            for p in ports:
                print(f" - [{p['type']}] {p['port']} ({p['description']})")
        else:
            print(" (No se detectaron puertos serie o USB activos)")
