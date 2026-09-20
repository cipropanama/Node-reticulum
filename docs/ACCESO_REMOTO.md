# Guía de Acceso Remoto y Gestión en Sitios de Difícil Acceso

**Auspiciado por [Cipropanama.org](https://cipropanama.org)**

---

## 1. Conexión Remota a través de la Red Reticulum

Reticulum permite administrar y comunicarse con el nodo de manera descentralizada sin necesidad de una dirección IP pública:

### A. Utilidades de Diagnóstico Remoto
- **Verificar alcance del nodo:**
  ```bash
  rnpath <DESTINATION_HASH_DEL_NODO>
  ```
- **Probar latencia y calidad de enlace:**
  ```bash
  rnprobe <DESTINATION_HASH_DEL_NODO>
  ```
- **Consultar estado de la interfaz:**
  ```bash
  rnstatus
  ```

---

## 2. Configuración de Punto de Acceso WiFi Local de Mantenimiento

Para acceder al nodo cuando se visita en campo con un teléfono móvil o portátil:
1. El instalador configura la interfaz de red local `AutoInterface` y `TCPServerInterface` en el puerto `4242`.
2. Si el SBC tiene WiFi integrado (ej. Raspberry Pi Zero W), se puede configurar un punto de acceso (AP) independiente usando `NetworkManager` o `hostapd`.
3. Cualquier cliente conectado a la WiFi puede abrir la aplicación **Sideband** o **NomadNet**, conectarse a la IP del nodo en el puerto `4242` y navegar por las páginas Microweb o enviar mensajes a la malla.

---

## 3. Túneles Remotos sobre Internet (Hubs Reticulum)

Si el nodo tiene acceso esporádico o permanente a internet (ej. enlace 4G/LTE, Starlink o radioenlace IP):
1. Ejecute `sudo rns-admin` -> Opción `[2]` (Asistente de Configuración).
2. Habilite **TCP Client Interface**.
3. Ingrese la dirección del Hub comunitario o de la red de emergencia (ej. `hub.reticulum.network` o el servidor privado de Cipropanama).
4. El nodo enrutará automáticamente el tráfico local de LoRa hacia el resto del mundo a través del túnel seguro y encriptado.

---

## 4. Watchdog y Autoreparación Desatendida

Para nodos ubicados en cerros, torres o refugios remotos:
- El servicio `rns-watchdog.timer` se ejecuta cada 2 minutos.
- Si detecta que `rnsd` o `nomadnet` fallaron, los reinicia automáticamente.
- Si la memoria RAM se satura, ejecuta liberación de cachés (`sync && drop_caches`).
- Si se alcanza un número de 5 fallos críticos consecutivos irrecuperables, ejecuta un reinicio controlado del sistema (`systemctl reboot`) para restablecer los buses serie/USB y el subsistema de red.
