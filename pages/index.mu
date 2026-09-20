# == PANEL DE CONTROL - NODO DE EMERGENCIA RETICULUM ==
`!C`_Red de Comunicaciones de Emergencia y Resiliencia Comunitaria_`!c`
`!C`*CIPRO Panamá — Tecnología para ayudar (www.cipropanama.org)*`!c`

================================================================================

`!F03a`### 📡 ESTADO GENERAL DEL NODO`!f`
- *Nombre del Nodo:* `{NODE_NAME}`  |  *Zona:* `{NODE_LOCATION}`
- *Descripción:* `{NODE_DESCRIPTION}`
- *Modo de Operación:* `{NODE_MODE}`
- *ID Reticulum:* `{NODE_IDENTITY}`
- *Servicio LXMF:* `{LXMF_STATUS}`

--------------------------------------------------------------------------------

`!Fe62`### 🔋 ENERGÍA Y BATERÍA SOLAR (INA219)`!f`
- *Voltaje y Nivel:* `{BATTERY_VOLT}`  `{BATTERY_BAR}`
- *Flujo de Corriente:* `{BATTERY_CURRENT}`  |  *Potencia:* `{BATTERY_POWER}`
- *Tendencia Voltaje (24h):* ` {BATTERY_SPARKLINE} `

--------------------------------------------------------------------------------

`!F28b`### ⛅ ESTACIÓN METEOROLÓGICA AMBIENTAL (BME280)`!f`
- *Temperatura:* `{ENV_TEMP}`  |  *Humedad Relativa:* `{ENV_HUMIDITY}`
- *Presión Barométrica:* `{ENV_PRESSURE}`  (`{ENV_WEATHER}`)
- *Tendencia Barométrica:* ` {ENV_SPARKLINE} `

--------------------------------------------------------------------------------

`!F197`### 📻 ENLACE DE RADIO LoRa Y MALLA RETICULUM`!f`
- *Frecuencia LoRa:* `{LORA_FREQ}` MHz  |  *BW:* `{LORA_BW}` kHz  |  *SF:* `{LORA_SF}`
- *Interfaces Activas:* `{ACTIVE_INTERFACES}`

--------------------------------------------------------------------------------

`!F2a5`### 💻 SALUD Y RENDIMIENTO DEL SISTEMA`!f`
- *SBC:* `{SBC_MODEL}` (`{SBC_ARCH}`)
- *CPU Temp:* `{CPU_TEMP}` ` {CPU_SPARKLINE} `  |  *Carga:* `{LOAD_AVG}`
- *Memoria RAM:* `{RAM_BAR}` ({RAM_USED} / {RAM_TOTAL})
- *Tiempo Activo (Uptime):* `{UPTIME}`
- *Última Telemetría:* `{LAST_TELEMETRY_UPDATE}`

================================================================================

`!F03a`### 🤖 COMANDOS RÁPIDOS BOT LXMF`!f`
_Envía un mensaje LXMF a la identidad de este nodo con cualquiera de estas palabras:_
- `status`  → Resumen completo e instantáneo de telemetría
- `bat`     → Estado detallado de batería, corriente y consumo solar
- `env`     → Reporte ambiental (temperatura, humedad, presión)
- `net`     → Interfaces de red activas y frecuencia de radio
- `ping`    → Prueba de cobertura y eco de enlace

--------------------------------------------------------------------------------

`[📨 Buzón de Almacenamiento y Reenvío LXMF]`(emergency.mu)  |  `[ℹ️ Acerca de CIPRO Panamá]`(about.mu)  |  `[🔄 Actualizar Dashboard]`(index.mu)

`!C`_CIPRO Panamá - Desarrollado con ❤️ para las telecomunicaciones libres._`!c`
