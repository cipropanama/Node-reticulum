#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro del Diagrama de Conexionado Eléctrico Compacto y Elegante
CIPRO Panamá — Proyecto Reticulum Emergency Mesh Node
(https://www.cipropanama.org)
"""

import os
import subprocess
from PIL import Image

def generate_schematic():
    # Dimensiones elegantes: 1800 x 1120 px
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1120" width="1800" height="1120" style="background:#070d18; font-family:'Segoe UI', Inter, -apple-system, Roboto, Helvetica, sans-serif;">
  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#111927" stroke-width="0.7"/>
    </pattern>

    <!-- Component Shadows & Glows -->
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="wire-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.7"/>
    </filter>

    <!-- Gradients -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="rpi-pcb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#15803d"/>
      <stop offset="50%" stop-color="#166534"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>

    <linearGradient id="blue-pcb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1d4ed8"/>
      <stop offset="50%" stop-color="#1e40af"/>
      <stop offset="100%" stop-color="#1e3a8a"/>
    </linearGradient>

    <linearGradient id="purple-pcb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7e22ce"/>
      <stop offset="100%" stop-color="#581c87"/>
    </linearGradient>

    <linearGradient id="dark-pcb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="silver-metal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="40%" stop-color="#cbd5e1"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>

    <linearGradient id="gold-metal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="60%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#a16207"/>
    </linearGradient>

    <linearGradient id="terminal-green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16a34a"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>
  </defs>

  <!-- Background Base -->
  <rect width="1800" height="1120" fill="#070d18"/>
  <rect width="1800" height="1120" fill="url(#grid)"/>

  <!-- ==================== HEADER BANNER ==================== -->
  <g transform="translate(0, 0)">
    <rect width="1800" height="65" fill="url(#header-grad)" stroke="#334155" stroke-width="1"/>
    <rect x="0" y="63" width="1800" height="2" fill="#0284c7"/>
    
    <rect x="30" y="12" width="40" height="40" rx="6" fill="#0284c7"/>
    <text x="50" y="38" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle">⚡</text>
    
    <text x="85" y="33" font-size="17" font-weight="bold" fill="#f8fafc">GUÍA DE CONEXIONADO Y PINOUT REAL (NODO DE EMERGENCIA RETICULUM)</text>
    <text x="85" y="52" font-size="11" font-weight="500" fill="#94a3b8">RASPBERRY PI ZERO W + INA219 + BME280 + DS3231 RTC + RNODE LORA 915MHz</text>
    
    <rect x="1480" y="14" width="290" height="36" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <text x="1625" y="37" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">CIPRO Panamá — www.cipropanama.org</text>
  </g>

  <!-- ==================== 1. BATERÍA SOLAR 12V (TOP LEFT) ==================== -->
  <!-- Box: 200 x 135 at (140, 85) -->
  <g transform="translate(140, 85)" filter="url(#card-shadow)">
    <rect width="200" height="135" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
    <rect width="200" height="26" rx="8" fill="#0f172a"/>
    <text x="100" y="18" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">🔋 BATERÍA 12V</text>
    <text x="100" y="44" font-size="10" fill="#94a3b8" text-anchor="middle">LiFePO4 12.8V</text>

    <!-- Borne Negativo (-) -> Absolute X=195, Y=155 -->
    <circle cx="55" cy="70" r="14" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
    <text x="55" y="76" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="55" y="102" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">GND (Masa)</text>

    <!-- Borne Positivo (+) -> Absolute X=285, Y=155 -->
    <circle cx="145" cy="70" r="14" fill="#dc2626" stroke="#fecaca" stroke-width="2"/>
    <text x="145" y="76" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="145" y="102" font-size="9" font-weight="bold" fill="#f87171" text-anchor="middle">+12V (DC)</text>

    <text x="100" y="122" font-size="9" fill="#64748b" text-anchor="middle">Alimentación DC</text>
  </g>

  <!-- ==================== 2. SENSOR DE BATERÍA INA219 (TOP CENTER-LEFT) ==================== -->
  <!-- Box: 220 x 135 at (380, 85) -->
  <g transform="translate(380, 85)" filter="url(#card-shadow)">
    <rect width="220" height="135" rx="8" fill="url(#blue-pcb)" stroke="#3b82f6" stroke-width="1.5"/>
    <rect width="220" height="26" rx="8" fill="#1e3a8a"/>
    <text x="110" y="18" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">⚡ INA219 (Dir: 0x40)</text>

    <!-- Bornera Shunt (VIN+ / VIN-) -->
    <rect x="25" y="34" width="170" height="34" rx="4" fill="url(#terminal-green)" stroke="#22c55e" stroke-width="1"/>
    
    <!-- Tornillo VIN+ -> Absolute X=435, Y=136 -->
    <circle cx="55" cy="51" r="10" fill="#0f172a" stroke="url(#gold-metal)" stroke-width="1.5"/>
    <text x="55" y="55" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="55" y="80" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN+</text>

    <!-- Tornillo VIN- -> Absolute X=545, Y=136 -->
    <circle cx="165" cy="51" r="10" fill="#0f172a" stroke="url(#gold-metal)" stroke-width="1.5"/>
    <text x="165" y="55" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="165" y="80" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN-</text>

    <!-- Pines Header I2C Inferiores (VCC, GND, SCL, SDA) -> Y_rel=115 -> Absolute Y=200 -->
    <!-- VCC : Absolute X=415 -->
    <circle cx="35" cy="115" r="5.5" fill="#dc2626" stroke="#ffffff" stroke-width="1.2"/>
    <text x="35" y="103" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">VCC</text>

    <!-- GND : Absolute X=465 -->
    <circle cx="85" cy="115" r="5.5" fill="#0f172a" stroke="#ffffff" stroke-width="1.2"/>
    <text x="85" y="103" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=515 -->
    <circle cx="135" cy="115" r="5.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.2"/>
    <text x="135" y="103" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=565 -->
    <circle cx="185" cy="115" r="5.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.2"/>
    <text x="185" y="103" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>
  </g>

  <!-- ==================== 3. STEP-DOWN LM2596 (TOP CENTER-RIGHT) ==================== -->
  <!-- Box: 220 x 135 at (640, 85) -->
  <g transform="translate(640, 85)" filter="url(#card-shadow)">
    <rect width="220" height="135" rx="8" fill="url(#blue-pcb)" stroke="#1d4ed8" stroke-width="1.5"/>
    <rect width="220" height="26" rx="8" fill="#172554"/>
    <text x="110" y="18" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">🎛️ STEP-DOWN LM2596</text>

    <!-- Potenciómetro e Inductor -->
    <rect x="85" y="38" width="50" height="30" rx="3" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <circle cx="110" cy="53" r="6" fill="url(#gold-metal)"/>
    <rect x="85" y="75" width="50" height="45" rx="3" fill="#0f172a" stroke="#334155"/>
    <text x="110" y="101" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">330 uH</text>

    <!-- Terminales Entrada (Izquierda) -->
    <!-- IN- : Absolute X=660, Y=135 -->
    <circle cx="20" cy="50" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.2"/>
    <text x="34" y="54" font-size="8.5" font-weight="bold" fill="#ffffff">IN-</text>

    <!-- IN+ : Absolute X=660, Y=180 -->
    <circle cx="20" cy="95" r="7" fill="#dc2626" stroke="#ffffff" stroke-width="1.2"/>
    <text x="34" y="99" font-size="8.5" font-weight="bold" fill="#ffffff">IN+</text>

    <!-- Terminales Salida (Derecha) -->
    <!-- OUT- (GND) : Absolute X=840, Y=135 -->
    <circle cx="200" cy="50" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.2"/>
    <text x="186" y="54" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="end">OUT-</text>

    <!-- OUT+ (5.1V) : Absolute X=840, Y=180 -->
    <circle cx="200" cy="95" r="7" fill="#ea580c" stroke="#ffffff" stroke-width="1.2"/>
    <text x="186" y="99" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="end">5.1V</text>
  </g>

  <!-- ==================== 4. TARJETA RESUMEN DE FLUJO DE POTENCIA (TOP RIGHT) ==================== -->
  <!-- Box: 770 x 135 at (900, 85) -->
  <g transform="translate(900, 85)" filter="url(#card-shadow)">
    <rect width="770" height="135" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <rect width="770" height="26" rx="8" fill="#0f172a"/>
    <text x="385" y="18" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">💡 ARQUITECTURA DE POTENCIA Y PROTECCIÓN</text>
    
    <g transform="translate(20, 36)">
      <circle cx="8" cy="14" r="4.5" fill="#ef4444"/>
      <text x="20" y="17" font-size="10.5" font-weight="bold" fill="#f87171">12V Batería (+):</text>
      <text x="115" y="17" font-size="10.5" fill="#cbd5e1">Borne (+) ➔ VIN+ del INA219. Sale por VIN- ➔ IN+ del Step-Down.</text>

      <circle cx="8" cy="38" r="4.5" fill="#94a3b8"/>
      <text x="20" y="41" font-size="10.5" font-weight="bold" fill="#cbd5e1">Masa Común:</text>
      <text x="115" y="41" font-size="10.5" fill="#cbd5e1">Batería (-) ➔ IN- del Step-Down. GND unificado para Pi Zero, sensores y RNode.</text>

      <circle cx="8" cy="62" r="4.5" fill="#ea580c"/>
      <text x="20" y="65" font-size="10.5" font-weight="bold" fill="#fb923c">Salida 5.1V:</text>
      <text x="115" y="65" font-size="10.5" fill="#cbd5e1">OUT+ del Step-Down alimenta el Pin 2 (5V) de la Pi Zero y 5V del RNode.</text>

      <circle cx="8" cy="86" r="4.5" fill="#38bdf8"/>
      <text x="20" y="89" font-size="10.5" font-weight="bold" fill="#38bdf8">Sensor INA219:</text>
      <text x="115" y="89" font-size="10.5" fill="#cbd5e1">Mide voltaje de batería y corriente en tiempo real vía I2C (0x40).</text>
    </g>
  </g>

  <!-- ==================== 5. RASPBERRY PI ZERO W (MIDDLE LEFT) ==================== -->
  <!-- Box: 680 x 270 at (140, 270) -->
  <g transform="translate(140, 270)" filter="url(#card-shadow)">
    <!-- Base PCB -->
    <rect width="680" height="270" rx="14" fill="url(#rpi-pcb)" stroke="#22c55e" stroke-width="2"/>
    <circle cx="15" cy="15" r="7" fill="url(#gold-metal)"/>
    <circle cx="665" cy="15" r="7" fill="url(#gold-metal)"/>
    <circle cx="15" cy="255" r="7" fill="url(#gold-metal)"/>
    <circle cx="665" cy="255" r="7" fill="url(#gold-metal)"/>

    <!-- MicroSD y SoC -->
    <rect x="35" y="115" width="80" height="100" rx="5" fill="url(#silver-metal)" stroke="#475569"/>
    <text x="75" y="170" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">MicroSD</text>

    <!-- SoC BCM2835 -->
    <rect x="270" y="115" width="110" height="110" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
    <text x="325" y="165" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Broadcom</text>
    <text x="325" y="182" font-size="9.5" fill="#94a3b8" text-anchor="middle">BCM2835</text>

    <!-- WiFi / BT -->
    <rect x="490" y="130" width="55" height="55" rx="3" fill="url(#silver-metal)" stroke="#94a3b8"/>
    <text x="517" y="162" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">WiFi/BT</text>

    <text x="340" y="250" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">Raspberry Pi Zero W — Controlador Central Reticulum</text>

    <!-- ==================== HEADER GPIO 40 PINES ==================== -->
    <rect x="25" y="18" width="630" height="70" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    <text x="370" y="32" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">CABEZAL DE PINES GPIO</text>

    <!-- FILA SUPERIOR: PINES IMPARES (1, 3, 5, 7, 9...) -> Y_rel=46 -->
    <!-- PIN 1: 3.3V (X_rel=55 -> Absolute X=195, Y=316) -->
    <circle cx="55" cy="46" r="6" fill="#dc2626" stroke="#fecaca" stroke-width="1.5"/>
    <text x="55" y="60" font-size="8" font-weight="bold" fill="#f87171" text-anchor="middle">1 (3.3V)</text>

    <!-- PIN 3: GPIO 2 / SDA (X_rel=90 -> Absolute X=230, Y=316) -->
    <circle cx="90" cy="46" r="6" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
    <text x="90" y="60" font-size="8" font-weight="bold" fill="#38bdf8" text-anchor="middle">3 (SDA)</text>

    <!-- PIN 5: GPIO 3 / SCL (X_rel=125 -> Absolute X=265, Y=316) -->
    <circle cx="125" cy="46" r="6" fill="#16a34a" stroke="#bbf7d0" stroke-width="1.5"/>
    <text x="125" y="60" font-size="8" font-weight="bold" fill="#4ade80" text-anchor="middle">5 (SCL)</text>

    <!-- PIN 7 a 39 -->
    <g fill="#334155">
      <circle cx="160" cy="46" r="3.5"/><circle cx="195" cy="46" r="3.5"/><circle cx="230" cy="46" r="3.5"/>
      <circle cx="265" cy="46" r="3.5"/><circle cx="300" cy="46" r="3.5"/><circle cx="335" cy="46" r="3.5"/>
      <circle cx="370" cy="46" r="3.5"/><circle cx="405" cy="46" r="3.5"/><circle cx="440" cy="46" r="3.5"/>
      <circle cx="475" cy="46" r="3.5"/><circle cx="510" cy="46" r="3.5"/><circle cx="545" cy="46" r="3.5"/>
      <circle cx="580" cy="46" r="3.5"/><circle cx="615" cy="46" r="3.5"/>
    </g>

    <!-- FILA INFERIOR: PINES PARES (2, 4, 6, 8, 10...) -> Y_rel=70 -->
    <!-- PIN 2: 5V IN (X_rel=55 -> Absolute X=195, Y=340) -->
    <circle cx="55" cy="70" r="6" fill="#ea580c" stroke="#ffedd5" stroke-width="1.5"/>
    <text x="55" y="85" font-size="8" font-weight="bold" fill="#fb923c" text-anchor="middle">2 (5V)</text>

    <!-- PIN 4: 5V -->
    <circle cx="90" cy="70" r="3.5" fill="#334155"/>

    <!-- PIN 6: GND (X_rel=125 -> Absolute X=265, Y=340) -->
    <circle cx="125" cy="70" r="6" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="125" y="85" font-size="8" font-weight="bold" fill="#cbd5e1" text-anchor="middle">6 (GND)</text>

    <!-- PIN 8: GPIO 14 / TXD (X_rel=160 -> Absolute X=300, Y=340) -->
    <circle cx="160" cy="70" r="6" fill="#9333ea" stroke="#f3e8ff" stroke-width="1.5"/>
    <text x="160" y="85" font-size="8" font-weight="bold" fill="#c084fc" text-anchor="middle">8 (TX)</text>

    <!-- PIN 10: GPIO 15 / RXD (X_rel=195 -> Absolute X=335, Y=340) -->
    <circle cx="195" cy="70" r="6" fill="#eab308" stroke="#fef9c3" stroke-width="1.5"/>
    <text x="195" y="85" font-size="8" font-weight="bold" fill="#fde047" text-anchor="middle">10 (RX)</text>

    <!-- PIN 12 a 40 -->
    <g fill="#334155">
      <circle cx="230" cy="70" r="3.5"/><circle cx="265" cy="70" r="3.5"/><circle cx="300" cy="70" r="3.5"/>
      <circle cx="335" cy="70" r="3.5"/><circle cx="370" cy="70" r="3.5"/><circle cx="405" cy="70" r="3.5"/>
      <circle cx="440" cy="70" r="3.5"/><circle cx="475" cy="70" r="3.5"/><circle cx="510" cy="70" r="3.5"/>
      <circle cx="545" cy="70" r="3.5"/><circle cx="580" cy="70" r="3.5"/><circle cx="615" cy="70" r="3.5"/>
    </g>
  </g>

  <!-- ==================== 6. MÓDULO RNODE LORA ESP32 (MIDDLE RIGHT) ==================== -->
  <!-- Box: 770 x 270 at (900, 270) -->
  <g transform="translate(900, 270)" filter="url(#card-shadow)">
    <rect width="770" height="270" rx="14" fill="url(#dark-pcb)" stroke="#475569" stroke-width="2"/>
    <rect width="770" height="28" rx="14" fill="#0f172a"/>
    <text x="385" y="19" font-size="11.5" font-weight="bold" fill="#38bdf8" text-anchor="middle">📡 TRANSCEPTOR LORA RNODE (ESP32 / HELTEC / T-BEAM)</text>

    <!-- Pantalla OLED 0.96" -->
    <rect x="250" y="50" width="220" height="125" rx="6" fill="#020617" stroke="#38bdf8" stroke-width="1.5"/>
    <rect x="260" y="58" width="200" height="109" fill="#000000"/>
    <text x="360" y="82" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">RETICULUM RNODE</text>
    <text x="360" y="104" font-size="10" fill="#22c55e" text-anchor="middle">915.000 MHz (SF8 / BW 125)</text>
    <text x="360" y="124" font-size="10" fill="#f8fafc" text-anchor="middle">TX: 20 dBm | SNR: +8 dB</text>
    <text x="360" y="145" font-size="9" fill="#94a3b8" text-anchor="middle">CIPRO Rescue Mesh Node</text>

    <!-- Conector SMA y Antena -->
    <rect x="630" y="70" width="35" height="26" rx="2" fill="url(#gold-metal)" stroke="#a16207"/>
    <path d="M 665 83 L 720 83 L 720 35" stroke="#0f172a" stroke-width="6" fill="none"/>
    <rect x="712" y="-20" width="16" height="60" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    <text x="720" y="-28" font-size="9" font-weight="bold" fill="#38bdf8" text-anchor="middle">ANTENA</text>

    <!-- Pines UART + ALIMENTACIÓN (Lateral Izquierdo) -->
    <!-- 5V / VCC : Absolute X=935, Y=325 -->
    <circle cx="35" cy="55" r="6.5" fill="#ea580c" stroke="#ffffff" stroke-width="1.5"/>
    <text x="50" y="59" font-size="10" font-weight="bold" fill="#ffffff">5V / VCC</text>

    <!-- GND : Absolute X=935, Y=370 -->
    <circle cx="35" cy="100" r="6.5" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="50" y="104" font-size="10" font-weight="bold" fill="#ffffff">GND</text>

    <!-- RX : Absolute X=935, Y=415 -->
    <circle cx="35" cy="145" r="6.5" fill="#9333ea" stroke="#ffffff" stroke-width="1.5"/>
    <text x="50" y="149" font-size="10" font-weight="bold" fill="#ffffff">RX (a TX Pin 8)</text>

    <!-- TX : Absolute X=935, Y=460 -->
    <circle cx="35" cy="190" r="6.5" fill="#eab308" stroke="#ffffff" stroke-width="1.5"/>
    <text x="50" y="194" font-size="10" font-weight="bold" fill="#ffffff">TX (a RX Pin 10)</text>

    <text x="385" y="248" font-size="10" fill="#94a3b8" text-anchor="middle">Velocidad UART: 115200 Baudios (KISS Protocol / /dev/ttyAMA0)</text>
  </g>

  <!-- ==================== 7. RIEL DISTRIBUIDOR I2C (Y=580 a 645) ==================== -->
  <g transform="translate(140, 580)" filter="url(#card-shadow)">
    <rect width="1530" height="68" rx="7" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    
    <!-- Línea 1: 3.3V (VCC) - Rojo (Y_abs=595) -->
    <line x1="20" y1="15" x2="1510" y2="15" stroke="#dc2626" stroke-width="3.5"/>
    <rect x="680" y="7" width="140" height="15" rx="3" fill="#dc2626"/>
    <text x="750" y="18" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">3.3V VCC BUS (Pin 1)</text>

    <!-- Línea 2: GND (Masa) - Gris (Y_abs=610) -->
    <line x1="20" y1="30" x2="1510" y2="30" stroke="#64748b" stroke-width="3.5"/>
    <rect x="680" y="22" width="140" height="15" rx="3" fill="#1e293b" stroke="#64748b"/>
    <text x="750" y="33" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">GND MASA BUS (Pin 6)</text>

    <!-- Línea 3: SCL (Reloj) - Verde (Y_abs=625) -->
    <line x1="20" y1="45" x2="1510" y2="45" stroke="#16a34a" stroke-width="3.5"/>
    <rect x="680" y="37" width="140" height="15" rx="3" fill="#16a34a"/>
    <text x="750" y="48" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL RELOJ BUS (Pin 5)</text>

    <!-- Línea 4: SDA (Datos) - Azul (Y_abs=640) -->
    <line x1="20" y1="60" x2="1510" y2="60" stroke="#0284c7" stroke-width="3.5"/>
    <rect x="680" y="52" width="140" height="15" rx="3" fill="#0284c7"/>
    <text x="750" y="63" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA DATOS BUS (Pin 3)</text>

    <text x="1370" y="40" font-size="10.5" font-weight="bold" fill="#38bdf8">BUS I2C PARALELO DE 4 HILOS</text>
  </g>

  <!-- ==================== 8. SENSORES I2C INFERIORES: BME280 Y DS3231 RTC ==================== -->

  <!-- 8.1 SENSOR BME280 / BMP280 (BOTTOM LEFT) -->
  <!-- Box: 580 x 170 at (200, 680) -->
  <g transform="translate(200, 680)" filter="url(#card-shadow)">
    <rect width="580" height="170" rx="10" fill="url(#purple-pcb)" stroke="#9333ea" stroke-width="1.5"/>
    <rect width="580" height="26" rx="10" fill="#581c87"/>
    <text x="290" y="18" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">🌦️ SENSOR BME280 / BMP280 (Dirección: 0x76)</text>

    <!-- Pines Header I2C Superiores (VIN, GND, SCL, SDA) -> Y_rel=48 -> Absolute Y=728 -->
    <!-- VIN : Absolute X=300 -->
    <circle cx="100" cy="48" r="6" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
    <text x="100" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN (3.3V)</text>

    <!-- GND : Absolute X=395 -->
    <circle cx="195" cy="48" r="6" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="195" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=490 -->
    <circle cx="290" cy="48" r="6" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="290" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=585 -->
    <circle cx="385" cy="48" r="6" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="385" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>

    <!-- Sensor Metálico Bosch -->
    <rect x="265" y="90" width="50" height="36" rx="3" fill="url(#silver-metal)" stroke="#475569"/>
    <text x="290" y="112" font-size="9" font-weight="bold" fill="#0f172a" text-anchor="middle">BOSCH</text>
    <text x="290" y="150" font-size="9.5" fill="#f3e8ff" text-anchor="middle">Presión Atmosférica (hPa), Temp (°C), Humedad (%) — Alerta Tormentas</text>
  </g>

  <!-- 8.2 RELOJ DE TIEMPO REAL DS3231 RTC (BOTTOM RIGHT) -->
  <!-- Box: 580 x 170 at (980, 680) -->
  <g transform="translate(980, 680)" filter="url(#card-shadow)">
    <rect width="580" height="170" rx="10" fill="url(#blue-pcb)" stroke="#3b82f6" stroke-width="1.5"/>
    <rect width="580" height="26" rx="10" fill="#1e3a8a"/>
    <text x="290" y="18" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">🕒 RELOJ RTC DS3231 (Dirección: 0x68)</text>

    <!-- Pines Header I2C Superiores (VCC, GND, SCL, SDA) -> Y_rel=48 -> Absolute Y=728 -->
    <!-- VCC : Absolute X=1080 -->
    <circle cx="100" cy="48" r="6" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
    <text x="100" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">VCC (3.3V)</text>

    <!-- GND : Absolute X=1175 -->
    <circle cx="195" cy="48" r="6" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="195" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=1270 -->
    <circle cx="290" cy="48" r="6" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="290" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=1365 -->
    <circle cx="385" cy="48" r="6" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="385" y="68" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>

    <!-- Soporte Pila Botón CR2032 -->
    <circle cx="480" cy="115" r="28" fill="url(#silver-metal)" stroke="#64748b" stroke-width="2"/>
    <text x="480" y="113" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">CR2032</text>
    <text x="480" y="126" font-size="8" fill="#334155" text-anchor="middle">3V Litio</text>

    <text x="210" y="110" font-size="10" fill="#e0f2fe">Oscilador TCXO de Alta Precisión</text>
    <text x="210" y="128" font-size="9.5" fill="#93c5fd">Sincroniza hora offline en Reticulum</text>
  </g>

  <!-- ==================== 9. TABLA DE REFERENCIA RÁPIDA (FOOTER) ==================== -->
  <!-- Box: 1530 x 160 at (140, 885) -->
  <g transform="translate(140, 885)" filter="url(#card-shadow)">
    <rect width="1530" height="160" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    <rect width="1530" height="26" rx="8" fill="#1e293b"/>
    <text x="765" y="18" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">📋 TABLA DE REFERENCIA RÁPIDA DE CONEXIONADO Y PINES EXACTOS</text>

    <g transform="translate(25, 42)">
      <!-- Columna 1 -->
      <g transform="translate(0, 0)">
        <text x="0" y="14" font-size="10.5" font-weight="bold" fill="#38bdf8">📌 ALIMENTACIÓN Y VOLTAJE:</text>
        <text x="0" y="34" font-size="10.5" fill="#cbd5e1"><tspan fill="#f87171" font-weight="bold">12V Batería (+): </tspan>Va al borne VIN+ del INA219. Sale por VIN- hacia IN+ del Step-Down.</text>
        <text x="0" y="52" font-size="10.5" fill="#cbd5e1"><tspan fill="#fb923c" font-weight="bold">5.1V OUT+: </tspan>Conectado a Pin 2 de la Pi Zero y al Pin 5V/VCC del RNode LoRa.</text>
        <text x="0" y="70" font-size="10.5" fill="#cbd5e1"><tspan fill="#94a3b8" font-weight="bold">GND (Masa Común): </tspan>Conecta Batería (-), Step-Down IN-/OUT-, Pi Zero Pin 6 y RNode GND.</text>
        <text x="0" y="88" font-size="10.5" fill="#cbd5e1"><tspan fill="#f87171" font-weight="bold">3.3V Pi Zero Pin 1: </tspan>Alimenta exclusivamente la lógica de los 3 sensores I2C.</text>
      </g>

      <!-- Columna 2 -->
      <g transform="translate(530, 0)">
        <text x="0" y="14" font-size="10.5" font-weight="bold" fill="#38bdf8">🔌 UART SERIAL LORA (115200 BAUD):</text>
        <text x="0" y="34" font-size="10.5" fill="#cbd5e1"><tspan fill="#c084fc" font-weight="bold">Pi Zero Pin 8 (TXD / GPIO 14): </tspan>Conectado al Pin RX del RNode ESP32.</text>
        <text x="0" y="52" font-size="10.5" fill="#cbd5e1"><tspan fill="#fde047" font-weight="bold">Pi Zero Pin 10 (RXD / GPIO 15): </tspan>Conectado al Pin TX del RNode ESP32.</text>
        <text x="0" y="70" font-size="10.5" fill="#cbd5e1"><tspan fill="#38bdf8" font-weight="bold">Puerto Serial: </tspan>/dev/ttyAMA0 configurado en Reticulum rnsd.</text>
        <text x="0" y="88" font-size="10.5" fill="#4ade80"><tspan fill="#4ade80" font-weight="bold">Protocolo: </tspan>KISS Serial Framing de alta eficiencia para mallas LoRa.</text>
      </g>

      <!-- Columna 3 -->
      <g transform="translate(1060, 0)">
        <text x="0" y="14" font-size="10.5" font-weight="bold" fill="#38bdf8">🔍 BUS I2C COMPARTIDO (PARALELO):</text>
        <text x="0" y="34" font-size="10.5" fill="#cbd5e1"><tspan fill="#60a5fa" font-weight="bold">0x40 (INA219): </tspan>Voltaje, amperaje y estado de carga de la batería.</text>
        <text x="0" y="52" font-size="10.5" fill="#cbd5e1"><tspan fill="#c084fc" font-weight="bold">0x76 (BME280): </tspan>Presión atmosférica, temperatura y tormentas.</text>
        <text x="0" y="70" font-size="10.5" fill="#cbd5e1"><tspan fill="#38bdf8" font-weight="bold">0x68 (DS3231 RTC): </tspan>Reloj de precisión en tiempo real con pila CR2032.</text>
        <text x="0" y="88" font-size="10.5" fill="#4ade80">✓ Los 3 sensores comparten SDA (Pin 3) y SCL (Pin 5) sin conflicto.</text>
      </g>
    </g>
  </g>

  <!-- ==================== CABLEADO ULTRA-LIMPIO POR CALLEJONES ==================== -->
  <g filter="url(#wire-glow)">
    
    <!-- 1. POTENCIA 12V -->
    <!-- Batería (+) [X=285, Y=155] ➔ INA219 VIN+ [X=435, Y=136] -->
    <path d="M 285 155 L 355 155 L 355 136 L 435 136" fill="none" stroke="#ef4444" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="285" cy="155" r="3.5" fill="#ffffff"/>
    <circle cx="435" cy="136" r="3.5" fill="#ffffff"/>

    <!-- INA219 VIN- [X=545, Y=136] ➔ Step-Down IN+ [X=660, Y=180] -->
    <path d="M 545 136 L 615 136 L 615 180 L 660 180" fill="none" stroke="#f87171" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="545" cy="136" r="3.5" fill="#ffffff"/>
    <circle cx="660" cy="180" r="3.5" fill="#ffffff"/>

    <!-- Batería (-) [X=195, Y=155] ➔ Step-Down IN- [X=660, Y=135] (Canal superior Y=230) -->
    <path d="M 195 155 L 195 230 L 630 230 L 630 135 L 660 135" fill="none" stroke="#64748b" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="195" cy="155" r="3.5" fill="#ffffff"/>
    <circle cx="660" cy="135" r="3.5" fill="#ffffff"/>

    <!-- 2. SALIDA 5.1V REGULADA (LM2596 OUT+ / OUT-) -->
    <!-- Step-Down OUT+ (5.1V) [X=840, Y=180] ➔ Distribuidor [X=870, Y=255] -->
    <!-- Rama a Pi Zero Pin 2 [X=195, Y=340] -->
    <path d="M 840 180 L 870 180 L 870 255 L 195 255 L 195 340" fill="none" stroke="#ea580c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Rama a RNode 5V [X=935, Y=325] -->
    <path d="M 870 180 L 890 180 L 890 325 L 935 325" fill="none" stroke="#ea580c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="840" cy="180" r="3.5" fill="#ffffff"/>
    <circle cx="195" cy="340" r="3.5" fill="#ffffff"/>
    <circle cx="935" cy="325" r="3.5" fill="#ffffff"/>

    <!-- Step-Down OUT- (GND) [X=840, Y=135] ➔ Distribuidor [X=880, Y=245] -->
    <!-- Rama a Pi Zero Pin 6 [X=265, Y=340] -->
    <path d="M 840 135 L 880 135 L 880 245 L 265 245 L 265 340" fill="none" stroke="#94a3b8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Rama a RNode GND [X=935, Y=370] -->
    <path d="M 880 135 L 900 135 L 900 370 L 935 370" fill="none" stroke="#94a3b8" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="840" cy="135" r="3.5" fill="#ffffff"/>
    <circle cx="265" cy="340" r="3.5" fill="#ffffff"/>
    <circle cx="935" cy="370" r="3.5" fill="#ffffff"/>

    <!-- 3. UART SERIAL (Pines 8 y 10 ➔ RNode) (Canal Superior Y=250 y Y=260) -->
    <!-- Pi Zero Pin 8 (TXD) [X=300, Y=340] ➔ RNode RX [X=935, Y=415] -->
    <path d="M 300 340 L 300 250 L 860 250 L 860 415 L 935 415" fill="none" stroke="#9333ea" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="300" cy="340" r="3.5" fill="#ffffff"/>
    <circle cx="935" cy="415" r="3.5" fill="#ffffff"/>

    <!-- Pi Zero Pin 10 (RXD) [X=335, Y=340] ➔ RNode TX [X=935, Y=460] -->
    <path d="M 335 340 L 335 260 L 850 260 L 850 460 L 935 460" fill="none" stroke="#eab308" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="335" cy="340" r="3.5" fill="#ffffff"/>
    <circle cx="935" cy="460" r="3.5" fill="#ffffff"/>

    <!-- 4. I2C DESDE RASPBERRY PI ZERO AL RIEL (Por el callejón izquierdo X=50 a X=110) -->
    <!-- Pin 1 (3.3V) [X=195, Y=316] ➔ Riel 3.3V (Y=595) -->
    <path d="M 195 316 L 195 295 L 60 295 L 60 595 L 160 595" fill="none" stroke="#dc2626" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="195" cy="316" r="3.5" fill="#ffffff"/>
    <circle cx="160" cy="595" r="4" fill="#dc2626" stroke="#ffffff" stroke-width="1.2"/>

    <!-- Pin 6 (GND) [X=265, Y=340] ➔ Riel GND (Y=610) -->
    <path d="M 265 340 L 265 305 L 75 305 L 75 610 L 160 610" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="265" cy="340" r="3.5" fill="#ffffff"/>
    <circle cx="160" cy="610" r="4" fill="#64748b" stroke="#ffffff" stroke-width="1.2"/>

    <!-- Pin 5 (SCL) [X=265, Y=316] ➔ Riel SCL (Y=625) -->
    <path d="M 265 316 L 265 285 L 90 285 L 90 625 L 160 625" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="265" cy="316" r="3.5" fill="#ffffff"/>
    <circle cx="160" cy="625" r="4" fill="#16a34a" stroke="#ffffff" stroke-width="1.2"/>

    <!-- Pin 3 (SDA) [X=230, Y=316] ➔ Riel SDA (Y=640) -->
    <path d="M 230 316 L 230 275 L 105 275 L 105 640 L 160 640" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="230" cy="316" r="3.5" fill="#ffffff"/>
    <circle cx="160" cy="640" r="4" fill="#0284c7" stroke="#ffffff" stroke-width="1.2"/>

    <!-- 5. CONEXIÓN I2C DEL INA219 (Pasa por callejón izquierdo superior) -->
    <!-- INA219 VCC [X=415, Y=200] ➔ Riel 3.3V (Y=595) -->
    <path d="M 415 200 L 415 235 L 50 235 L 50 595 L 160 595" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="415" cy="200" r="3" fill="#ffffff"/>

    <!-- INA219 GND [X=465, Y=200] ➔ Riel GND (Y=610) -->
    <path d="M 465 200 L 465 240 L 65 240 L 65 610 L 160 610" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="465" cy="200" r="3" fill="#ffffff"/>

    <!-- INA219 SCL [X=515, Y=200] ➔ Riel SCL (Y=625) -->
    <path d="M 515 200 L 515 245 L 80 245 L 80 625 L 160 625" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="515" cy="200" r="3" fill="#ffffff"/>

    <!-- INA219 SDA [X=565, Y=200] ➔ Riel SDA (Y=640) -->
    <path d="M 565 200 L 565 250 L 95 250 L 95 640 L 160 640" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="565" cy="200" r="3" fill="#ffffff"/>

    <!-- 6. DERIVACIONES DE SENSORES INFERIORES AL RIEL I2C (100% Verticales Rectas) -->
    <!-- SENSOR BME280 -->
    <!-- VIN [X=300, Y=728] ➔ Riel 3.3V (Y=595) -->
    <line x1="300" y1="728" x2="300" y2="595" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/>
    <circle cx="300" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="300" cy="595" r="4" fill="#dc2626" stroke="#ffffff" stroke-width="1.2"/>

    <!-- GND [X=395, Y=728] ➔ Riel GND (Y=610) -->
    <line x1="395" y1="728" x2="395" y2="610" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
    <circle cx="395" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="395" cy="610" r="4" fill="#64748b" stroke="#ffffff" stroke-width="1.2"/>

    <!-- SCL [X=490, Y=728] ➔ Riel SCL (Y=625) -->
    <line x1="490" y1="728" x2="490" y2="625" stroke="#16a34a" stroke-width="3" stroke-linecap="round"/>
    <circle cx="490" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="490" cy="625" r="4" fill="#16a34a" stroke="#ffffff" stroke-width="1.2"/>

    <!-- SDA [X=585, Y=728] ➔ Riel SDA (Y=640) -->
    <line x1="585" y1="728" x2="585" y2="640" stroke="#0284c7" stroke-width="3" stroke-linecap="round"/>
    <circle cx="585" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="585" cy="640" r="4" fill="#0284c7" stroke="#ffffff" stroke-width="1.2"/>

    <!-- SENSOR DS3231 RTC -->
    <!-- VCC [X=1080, Y=728] ➔ Riel 3.3V (Y=595) -->
    <line x1="1080" y1="728" x2="1080" y2="595" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/>
    <circle cx="1080" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="1080" cy="595" r="4" fill="#dc2626" stroke="#ffffff" stroke-width="1.2"/>

    <!-- GND [X=1175, Y=728] ➔ Riel GND (Y=610) -->
    <line x1="1175" y1="728" x2="1175" y2="610" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
    <circle cx="1175" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="1175" cy="610" r="4" fill="#64748b" stroke="#ffffff" stroke-width="1.2"/>

    <!-- SCL [X=1270, Y=728] ➔ Riel SCL (Y=625) -->
    <line x1="1270" y1="728" x2="1270" y2="625" stroke="#16a34a" stroke-width="3" stroke-linecap="round"/>
    <circle cx="1270" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="1270" cy="625" r="4" fill="#16a34a" stroke="#ffffff" stroke-width="1.2"/>

    <!-- SDA [X=1365, Y=728] ➔ Riel SDA (Y=640) -->
    <line x1="1365" y1="728" x2="1365" y2="640" stroke="#0284c7" stroke-width="3" stroke-linecap="round"/>
    <circle cx="1365" cy="728" r="3.5" fill="#ffffff"/>
    <circle cx="1365" cy="640" r="4" fill="#0284c7" stroke="#ffffff" stroke-width="1.2"/>

  </g>

</svg>
"""

    svg_file = "/tmp/fritzing_exact.svg"
    png_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/esquema_conexion_rpi_zero_i2c.png"
    jpg_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/esquema_conexion_rpi_zero_i2c.jpg"
    ina_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/ina219_wiring.jpg"
    i2c_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/i2c_sensors_wiring.jpg"

    os.makedirs("/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img", exist_ok=True)

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print("Renderizando esquema compacto con Chromium headless (1800x1120)...")
    subprocess.run([
        "chromium", "--headless", "--disable-gpu",
        f"--screenshot={png_file}",
        "--window-size=1800,1120",
        svg_file
    ], check=True)

    print("Guardando copias JPEG ultra-nítidas...")
    im = Image.open(png_file).convert("RGB")
    im.save(jpg_file, "JPEG", quality=98)
    im.save(ina_file, "JPEG", quality=98)
    im.save(i2c_file, "JPEG", quality=98)

    print(f"✓ Generado exitosamente: {jpg_file}")

if __name__ == "__main__":
    generate_schematic()
