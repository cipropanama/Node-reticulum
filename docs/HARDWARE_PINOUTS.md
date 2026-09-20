# Guía de Conexión de Hardware y Pinouts (SBC a RNode LoRa)

**Auspiciado por [Cipropanama.org](https://cipropanama.org)**

---

## 1. Conexión Vía USB (Recomendada y Plug & Play)

Para la mayoría de los despliegues, el método más robusto y sencillo es utilizar un dispositivo RNode conectado por puerto USB:
- **Dispositivos soportados:** LilyGO T-Beam, T-Echo, Heltec LoRa32 v3, RNode DIY basado en ESP32/nRF52.
- **Detección:** Se reconocen automáticamente como `/dev/ttyUSB0` o `/dev/ttyACM0`.
- **Alimentación:** En Raspberry Pi Zero W y MangoPi MQ-Pro, utilice un cable adaptador Micro-USB OTG a USB-A Hembra o USB-C según corresponda.

---

## 2. Conexión Directa por Cabecera de Pines (UART / Header)

Si se conecta un módulo transceptor LoRa UART directo (o microcontrolador RNode a pines GPIO):

### A. Raspberry Pi Zero W / 2W (Header de 40 Pines)
| Señal SBC | Pin Físico | Pin RNode / Módulo | Descripción |
| :--- | :--- | :--- | :--- |
| **5V / 3.3V** | Pin 2 (5V) o Pin 1 (3.3V) | VCC | Alimentación |
| **GND** | Pin 6 / 9 / 14 | GND | Tierra común |
| **TXD (GPIO 14)** | Pin 8 | RX | Transmisión de datos |
| **RXD (GPIO 15)** | Pin 10 | TX | Recepción de datos |

> **Nota para Raspberry Pi:** Habilite el puerto serie UART desactivando la consola serial en `raspi-config` -> `Interface Options` -> `Serial Port`. El puerto será `/dev/serial0` o `/dev/ttyAMA0`.

---

### B. Orange Pi Zero / Zero 3 (Header UART)
| Señal Orange Pi | Header UART | Pin RNode |
| :--- | :--- | :--- |
| **VCC (5V / 3.3V)** | Pin 1 | VCC |
| **GND** | Pin 2 | GND |
| **TX (UART1 / UART5)**| Pin 3 | RX |
| **RX (UART1 / UART5)**| Pin 4 | TX |

---

### C. MangoPi MQ-Pro (Allwinner D1 RISC-V)
| Señal MangoPi | Pin Físico | Pin RNode |
| :--- | :--- | :--- |
| **3.3V** | Pin 1 | VCC |
| **GND** | Pin 6 | GND |
| **UART0 / UART3 TX** | Pin 8 | RX |
| **UART0 / UART3 RX** | Pin 10 | TX |

---

## 3. Recomendaciones de Energía para Despliegues Remotos

1. **Protección contra bajadas de tensión (Brownout):** Los transmisores LoRa pueden tener picos de consumo durante la transmisión. Coloque un condensador electrolítico de `100uF - 470uF` entre VCC y GND del transceptor si observa reinicios espontáneos.
2. **Sistema de Respaldo Solar:** Panel solar de 20W - 50W con controlador MPPT y batería LiFePO4 de 12V con conversor reductor (Step-down) de alta eficiencia a 5.1V.
3. **Watchdog de Hardware:** El instalador configura el script `watchdog.py` que monitorea periódicamente la estabilidad del sistema y los daemons para evitar cuelgues desatendidos.
