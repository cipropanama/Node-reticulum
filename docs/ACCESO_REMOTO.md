# Guía de Acceso Remoto y Gestión en Sitios de Difícil Acceso

**CIPRO Panamá — Tecnología para ayudar**  
[www.cipropanama.org](https://www.cipropanama.org/)

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

## 3. Túneles Remotos sobre Internet (Servidor Central CIPRO Panamá)

Si el nodo dispone de acceso permanente o intermitente a Internet (WiFi local, módem 4G/LTE, enlace satelital Starlink o radioenlace IP):
1. El nodo se conecta automáticamente al **Servidor Central de Reticulum de CIPRO Panamá**:
   - **Host:** `rns.cipropanama.org`
   - **Puerto:** `4242`
2. **Beneficio:** Todos los mensajes de emergencia, telemetría y paquetes LoRa recibidos localmente en tu zona se transmiten y sincronizan a través de Internet con el resto de nodos de la red CIPRO en Panamá y el mundo.
3. Para modificar o deshabilitar este enlace en cualquier momento:
   - Ejecuta `sudo rns-admin` -> Opción `[2]` (Asistente de Configuración) o edita `/root/.reticulum/config`.

---

## 4. Watchdog y Autoreparación Desatendida

Para nodos ubicados en cerros, torres o refugios remotos:
- El servicio `rns-watchdog.timer` se ejecuta cada 2 minutos.
- Si detecta que `rnsd` o `nomadnet` fallaron, los reinicia automáticamente.
- Si la memoria RAM se satura, ejecuta liberación de cachés (`sync && drop_caches`).
- Si se alcanza un número de 5 fallos críticos consecutivos irrecuperables, ejecuta un reinicio controlado del sistema (`systemctl reboot`) para restablecer los buses serie/USB y el subsistema de red.

---

## 🤝 Comunidad y Licencia

Este proyecto está liberado bajo la licencia **MIT**. Su uso es totalmente libre para fines experimentales, respuesta a emergencias y proyectos comunitarios solidarios.

Si este desarrollo te ha sido útil, te invitamos a mantener el reconocimiento y el enlace hacia el proyecto original.

### Contacto CIPRO Panamá

- 🌐 **Sitio Web:** [www.cipropanama.org](https://www.cipropanama.org/)
- ✉️ **Correo Electrónico:** [info@cipropanama.org](mailto:info@cipropanama.org)

> **CIPRO Panamá** — _Tecnología para ayudar._  
> Desarrollado con ❤️ para las telecomunicaciones libres.
