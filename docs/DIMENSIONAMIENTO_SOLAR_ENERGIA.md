# Guía de Dimensionamiento Energético y Solar para Nodos Reticulum

**CIPRO Panamá — Tecnología para ayudar**  
[www.cipropanama.org](https://www.cipropanama.org/) • [info@cipropanama.org](mailto:info@cipropanama.org)

Esta guía técnica proporciona los **datos de consumo eléctrico real**, **comparativas de baterías** y **tablas de dimensionamiento de paneles solares** para garantizar que el **Nodo de Emergencia Reticulum** opere de forma **100% ininterrumpida (24/7/365)** en puntos remotos y de difícil acceso (cerros, torres, selva o zonas de desastre).

---

## 1. Consumo Eléctrico Real por Tipo de Microcomputadora (SBC)

Los consumos a continuación incluyen el **sistema completo en operación continua**:
* Microcomputador corriendo Linux (RNS Daemon + NomadNet + Watchdogs).
* Radio transceptor LoRa ESP32 / RNode en modo escucha continua (RX) y balizas periódicas (TX).
* Sensores I2C en paralelo (INA219 + BME280 + Reloj RTC DS3231).
* Pérdidas por eficiencia del conversor Step-Down DC-DC Buck (~88% de rendimiento).

| Microcomputadora / Plataforma | Voltaje SBC | Corriente Promedio | Potencia Promedio | Consumo Diario (24h) | Amperios-Hora Diarios (Línea 12V) | Nivel de Idoneidad para Sitios Remotos |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **ESP32 Standalone (RNode Puro)** *(Sin Linux, Repetidor LoRa)* | 3.3V / 5V | ~60 mA | **0.30 W** | **7.2 Wh / día** | **0.60 Ah / día** | 🟢 **Excelente** (Micro-solar 5W / Bat 6Ah) |
| **Raspberry Pi Zero W** *(Recomendada)* | 5.1V | ~180 mA | **0.90 W** | **21.6 Wh / día** | **1.80 Ah / día** | 🟢 **Óptima** (Equilibrio perfecto bajo consumo + NomadNet) |
| **Raspberry Pi Zero 2 W** *(Quad-Core 64-bit)* | 5.1V | ~240 mA | **1.22 W** | **29.3 Wh / día** | **2.44 Ah / día** | 🟢 **Muy Buena** (Mayor potencia CPU, bajo consumo) |
| **Orange Pi Zero 3 / Zero 2** *(Allwinner H618)* | 5.0V | ~320 mA | **1.60 W** | **38.4 Wh / día** | **3.20 Ah / día** | 🟡 **Buena** (Económica, consumo moderado) |
| **MangoPi MQ-Pro** *(Allwinner D1 RISC-V)* | 5.0V | ~210 mA | **1.05 W** | **25.2 Wh / día** | **2.10 Ah / día** | 🟢 **Muy Buena** (Arquitectura abierta RISC-V) |
| **Raspberry Pi 3B+** *(Quad-Core A53)* | 5.1V | ~550 mA | **2.80 W** | **67.2 Wh / día** | **5.60 Ah / día** | 🟠 **Aceptable** (Requiere panel y batería medianos) |
| **Raspberry Pi 4B / 5** *(Gateway / Servidor Central)* | 5.1V | ~800 mA | **4.10 W** | **98.4 Wh / día** | **8.20 Ah / día** | 🔴 **Solo con Red / Solar Grande** (>50W Panel) |

> 💡 **Regla de Oro:** Para instalaciones en sitios remotos sin mantenimiento, la **Raspberry Pi Zero W** o **Zero 2 W** es la opción ideal: consume menos de **1 Vatio**, permitiendo operar con paneles y baterías muy compactos.

---

## 2. Comparativa Técnica de Tecnologías de Batería

Para sitios inaccesibles, no todas las baterías son iguales. La **Profundidad de Descarga (DoD)** y los **Ciclos de Vida Útil** determinan cuánta energía real se puede extraer sin dañar la celda:

```
  ┌──────────────────────┬─────────────┬─────────────┬──────────────┬────────────────────────────┐
  │ Química de Batería   │ DoD Útil    │ Ciclos Vida │ Rendimiento  │ Resistencia a Calor Trópico│
  ├──────────────────────┼─────────────┼─────────────┼──────────────┼────────────────────────────┤
  │ LiFePO4 (12.8V)      │ 90%         │ 3000 - 5000 │ 95%          │ ⭐⭐⭐⭐⭐ Excelente (Segura)│
  │ Li-Ion 18650 (3S)    │ 80%         │ 500 - 800   │ 90%          │ ⭐⭐⭐   Moderada (BMS req) │
  │ Plomo-Ácido AGM/Gel  │ 50%         │ 300 - 500   │ 75%          │ ⭐⭐    Pobre a >35°C      │
  └──────────────────────┴─────────────┴─────────────┴──────────────┴────────────────────────────┘
```

### Detalle de cada tecnología:
1. **LiFePO4 (Litio Ferrofosfato - 12.8V):** *(Recomendación CIPRO Panamá)*
   - Puedes usar el **90% de su capacidad nominal** sin degradarla.
   - Vida útil de **8 a 10 años** (más de 3,500 ciclos diarios).
   - Químicamente estable: no explota ni se incendia ante altas temperaturas o sobrecargas.
2. **Li-Ion (Celdas 18650 / 21700 en arreglo 3S 11.1V–12.6V):**
   - Muy ligera y compacta. Requiere placa de protección BMS (*Battery Management System*) obligatoria.
   - Vida útil de **2 a 3 años** (500–800 ciclos).
3. **Plomo-Ácido / AGM / Gel (12V Automotriz o Sellada VRLA):**
   - **Solo permite usar el 50% de su capacidad**. Si descargas una batería de plomo al 100%, morirá en menos de 3 meses.
   - Muy pesada para transportar a cerros a pie, pero económica y disponible en cualquier ferretería local.

---

## 3. Matriz de Autonomía sin Sol (Días de Respaldo Continuo)

Días completos que el nodo puede funcionar **en total oscuridad / lluvia continua** según la capacidad de la batería:

| Capacidad Batería (12V) | Energía Útil (LiFePO4 - 90% DoD) | Energía Útil (Plomo AGM - 50% DoD) | Autonomía: RPi Zero W (0.9W) | Autonomía: RPi Zero 2W (1.2W) | Autonomía: Orange Pi Zero 3 (1.6W) | Autonomía: ESP32 RNode (0.3W) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **6 Ah (LiFePO4)** | **69.1 Wh** | — | **3.2 Días** (76 horas) | **2.3 Días** (56 horas) | **1.8 Días** (43 horas) | **9.6 Días** (230 horas) |
| **10 Ah (LiFePO4)** | **115.2 Wh** | — | **5.3 Días** (128 horas) | **3.9 Días** (94 horas) | **3.0 Días** (72 horas) | **16.0 Días** (384 horas) |
| **12 Ah (LiFePO4)** | **138.2 Wh** | — | **6.4 Días** (153 horas) | **4.7 Días** (113 horas) | **3.6 Días** (86 horas) | **19.2 Días** (460 horas) |
| **20 Ah (LiFePO4)** | **230.4 Wh** | — | **10.6 Días** (256 horas) | **7.8 Días** (188 horas) | **6.0 Días** (144 horas) | **32.0 Días** (768 horas) |
| **18 Ah (Plomo AGM)** | — | **108.0 Wh** | **5.0 Días** (120 horas) | **3.6 Días** (88 horas) | **2.8 Días** (67 horas) | **15.0 Días** (360 horas) |
| **45 Ah (Plomo Auto)**| — | **270.0 Wh** | **12.5 Días** (300 horas) | **9.2 Días** (225 horas) | **7.0 Días** (168 horas) | **37.5 Días** (900 horas) |

> 🎯 **Objetivo de Diseño CIPRO Panamá:** Para cerros y torres remotas se debe dimensionar para un mínimo de **4 a 5 días de autonomía sin sol** (para soportar frentes de tormentas o temporales prolongados).

---

## 4. Dimensionamiento de Paneles Solares y Horas de Sol Pico (HSP)

### ¿Qué son las Horas de Sol Pico (HSP)?
El sol no brilla con la misma intensidad todo el día. Las **HSP** equivalen al número de horas al día en que la radiación solar tiene una intensidad estándar de $1000\,\text{W/m}^2$.

* **Panamá y Centroamérica (Promedio Anual):** **4.5 a 5.2 HSP** en temporada seca / despejada.
* **Días Lluviosos / Nublados (Peor caso invernal):** **2.0 a 2.5 HSP**.

### Fórmula de Generación Solar Diaria:
$$E_{\text{generada}} (\text{Wh/día}) = P_{\text{panel}} (\text{W}_p) \times \text{HSP} \times 0.75 \text{ (Factor de rendimiento y pérdidas)}$$

| Potencia Panel Solar ($W_p$) | Generación con Sol Óptimo (5.0 HSP) | Generación con Día Nublado (2.5 HSP) | Generación con Tormenta (1.5 HSP) | ¿Cubre el consumo de RPi Zero W? (21.6 Wh/día) |
| :---: | :---: | :---: | :---: | :---: |
| **10 W** | **37.5 Wh / día** | **18.7 Wh / día** | **11.2 Wh / día** | ⚠️ Justo en días de sol, déficit con lluvia |
| **20 W** *(Recomendado)* | **75.0 Wh / día** | **37.5 Wh / día** | **22.5 Wh / día** | 🟢 **Sí, 100% autosuficiente incluso con nubes** |
| **30 W** | **112.5 Wh / día** | **56.2 Wh / día** | **33.7 Wh / día** | 🟢 **Excelente margen de recarga rápida** |
| **50 W** | **187.5 Wh / día** | **93.7 Wh / día** | **56.2 Wh / día** | 🟢 **Ideal para RPi 3B+ / RPi 4B / Orange Pi** |

---

## 5. Cuadros de Referencia para el Armado de Nodos

Utilice estos tres kits pre-calculados como referencia según la ubicación y el propósito del despliegue:

### 📦 Kit 1: Nodo Autónomo Estándar (Recomendado para Cerros y Torres Inaccesibles)
*Ideal para cerros y zonas remotas donde se requiere mantenimiento CERO durante 5 a 10 años.*

```
 ┌─────────────────┐       ┌─────────────────┐       ┌────────────────────────┐
 │ Panel Solar 20W │──────>│ Controlador PWM │──────>│ Batería LiFePO4 12V 10Ah│
 └─────────────────┘       │   o MPPT 12V    │       └───────────┬────────────┘
                           └─────────────────┘                   │
                                                                 ▼
 ┌───────────────────────────┐      5.1V DC          ┌────────────────────────┐
 │ RPi Zero W + RNode LoRa   │<──────────────────────│ Sensor INA219 + StepDown│
 └───────────────────────────┘                       └────────────────────────┘
```

* **Microcomputadora:** Raspberry Pi Zero W (con Linux en OverlayFS Read-Only).
* **Radio LoRa:** ESP32 RNode (Heltec v2 / LilyGO T-Beam / DIY UART).
* **Sensores I2C:** INA219 (Corriente/Batería), BME280 (Clima), DS3231 (Reloj RTC).
* **Panel Solar:** **20W a 30W Monocristalino (18V Voc)**.
* **Batería:** **LiFePO4 12.8V 10Ah o 12Ah** (con BMS integrado).
* **Controlador de Carga:** Controlador Solar 10A con soporte LiFePO4.
* **Regulador SBC:** Step-Down DC-DC LM2596 o MP1584 ajustado a **5.15V**.
* **Autonomía sin sol:** **5.3 Días (128 horas continuas)**.
* **Tiempo de recarga completa:** **3.5 horas de sol pico**.

---

### 📦 Kit 2: Nodo Repetidor Ultra-Ligero (Micro-Solar de Mochila o Puesto Avanzado)
*Para despliegues rápidos de rescatistas en mochilas, árboles o campamentos temporales.*

* **Microcomputador:** ESP32 Standalone RNode (Firmware RNode puro, sin Linux).
* **Panel Solar:** **10W Plegable o Rígido**.
* **Batería:** **LiFePO4 12.8V 6Ah** (o 4 celdas 18650 en paralelo con BMS 1S/3S).
* **Autonomía sin sol:** **9.6 Días (230 horas continuas)**.
* **Tiempo de recarga completa:** **2.0 horas de sol pico**.

---

### 📦 Kit 3: Estación Base Comunitaria / Gateway Central
*Para albergues, puestos de comando de rescate o sedes comunitarias con tráfico elevado.*

* **Microcomputador:** Raspberry Pi 3B+ o Raspberry Pi 4B (4GB RAM).
* **Funciones:** NomadNet Hub + Propagation Node LXMF masivo + Wi-Fi Hotspot local.
* **Panel Solar:** **50W a 80W Monocristalino**.
* **Batería:** **LiFePO4 12.8V 20Ah a 30Ah** (o Batería AGM 12V 45Ah).
* **Autonomía sin sol:** **4.5 a 6.0 Días continuos**.
* **Tiempo de recarga completa:** **4.0 horas de sol pico**.

---

## 6. Recomendaciones Prácticas de Instalación Física

1. **Orientación e Inclinación del Panel Solar en Panamá:**
   - **Inclinación:** En Panamá (latitud ~8° a 9° N), incline el panel entre **10° y 15° hacia el SUR**.
   - Esta inclinación permite que la lluvia limpie automáticamente el polvo y el polen sin acumular agua.
2. **Ventilación y Protección contra Condensación:**
   - La caja estanca (gabinete IP66 / IP67) debe incluir una válvula de alivio respiradero de teflón (*Gore-Tex vent*) para evitar que la humedad tropical condense agua sobre la electrónica.
3. **Calibración del Step-Down DC-DC:**
   - Ajuste el potenciómetro del LM2596 con un multímetro a **5.15V exactos en vacío** antes de conectar la Raspberry Pi. Esto compensa la caída de tensión en los cables bajo carga de transmisión de radio.

---

## 🤝 Comunidad y Licencia
Este proyecto está liberado bajo la licencia MIT. Su uso es totalmente libre para fines experimentales, respuesta a emergencias y proyectos comunitarios solidarios.
Si este desarrollo te ha sido útil, te invitamos a mantener el reconocimiento y el enlace hacia el proyecto original.

### Contacto CIPRO Panamá
- 🌐 **Sitio Web:** [www.cipropanama.org](https://www.cipropanama.org/)
- ✉️ **Correo Electrónico:** [info@cipropanama.org](mailto:info@cipropanama.org)
- 🐙 **GitHub:** [github.com/cipropanama](https://github.com/cipropanama)

> **CIPRO Panamá** — _Tecnología para ayudar._  
> Desarrollado con ❤️ para las telecomunicaciones libres.
