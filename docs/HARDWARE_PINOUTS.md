# Guía de Conexión de Hardware y Pinouts (SBC a RNode LoRa)

**CIPRO Panamá — Tecnología para ayudar**  
[www.cipropanama.org](https://www.cipropanama.org/)

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

---

## 3. Conexión del Módulo Sensor de Batería Solar INA219 (I2C)

El sensor **INA219** permite medir con alta precisión el voltaje real (0 a 26V DC) y la corriente de la batería solar o banco de 12V/LiFePO4, publicando los datos en la telemetría pública de NomadNet.

<p align="center">
  <img src="img/ina219_wiring.jpg" alt="Diagrama de Conexión Sensor INA219 y Batería Solar" width="850" style="max-width:100%; border-radius:8px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <br>
  <em>Diagrama de conexión: Batería Solar 12V, Sensor INA219, Regulador Step-Down 5V, MicroPC SBC y Radio LoRa RNode.</em>
</p>

### A. Pines Lógicos I2C (Hacia el SBC)

Conecta los 4 pines de control del módulo INA219 a los pines GPIO de tu microcomputador:

| Pin INA219 | Raspberry Pi Zero W / 2W | Orange Pi Zero / Zero 3 | MangoPi MQ-Pro (D1) | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **VCC** | Pin 1 (3.3V) | Pin 1 (3.3V) | Pin 1 (3.3V) | Alimentación lógica del sensor |
| **GND** | Pin 6 / 9 / 14 (GND) | Pin 2 / 8 (GND) | Pin 6 (GND) | Tierra común |
| **SDA** | Pin 3 (GPIO 2 / I2C1_SDA) | Pin 3 (I2C0_SDA) | Pin 3 (TWI2_SDA) | Línea de datos I2C |
| **SCL** | Pin 5 (GPIO 3 / I2C1_SCL) | Pin 5 (I2C0_SCL) | Pin 5 (TWI2_SCL) | Línea de reloj I2C |

---

### B. Conexión de Medición de Potencia (Batería y Carga)

El sensor mide la corriente y voltaje en el lado positivo (*High-Side*):

```
                       [ + ] Borne Positivo Batería (12V)
                               │
                               ▼
                       ┌───────────────┐
                       │  Pin VIN +    │ (Módulo INA219)
                       │               │
                       │  Pin VIN -    │
                       └───────┬───────┘
                               │
                               ▼
              [ + Entrada ] Conversor Step-Down DC-DC (12V a 5.1V)
                               │
                               ▼
                     [ 5V ] Microcomputador SBC / RNode
```

- **`VIN +`**: Conectar directo al polo positivo (+) de la batería de 12V o LiFePO4.
- **`VIN -`**: Conectar a la entrada positiva (+) del regulador/conversor reductor (Step-Down) que alimenta al SBC.
- **`GND`**: Debe estar unido a la tierra común (GND) del sistema.

---

### C. Habilitación del Bus I2C en el Sistema Operativo

1. **En Raspberry Pi OS:**
   ```bash
   sudo raspi-config
   # Seleccionar: Interface Options -> I2C -> Enable -> Yes
   ```
   *O agregando `dtparam=i2c_arm=on` en `/boot/config.txt` (o `/boot/firmware/config.txt`).*

2. **En Armbian (Orange Pi):**
   ```bash
   sudo armbian-config
   # Seleccionar: System -> Hardware -> Marcar 'i2c0' o 'i2c1' -> Guardar
   ```

3. **Verificar detección del sensor en terminal:**
   ```bash
   sudo i2cdetect -y 1
   ```
   *(En Orange Pi Zero puede ser `i2cdetect -y 0`)*.  
   Deberás ver el número **`40`** en la matriz (dirección I2C `0x40`).

Una vez detectado, el sistema Reticulum Emergency Node comenzará a reportar el voltaje de la batería automáticamente en `sudo rns-admin`, en NomadNet y en las respuestas del bot de eco.

---

## 4. Recomendaciones de Energía para Despliegues Remotos

1. **Protección contra bajadas de tensión (Brownout):** Los transmisores LoRa pueden tener picos de consumo durante la transmisión. Coloque un condensador electrolítico de `100uF - 470uF` entre VCC y GND del transceptor si observa reinicios espontáneos.
2. **Sistema de Respaldo Solar:** Panel solar de 20W - 50W con controlador MPPT y batería LiFePO4 de 12V con conversor reductor (Step-down) de alta eficiencia a 5.1V.
3. **Watchdog de Hardware:** El instalador configura el script `watchdog.py` que monitorea periódicamente la estabilidad del sistema y los daemons para evitar cuelgues desatendidos.

---

## 🤝 Comunidad y Licencia

Este proyecto está liberado bajo la licencia **MIT**. Su uso es totalmente libre para fines experimentales, respuesta a emergencias y proyectos comunitarios solidarios.

Si este desarrollo te ha sido útil, te invitamos a mantener el reconocimiento y el enlace hacia el proyecto original.

### Contacto CIPRO Panamá

- 🌐 **Sitio Web:** [www.cipropanama.org](https://www.cipropanama.org/)
- ✉️ **Correo Electrónico:** [info@cipropanama.org](mailto:info@cipropanama.org)

> **CIPRO Panamá** — _Tecnología para ayudar._  
> Desarrollado con ❤️ para las telecomunicaciones libres.
