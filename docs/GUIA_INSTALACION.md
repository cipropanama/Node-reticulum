# Guía de Instalación y Operación: Reticulum Emergency Node

**CIPRO Panamá — Tecnología para ayudar**  
[www.cipropanama.org](https://www.cipropanama.org/)

---

## 1. Requisitos Previos

- **Hardware Recomendado:**
  - Raspberry Pi Zero W / Zero 2W
  - Orange Pi Zero / Zero 2 / Zero 3
  - MangoPi MQ-Pro (Allwinner D1 RISC-V)
  - Tarjeta MicroSD Clase 10 / A1 de al menos 8GB o 16GB.
  - Interfaz LoRa RNode (USB LilyGO T-Beam, T-Echo, RNode DIY SX1262/SX1276 o módem Packet KISS).
  - Fuente de alimentación estable (5V 2A mínimo) o sistema solar/batería de respaldo.

- **Sistema Operativo Soportado:**
  - Raspberry Pi OS Lite (Debian Bookworm / Bullseye)
  - Armbian (Minimal / Server)
  - DietPi
  - Ubuntu Server para ARM/RISC-V

---

## 2. Instalación Automática (1-Línea)

Una vez que el SBC tenga acceso a Internet (por Wi-Fi o Ethernet), abra una terminal y ejecute el siguiente comando:

```bash
curl -sSL https://raw.githubusercontent.com/cipropanama/Node-reticulum/main/install.sh | sudo bash
```

### O clonando directamente desde GitHub:

```bash
git clone https://github.com/cipropanama/ReticulumNode.git
cd ReticulumNode
sudo bash install.sh
```

---

## 3. Asistente de Configuración Inicial

El instalador iniciará automáticamente el asistente interactivo paso a paso:

1. **Nombre del Nodo:** Defina un nombre identificable (ej. `CiproPanama-Emergencia-01`).
2. **Ubicación:** Región o coordenadas aproximadas.
3. **Modo de Transporte:** Mantenga habilitado el modo Transporte para que el nodo retransmita tráfico de la malla.
4. **Nodo de Propagación LXMF (Store-and-Forward):** Habilitado para almacenar mensajes dirigidos a personas que estén fuera de línea y entregárselos al volver a conectarse.
5. **Configuración LoRa (RNode):**
   - Selección automática o manual del puerto serie (`/dev/ttyUSB0` o `/dev/serial0`).
   - Frecuencia recomendada para Panamá y América: **915.0 MHz**.
   - Ancho de banda (BW): `125 kHz`.
   - Spreading Factor: `SF 8` o `SF 9`.
   - Coding Rate: `CR 5` (4/5).
   - Potencia TX: `17 dBm` a `20 dBm`.
6. **Interfaces de Red Local (TCP/UDP):**
   - Servidor TCP en puerto `4242` para permitir que usuarios en el punto de acceso Wi-Fi local se conecten al nodo.

---

## 4. Reconfiguración Posterior (`rns-admin`)

En cualquier momento después de la instalación, puede reconfigurar el nodo, ver estadísticas o crear copias de seguridad ejecutando:

```bash
sudo rns-admin
```

Opciones disponibles en el panel:
- **[1] Ver Estado y Telemetría:** Muestra `rnstatus`, CPU, RAM, temperatura y servicios activos.
- **[2] Reejecutar Asistente:** Permite cambiar frecuencias, nombres o interfaces fácilmente.
- **[3] Ver Registros:** Ver logs de `rnsd`, `nomadnet` y el perro guardián `watchdog`.
- **[4] Gestión de Servicios:** Iniciar, detener o reiniciar la pila de servicios.
- **[5] Copias de Seguridad:** Respaldar y restaurar identidades criptográficas.
- **[6] Actualización:** Descargar la última versión desde GitHub.

---

## 5. Acceso a la Página NomadNet

Cualquier usuario conectado a la red Reticulum (a través de LoRa, WiFi o TCP) podrá acceder a la página Microweb del nodo:
- Abrir la aplicación **NomadNet** o **Sideband**.
- En el explorador de nodos o buscando por el nombre del nodo, podrá consultar la portada con telemetría en vivo, instrucciones de emergencia y la información oficial de **CIPRO Panamá**.

---

## 🤝 Comunidad y Licencia

Este proyecto está liberado bajo la licencia **MIT**. Su uso es totalmente libre para fines experimentales, respuesta a emergencias y proyectos comunitarios solidarios.

Si este desarrollo te ha sido útil, te invitamos a mantener el reconocimiento y el enlace hacia el proyecto original.

### Contacto CIPRO Panamá

- 🌐 **Sitio Web:** [www.cipropanama.org](https://www.cipropanama.org/)
- ✉️ **Correo Electrónico:** [info@cipropanama.org](mailto:info@cipropanama.org)

> **CIPRO Panamá** — _Tecnología para ayudar._  
> Desarrollado con ❤️ para las telecomunicaciones libres.
