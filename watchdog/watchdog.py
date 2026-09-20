#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reticulum Emergency Node - Self-Healing Watchdog Daemon
Auspiciado por Cipropanama.org

Supervisa el estado del sistema, daemons de Reticulum/NomadNet,
conectividad de interfaces serie/USB y previene bloqueos en sitios remotos.
"""

import os
import sys
import time
import subprocess
import datetime
import json
import logging

LOG_FILE = "/var/log/reticulum-watchdog.log"
CONFIG_FILE = "/etc/reticulum-node/node.json"
MAX_FAILURES_BEFORE_REBOOT = 5
FAILURE_COUNTER_FILE = "/var/run/reticulum_watchdog_failures"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE) if os.access("/var/log", os.W_OK) else logging.NullHandler()
    ]
)

def get_failure_count():
    if os.path.exists(FAILURE_COUNTER_FILE):
        try:
            with open(FAILURE_COUNTER_FILE, "r") as f:
                return int(f.read().strip())
        except Exception:
            pass
    return 0

def set_failure_count(count):
    try:
        with open(FAILURE_COUNTER_FILE, "w") as f:
            f.write(str(count))
    except Exception:
        pass

def reset_failure_count():
    set_failure_count(0)

def is_service_active(service_name):
    """Checks if a systemd service is active and running."""
    try:
        res = subprocess.run(["systemctl", "--no-ask-password", "is-active", service_name], capture_output=True, text=True, timeout=5)
        return res.stdout.strip() == "active"
    except Exception as e:
        logging.warning(f"No se pudo consultar systemctl para {service_name}: {e}")
        return True # Don't falsely reboot if systemctl isn't available

def restart_service(service_name):
    """Restarts a systemd service."""
    if os.geteuid() != 0:
        logging.warning(f"No se puede reiniciar {service_name}: se requieren privilegios root.")
        return False
    logging.info(f"Intentando reiniciar servicio {service_name}...")
    try:
        res = subprocess.run(["systemctl", "--no-ask-password", "restart", service_name], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            logging.error(f"Fallo al ejecutar restart {service_name}: {res.stderr.strip()}")
            return False
        time.sleep(2)
        if is_service_active(service_name):
            logging.info(f"Servicio {service_name} reiniciado con éxito.")
            return True
        else:
            logging.error(f"Servicio {service_name} falló al iniciar después del reinicio.")
            return False
    except Exception as e:
        logging.error(f"Error al reiniciar {service_name}: {e}")
        return False

def check_memory_and_cleanup():
    """Monitors free RAM and drops caches if memory is critically low."""
    try:
        with open("/proc/meminfo", "r") as f:
            mem = {}
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem[parts[0].strip()] = int(parts[1].strip().split()[0])
        
        avail_kb = mem.get("MemAvailable", 0)
        total_kb = mem.get("MemTotal", 1)
        avail_mb = avail_kb // 1024
        
        # If available memory is less than 20MB or less than 5% of total RAM on small SBC
        if avail_mb < 20 or (avail_kb / total_kb) < 0.05:
            logging.warning(f"Memoria RAM críticamente baja ({avail_mb} MB disponibles). Liberando caché...")
            subprocess.run(["sync"])
            if os.path.exists("/proc/sys/vm/drop_caches"):
                with open("/proc/sys/vm/drop_caches", "w") as f:
                    f.write("3\n")
            logging.info("Caché liberada correctamente.")
    except Exception as e:
        logging.warning(f"Error en verificación de memoria: {e}")

def check_disk_and_cleanup():
    """Cleans up old logs if disk is full to prevent lockups."""
    try:
        st = os.statvfs("/")
        free_percent = (st.f_bavail / st.f_blocks) * 100
        if free_percent < 5:
            logging.warning(f"Espacio en disco críticamente bajo ({free_percent:.1f}% libre). Limpiando logs antiguos...")
            subprocess.run(["journalctl", "--vacuum-size=20M"], capture_output=True)
    except Exception as e:
        logging.warning(f"Error en verificación de disco: {e}")

def check_serial_interfaces():
    """Verifies that configured serial/USB devices exist."""
    if not os.path.exists(CONFIG_FILE):
        return True
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        configured_ports = cfg.get("serial_ports", [])
        for p in configured_ports:
            if not os.path.exists(p):
                logging.warning(f"Puerto de comunicación configurado no encontrado: {p}. Puede haberse desconectado el RNode/Módem.")
                return False
    except Exception as e:
        logging.warning(f"Error al verificar puertos serie: {e}")
    return True

def trigger_controlled_reboot():
    """Performs a safe synchronized reboot of the node to recover from severe lockups."""
    logging.critical("LÍMITE DE FALLOS ALCANZADO. Iniciando reinicio preventivo del nodo para recuperar conectividad...")
    reset_failure_count()
    subprocess.run(["sync"])
    time.sleep(1)
    subprocess.run(["systemctl", "reboot"])

def run_health_check():
    """Executes a full health check cycle."""
    logging.info("--- Ejecutando ciclo de verificación de salud del nodo (Cipropanama.org) ---")
    healthy = True
    
    # 1. Check RAM and Disk
    check_memory_and_cleanup()
    check_disk_and_cleanup()
    
    # 2. Check Services
    services_to_check = ["rnsd", "nomadnet"]
    for s in services_to_check:
        if not is_service_active(s):
            logging.warning(f"El servicio {s} está DETENIDO o INACTIVO.")
            if not restart_service(s):
                healthy = False
        else:
            logging.info(f"Servicio {s}: ACTIVO y funcionando.")

    # 3. Check Serial Interfaces
    if not check_serial_interfaces():
        logging.warning("Dispositivo RNode/Módem ausente. Intentando reiniciar rnsd tras comprobación...")
        # Don't mark as fatal immediately, but log it

    # 4. Update Telemetry Pages
    try:
        update_script = "/usr/local/bin/reticulum-telemetry"
        if os.path.exists(update_script):
            subprocess.run([update_script], timeout=15)
        else:
            # Fallback to relative script path
            script_path = os.path.join(os.path.dirname(__file__), "../scripts/update_telemetry.py")
            if os.path.exists(script_path):
                subprocess.run([sys.executable, script_path], timeout=15)
    except Exception as e:
        logging.warning(f"No se pudo actualizar la telemetría de NomadNet: {e}")

    # 5. Handle Failures & Watchdog threshold
    if not healthy:
        current_fails = get_failure_count() + 1
        set_failure_count(current_fails)
        logging.error(f"Fallo detectado en el ciclo. Contador de fallos consecutivos: {current_fails}/{MAX_FAILURES_BEFORE_REBOOT}")
        if current_fails >= MAX_FAILURES_BEFORE_REBOOT:
            trigger_controlled_reboot()
    else:
        reset_failure_count()
        logging.info("Nodo de Emergencia Reticulum en perfecto estado operativo.")

if __name__ == "__main__":
    run_health_check()
