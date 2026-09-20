#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro del Diagrama de Conexionado Eléctrico Oficial
Diseño Profesional Pulido — CIPRO Panamá
(https://www.cipropanama.org)
"""

import os
import subprocess
from PIL import Image

def generate_schematic():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1350" width="1800" height="1350" style="background:#080e1a; font-family:'Segoe UI', Inter, -apple-system, Roboto, Helvetica, sans-serif;">
  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#131c2e" stroke-width="0.8"/>
    </pattern>

    <!-- Component Shadows & Glows -->
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="wire-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.7"/>
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
  <rect width="1800" height="1350" fill="#080e1a"/>
  <rect width="1800" height="1350" fill="url(#grid)"/>

  <!-- ==================== HEADER BANNER ==================== -->
  <g transform="translate(0, 0)">
    <rect width="1800" height="75" fill="url(#header-grad)" stroke="#334155" stroke-width="1"/>
    <rect x="0" y="73" width="1800" height="2" fill="#0284c7"/>
    
    <rect x="30" y="15" width="45" height="45" rx="8" fill="#0284c7"/>
    <text x="52" y="44" font-size="22" font-weight="900" fill="#ffffff" text-anchor="middle">⚡</text>
    
    <text x="90" y="36" font-size="19" font-weight="bold" fill="#f8fafc">GUÍA MAESTRA DE CONEXIONADO Y PINOUT REAL (DIAGRAMA FRITZING OFICIAL)</text>
    <text x="90" y="58" font-size="12" font-weight="500" fill="#94a3b8">NODO RETICULUM / NOMADNET — RASPBERRY PI ZERO W + INA219 + BME280 + DS3231 RTC + RNODE LORA</text>
    
    <rect x="1460" y="17" width="310" height="40" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <text x="1615" y="42" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">CIPRO Panamá — www.cipropanama.org</text>
  </g>

  <!-- ==================== 1. BATERÍA SOLAR 12V (TOP LEFT) ==================== -->
  <g transform="translate(100, 100)" filter="url(#card-shadow)">
    <rect width="230" height="175" rx="10" fill="#1e293b" stroke="#475569" stroke-width="2"/>
    <rect width="230" height="32" rx="10" fill="#0f172a"/>
    <text x="115" y="22" font-size="12" font-weight="bold" fill="#f8fafc" text-anchor="middle">🔋 BATERÍA SOLAR 12V</text>
    <text x="115" y="54" font-size="11" fill="#94a3b8" text-anchor="middle">LiFePO4 / AGM 12.8V DC</text>

    <!-- Borne Negativo (-) -> Absolute X=165, Y=190 -->
    <circle cx="65" cy="90" r="17" fill="#0f172a" stroke="#cbd5e1" stroke-width="2.5"/>
    <text x="65" y="97" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="65" y="126" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">GND (Masa)</text>

    <!-- Borne Positivo (+) -> Absolute X=265, Y=190 -->
    <circle cx="165" cy="90" r="17" fill="#dc2626" stroke="#fecaca" stroke-width="2.5"/>
    <text x="165" y="97" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="165" y="126" font-size="10" font-weight="bold" fill="#f87171" text-anchor="middle">+12V DC</text>

    <text x="115" y="155" font-size="10" fill="#64748b" text-anchor="middle">Fuente de Energía Principal</text>
  </g>

  <!-- ==================== 2. SENSOR DE BATERÍA INA219 (TOP CENTER-LEFT) ==================== -->
  <g transform="translate(370, 100)" filter="url(#card-shadow)">
    <rect width="260" height="175" rx="10" fill="url(#blue-pcb)" stroke="#3b82f6" stroke-width="2"/>
    <rect width="260" height="32" rx="10" fill="#1e3a8a"/>
    <text x="130" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">⚡ SENSOR INA219 (Dir: 0x40)</text>

    <!-- Bornera Shunt Superior (VIN+ / VIN-) -->
    <rect x="25" y="42" width="210" height="44" rx="6" fill="url(#terminal-green)" stroke="#22c55e" stroke-width="1.5"/>
    
    <!-- Tornillo VIN+ -> Absolute X=440, Y=164 -->
    <circle cx="70" cy="64" r="12" fill="#0f172a" stroke="url(#gold-metal)" stroke-width="2"/>
    <text x="70" y="68" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="70" y="102" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN+ (Entrada)</text>

    <!-- Tornillo VIN- -> Absolute X=560, Y=164 -->
    <circle cx="190" cy="64" r="12" fill="#0f172a" stroke="url(#gold-metal)" stroke-width="2"/>
    <text x="190" y="68" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="190" y="102" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN- (Salida)</text>

    <!-- Pines Header I2C Inferiores (VCC, GND, SCL, SDA) -> Y_rel=148 -> Absolute Y=248 -->
    <!-- VCC : Absolute X=415 -->
    <circle cx="45" cy="148" r="6.5" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
    <text x="45" y="132" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">VCC</text>

    <!-- GND : Absolute X=470 -->
    <circle cx="100" cy="148" r="6.5" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="100" y="132" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=530 -->
    <circle cx="160" cy="148" r="6.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="160" y="132" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=585 -->
    <circle cx="215" cy="148" r="6.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="215" y="132" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>
  </g>

  <!-- ==================== 3. STEP-DOWN LM2596 (TOP CENTER-RIGHT) ==================== -->
  <g transform="translate(670, 100)" filter="url(#card-shadow)">
    <rect width="260" height="175" rx="10" fill="url(#blue-pcb)" stroke="#1d4ed8" stroke-width="2"/>
    <rect width="260" height="32" rx="10" fill="#172554"/>
    <text x="130" y="22" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">🎛️ STEP-DOWN LM2596 (5.1V)</text>

    <!-- Potenciómetro e Inductor -->
    <rect x="100" y="48" width="60" height="38" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <circle cx="130" cy="67" r="7" fill="url(#gold-metal)"/>
    <rect x="100" y="96" width="60" height="56" rx="4" fill="#0f172a" stroke="#334155"/>
    <text x="130" y="130" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">330 uH</text>

    <!-- Terminales Entrada (Izquierda) -->
    <!-- IN- : Absolute X=695, Y=164 -->
    <circle cx="25" cy="64" r="8" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="42" y="68" font-size="10" font-weight="bold" fill="#ffffff">IN - (GND)</text>

    <!-- IN+ : Absolute X=695, Y=220 -->
    <circle cx="25" cy="120" r="8" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
    <text x="42" y="124" font-size="10" font-weight="bold" fill="#ffffff">IN + (+12V)</text>

    <!-- Terminales Salida (Derecha) -->
    <!-- OUT- (GND) : Absolute X=905, Y=164 -->
    <circle cx="235" cy="64" r="8" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="218" y="68" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="end">OUT - (GND)</text>

    <!-- OUT+ (5.1V) : Absolute X=905, Y=220 -->
    <circle cx="235" cy="120" r="8" fill="#ea580c" stroke="#ffffff" stroke-width="1.5"/>
    <text x="218" y="124" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="end">OUT + (5.1V)</text>
  </g>

  <!-- ==================== 4. TARJETA RESUMEN DE FLUJO DE POTENCIA (TOP RIGHT) ==================== -->
  <g transform="translate(970, 100)" filter="url(#card-shadow)">
    <rect width="730" height="175" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <rect width="730" height="32" rx="10" fill="#0f172a"/>
    <text x="365" y="22" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">💡 ARQUITECTURA DE ALIMENTACIÓN Y MEDICIÓN EN ALTA (HIGH-SIDE)</text>
    
    <g transform="translate(25, 46)">
      <circle cx="10" cy="15" r="5" fill="#ef4444"/>
      <text x="25" y="19" font-size="12" font-weight="bold" fill="#f87171">Línea 12V (+):</text>
      <text x="120" y="19" font-size="12" fill="#cbd5e1">Batería (+) ➔ Borne VIN+ del INA219. Sale por VIN- ➔ Entrada IN+ del Step-Down.</text>

      <circle cx="10" cy="45" r="5" fill="#94a3b8"/>
      <text x="25" y="49" font-size="12" font-weight="bold" fill="#cbd5e1">Línea Masa:</text>
      <text x="120" y="49" font-size="12" fill="#cbd5e1">Batería (-) ➔ Entrada IN- del Step-Down. GND común unificado para todo el sistema.</text>

      <circle cx="10" cy="75" r="5" fill="#ea580c"/>
      <text x="25" y="79" font-size="12" font-weight="bold" fill="#fb923c">Línea 5.1V:</text>
      <text x="120" y="79" font-size="12" fill="#cbd5e1">OUT+ del Step-Down alimenta el Pin 2 (5V) de la Pi Zero y el pin 5V del RNode.</text>

      <circle cx="10" cy="105" r="5" fill="#38bdf8"/>
      <text x="25" y="109" font-size="12" font-weight="bold" fill="#38bdf8">Sensor INA219:</text>
      <text x="120" y="109" font-size="12" fill="#cbd5e1">Mide voltaje de batería y amperaje consumido en tiempo real vía I2C (0x40).</text>
    </g>
  </g>

  <!-- ==================== 5. RASPBERRY PI ZERO W (MIDDLE LEFT) ==================== -->
  <g transform="translate(100, 390)" filter="url(#card-shadow)">
    <!-- Base PCB -->
    <rect width="820" height="340" rx="16" fill="url(#rpi-pcb)" stroke="#22c55e" stroke-width="2"/>
    <circle cx="18" cy="18" r="9" fill="url(#gold-metal)"/>
    <circle cx="802" cy="18" r="9" fill="url(#gold-metal)"/>
    <circle cx="18" cy="322" r="9" fill="url(#gold-metal)"/>
    <circle cx="802" cy="322" r="9" fill="url(#gold-metal)"/>

    <!-- MicroSD y SoC -->
    <rect x="40" y="145" width="100" height="130" rx="6" fill="url(#silver-metal)" stroke="#475569"/>
    <text x="90" y="215" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">MicroSD</text>

    <!-- SoC BCM2835 -->
    <rect x="330" y="145" width="135" height="135" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
    <text x="397" y="208" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">Broadcom</text>
    <text x="397" y="228" font-size="11" fill="#94a3b8" text-anchor="middle">BCM2835 (ARM)</text>

    <!-- WiFi / BT -->
    <rect x="580" y="160" width="70" height="70" rx="4" fill="url(#silver-metal)" stroke="#94a3b8"/>
    <text x="615" y="200" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">WiFi/BT</text>

    <text x="410" y="315" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">Raspberry Pi Zero W — Controlador Central del Nodo Reticulum</text>

    <!-- ==================== HEADER GPIO 40 PINES ==================== -->
    <rect x="30" y="22" width="760" height="85" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <text x="450" y="38" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">CABEZAL DE PINES GPIO (40 PINES)</text>

    <!-- FILA SUPERIOR: PINES IMPARES (1, 3, 5, 7, 9...) -> Y_rel=56 -->
    <!-- PIN 1: 3.3V (X_rel=65 -> Absolute X=165, Y=446) -->
    <circle cx="65" cy="56" r="7.5" fill="#dc2626" stroke="#fecaca" stroke-width="2"/>
    <text x="65" y="72" font-size="9" font-weight="bold" fill="#f87171" text-anchor="middle">1 (3.3V)</text>

    <!-- PIN 3: GPIO 2 / SDA (X_rel=105 -> Absolute X=205, Y=446) -->
    <circle cx="105" cy="56" r="7.5" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/>
    <text x="105" y="72" font-size="9" font-weight="bold" fill="#38bdf8" text-anchor="middle">3 (SDA)</text>

    <!-- PIN 5: GPIO 3 / SCL (X_rel=145 -> Absolute X=245, Y=446) -->
    <circle cx="145" cy="56" r="7.5" fill="#16a34a" stroke="#bbf7d0" stroke-width="2"/>
    <text x="145" y="72" font-size="9" font-weight="bold" fill="#4ade80" text-anchor="middle">5 (SCL)</text>

    <!-- PIN 7 a 39 -->
    <g fill="#334155">
      <circle cx="185" cy="56" r="4.5"/><circle cx="225" cy="56" r="4.5"/><circle cx="265" cy="56" r="4.5"/>
      <circle cx="305" cy="56" r="4.5"/><circle cx="345" cy="56" r="4.5"/><circle cx="385" cy="56" r="4.5"/>
      <circle cx="425" cy="56" r="4.5"/><circle cx="465" cy="56" r="4.5"/><circle cx="505" cy="56" r="4.5"/>
      <circle cx="545" cy="56" r="4.5"/><circle cx="585" cy="56" r="4.5"/><circle cx="625" cy="56" r="4.5"/>
      <circle cx="665" cy="56" r="4.5"/><circle cx="705" cy="56" r="4.5"/><circle cx="745" cy="56" r="4.5"/>
    </g>

    <!-- FILA INFERIOR: PINES PARES (2, 4, 6, 8, 10...) -> Y_rel=84 -->
    <!-- PIN 2: 5V IN (X_rel=65 -> Absolute X=165, Y=474) -->
    <circle cx="65" cy="84" r="7.5" fill="#ea580c" stroke="#ffedd5" stroke-width="2"/>
    <text x="65" y="103" font-size="9" font-weight="bold" fill="#fb923c" text-anchor="middle">2 (5V)</text>

    <!-- PIN 4: 5V -->
    <circle cx="105" cy="84" r="4.5" fill="#334155"/>

    <!-- PIN 6: GND (X_rel=145 -> Absolute X=245, Y=474) -->
    <circle cx="145" cy="84" r="7.5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <text x="145" y="103" font-size="9" font-weight="bold" fill="#cbd5e1" text-anchor="middle">6 (GND)</text>

    <!-- PIN 8: GPIO 14 / TXD (X_rel=185 -> Absolute X=285, Y=474) -->
    <circle cx="185" cy="84" r="7.5" fill="#9333ea" stroke="#f3e8ff" stroke-width="2"/>
    <text x="185" y="103" font-size="9" font-weight="bold" fill="#c084fc" text-anchor="middle">8 (TX)</text>

    <!-- PIN 10: GPIO 15 / RXD (X_rel=225 -> Absolute X=325, Y=474) -->
    <circle cx="225" cy="84" r="7.5" fill="#eab308" stroke="#fef9c3" stroke-width="2"/>
    <text x="225" y="103" font-size="9" font-weight="bold" fill="#fde047" text-anchor="middle">10 (RX)</text>

    <!-- PIN 12 a 40 -->
    <g fill="#334155">
      <circle cx="265" cy="84" r="4.5"/><circle cx="305" cy="84" r="4.5"/><circle cx="345" cy="84" r="4.5"/>
      <circle cx="385" cy="84" r="4.5"/><circle cx="425" cy="84" r="4.5"/><circle cx="465" cy="84" r="4.5"/>
      <circle cx="505" cy="84" r="4.5"/><circle cx="545" cy="84" r="4.5"/><circle cx="585" cy="84" r="4.5"/>
      <circle cx="625" cy="84" r="4.5"/><circle cx="665" cy="84" r="4.5"/><circle cx="705" cy="84" r="4.5"/>
      <circle cx="745" cy="84" r="4.5"/>
    </g>
  </g>

  <!-- ==================== 6. MÓDULO RNODE LORA ESP32 (MIDDLE RIGHT) ==================== -->
  <g transform="translate(970, 390)" filter="url(#card-shadow)">
    <rect width="730" height="340" rx="16" fill="url(#dark-pcb)" stroke="#475569" stroke-width="2"/>
    <rect width="730" height="34" rx="16" fill="#0f172a"/>
    <text x="365" y="23" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">📡 TRANSCEPTOR LORA RNODE (ESP32 / HELTEC LORA32 / T-BEAM)</text>

    <!-- Pantalla OLED 0.96" -->
    <rect x="230" y="65" width="270" height="150" rx="8" fill="#020617" stroke="#38bdf8" stroke-width="2"/>
    <rect x="245" y="75" width="240" height="130" fill="#000000"/>
    <text x="365" y="105" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">RETICULUM RNODE</text>
    <text x="365" y="132" font-size="12" fill="#22c55e" text-anchor="middle">Frec: 915.000 MHz (SF8 / BW 125)</text>
    <text x="365" y="155" font-size="12" fill="#f8fafc" text-anchor="middle">TX: 20 dBm | SNR: +8 dB</text>
    <text x="365" y="180" font-size="11" fill="#94a3b8" text-anchor="middle">CIPRO Emergency Mesh Node</text>

    <!-- Conector SMA y Antena -->
    <rect x="590" y="90" width="45" height="35" rx="3" fill="url(#gold-metal)" stroke="#a16207"/>
    <path d="M 635 107 L 695 107 L 695 45" stroke="#0f172a" stroke-width="8" fill="none"/>
    <rect x="685" y="-30" width="20" height="80" rx="5" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <text x="695" y="-40" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">ANTENA 915MHz</text>

    <!-- Pines UART + ALIMENTACIÓN (Lateral Izquierdo) -->
    <!-- 5V / VCC : Absolute X=1010, Y=460 -->
    <circle cx="40" cy="70" r="8" fill="#ea580c" stroke="#ffffff" stroke-width="2"/>
    <text x="60" y="75" font-size="12" font-weight="bold" fill="#ffffff">5V / VCC (Alimentación)</text>

    <!-- GND : Absolute X=1010, Y=515 -->
    <circle cx="40" cy="125" r="8" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <text x="60" y="130" font-size="12" font-weight="bold" fill="#ffffff">GND (Masa Común)</text>

    <!-- RX : Absolute X=1010, Y=570 -->
    <circle cx="40" cy="180" r="8" fill="#9333ea" stroke="#ffffff" stroke-width="2"/>
    <text x="60" y="185" font-size="12" font-weight="bold" fill="#ffffff">RX (Recibe de TX Pin 8 de la Pi)</text>

    <!-- TX : Absolute X=1010, Y=625 -->
    <circle cx="40" cy="235" r="8" fill="#eab308" stroke="#ffffff" stroke-width="2"/>
    <text x="60" y="240" font-size="12" font-weight="bold" fill="#ffffff">TX (Envía a RX Pin 10 de la Pi)</text>

    <text x="365" y="315" font-size="12" fill="#94a3b8" text-anchor="middle">Velocidad UART: 115200 Baudios (KISS Protocol / /dev/ttyAMA0)</text>
  </g>

  <!-- ==================== 7. RIEL DISTRIBUIDOR I2C (Y=765 a 850) ==================== -->
  <g transform="translate(100, 765)" filter="url(#card-shadow)">
    <rect width="1600" height="85" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    
    <!-- Línea 1: 3.3V (VCC) - Rojo (Y_abs=785) -->
    <line x1="25" y1="20" x2="1575" y2="20" stroke="#dc2626" stroke-width="4"/>
    <rect x="700" y="10" width="160" height="19" rx="4" fill="#dc2626"/>
    <text x="780" y="23" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">3.3V VCC BUS (Pin 1)</text>

    <!-- Línea 2: GND (Masa) - Gris (Y_abs=805) -->
    <line x1="25" y1="40" x2="1575" y2="40" stroke="#64748b" stroke-width="4"/>
    <rect x="700" y="30" width="160" height="19" rx="4" fill="#1e293b" stroke="#64748b"/>
    <text x="780" y="43" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">GND MASA BUS (Pin 6)</text>

    <!-- Línea 3: SCL (Reloj) - Verde (Y_abs=825) -->
    <line x1="25" y1="60" x2="1575" y2="60" stroke="#16a34a" stroke-width="4"/>
    <rect x="700" y="50" width="160" height="19" rx="4" fill="#16a34a"/>
    <text x="780" y="63" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL RELOJ BUS (Pin 5)</text>

    <!-- Línea 4: SDA (Datos) - Azul (Y_abs=845) -->
    <line x1="25" y1="80" x2="1575" y2="80" stroke="#0284c7" stroke-width="4"/>
    <rect x="700" y="70" width="160" height="19" rx="4" fill="#0284c7"/>
    <text x="780" y="83" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA DATOS BUS (Pin 3)</text>

    <text x="1420" y="48" font-size="12" font-weight="bold" fill="#38bdf8">BUS I2C PARALELO DE 4 HILOS (I2C-1)</text>
  </g>

  <!-- ==================== 8. SENSORES I2C INFERIORES: BME280 Y DS3231 RTC ==================== -->

  <!-- 8.1 SENSOR BME280 / BMP280 (BOTTOM LEFT) -->
  <g transform="translate(150, 885)" filter="url(#card-shadow)">
    <rect width="650" height="210" rx="12" fill="url(#purple-pcb)" stroke="#9333ea" stroke-width="2"/>
    <rect width="650" height="32" rx="12" fill="#581c87"/>
    <text x="325" y="22" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🌦️ SENSOR BME280 / BMP280 (Dirección I2C: 0x76)</text>

    <!-- Pines Header I2C Superiores (VIN, GND, SCL, SDA) -> Y_rel=60 -> Absolute Y=945 -->
    <!-- VIN : Absolute X=260 -->
    <circle cx="110" cy="60" r="7.5" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>
    <text x="110" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">VIN (3.3V)</text>

    <!-- GND : Absolute X=370 -->
    <circle cx="220" cy="60" r="7.5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <text x="220" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=480 -->
    <circle cx="330" cy="60" r="7.5" fill="#16a34a" stroke="#ffffff" stroke-width="2"/>
    <text x="330" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=590 -->
    <circle cx="440" cy="60" r="7.5" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
    <text x="440" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>

    <!-- Sensor Metálico Bosch -->
    <rect x="295" y="115" width="60" height="45" rx="4" fill="url(#silver-metal)" stroke="#475569"/>
    <text x="325" y="142" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">BOSCH</text>
    <text x="325" y="185" font-size="11" fill="#f3e8ff" text-anchor="middle">Presión Atmosférica (hPa), Temperatura (°C), Humedad (%) — Alerta de Tormentas</text>
  </g>

  <!-- 8.2 RELOJ DE TIEMPO REAL DS3231 RTC (BOTTOM RIGHT) -->
  <g transform="translate(1000, 885)" filter="url(#card-shadow)">
    <rect width="650" height="210" rx="12" fill="url(#blue-pcb)" stroke="#3b82f6" stroke-width="2"/>
    <rect width="650" height="32" rx="12" fill="#1e3a8a"/>
    <text x="325" y="22" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🕒 RELOJ RTC DS3231 (Dirección I2C: 0x68)</text>

    <!-- Pines Header I2C Superiores (VCC, GND, SCL, SDA) -> Y_rel=60 -> Absolute Y=945 -->
    <!-- VCC : Absolute X=1110 -->
    <circle cx="110" cy="60" r="7.5" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>
    <text x="110" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">VCC (3.3V)</text>

    <!-- GND : Absolute X=1220 -->
    <circle cx="220" cy="60" r="7.5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <text x="220" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- SCL : Absolute X=1330 -->
    <circle cx="330" cy="60" r="7.5" fill="#16a34a" stroke="#ffffff" stroke-width="2"/>
    <text x="330" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">SCL</text>

    <!-- SDA : Absolute X=1440 -->
    <circle cx="440" cy="60" r="7.5" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
    <text x="440" y="85" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">SDA</text>

    <!-- Soporte Pila Botón CR2032 -->
    <circle cx="530" cy="140" r="35" fill="url(#silver-metal)" stroke="#64748b" stroke-width="2.5"/>
    <text x="530" y="138" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">CR2032</text>
    <text x="530" y="154" font-size="10" fill="#334155" text-anchor="middle">3V Litio</text>

    <text x="240" y="135" font-size="12" fill="#e0f2fe">Oscilador TCXO de Alta Precisión Compensado</text>
    <text x="240" y="155" font-size="11" fill="#93c5fd">Sincroniza hora sin conexión en Reticulum y NomadNet</text>
  </g>

  <!-- ==================== 9. TABLA DE REFERENCIA RÁPIDA (FOOTER) ==================== -->
  <g transform="translate(100, 1130)" filter="url(#card-shadow)">
    <rect width="1600" height="185" rx="10" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    <rect width="1600" height="30" rx="10" fill="#1e293b"/>
    <text x="800" y="20" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">📋 TABLA DE REFERENCIA RÁPIDA DE CONEXIONADO Y PINES EXACTOS</text>

    <g transform="translate(30, 48)">
      <!-- Columna 1 -->
      <g transform="translate(0, 0)">
        <text x="0" y="15" font-size="12" font-weight="bold" fill="#38bdf8">📌 ALIMENTACIÓN Y VOLTAJE:</text>
        <text x="0" y="38" font-size="12" fill="#cbd5e1"><tspan fill="#f87171" font-weight="bold">12V Batería (+): </tspan>Va al borne VIN+ del INA219. Sale por VIN- hacia IN+ del Step-Down.</text>
        <text x="0" y="58" font-size="12" fill="#cbd5e1"><tspan fill="#fb923c" font-weight="bold">5.1V Step-Down OUT+: </tspan>Conectado a Pin 2 de la Pi Zero y al Pin 5V/VCC del RNode LoRa.</text>
        <text x="0" y="78" font-size="12" fill="#cbd5e1"><tspan fill="#94a3b8" font-weight="bold">GND (Masa Común): </tspan>Conecta Batería (-), Step-Down IN-/OUT-, Pi Zero Pin 6 y RNode GND.</text>
        <text x="0" y="98" font-size="12" fill="#cbd5e1"><tspan fill="#f87171" font-weight="bold">3.3V Pi Zero Pin 1: </tspan>Alimenta exclusivamente la lógica de los 3 sensores I2C.</text>
      </g>

      <!-- Columna 2 -->
      <g transform="translate(550, 0)">
        <text x="0" y="15" font-size="12" font-weight="bold" fill="#38bdf8">🔌 UART SERIAL LORA (115200 BAUD):</text>
        <text x="0" y="38" font-size="12" fill="#cbd5e1"><tspan fill="#c084fc" font-weight="bold">Pi Zero Pin 8 (TXD / GPIO 14): </tspan>Conectado al Pin RX del RNode ESP32.</text>
        <text x="0" y="58" font-size="12" fill="#cbd5e1"><tspan fill="#fde047" font-weight="bold">Pi Zero Pin 10 (RXD / GPIO 15): </tspan>Conectado al Pin TX del RNode ESP32.</text>
        <text x="0" y="78" font-size="12" fill="#cbd5e1"><tspan fill="#38bdf8" font-weight="bold">Puerto Serial: </tspan>/dev/ttyAMA0 configurado en Reticulum rnsd.</text>
        <text x="0" y="98" font-size="12" fill="#4ade80"><tspan fill="#4ade80" font-weight="bold">Protocolo: </tspan>KISS Serial Framing de alta eficiencia para mallas LoRa.</text>
      </g>

      <!-- Columna 3 -->
      <g transform="translate(1100, 0)">
        <text x="0" y="15" font-size="12" font-weight="bold" fill="#38bdf8">🔍 BUS I2C COMPARTIDO (PARALELO):</text>
        <text x="0" y="38" font-size="12" fill="#cbd5e1"><tspan fill="#60a5fa" font-weight="bold">0x40 (INA219): </tspan>Voltaje, amperaje y estado de carga de la batería.</text>
        <text x="0" y="58" font-size="12" fill="#cbd5e1"><tspan fill="#c084fc" font-weight="bold">0x76 (BME280): </tspan>Presión atmosférica, temperatura y tormentas.</text>
        <text x="0" y="78" font-size="12" fill="#cbd5e1"><tspan fill="#38bdf8" font-weight="bold">0x68 (DS3231 RTC): </tspan>Reloj de precisión en tiempo real con pila CR2032.</text>
        <text x="0" y="98" font-size="12" fill="#4ade80">✓ Los 3 sensores comparten SDA (Pin 3) y SCL (Pin 5) sin conflicto.</text>
      </g>
    </g>
  </g>

  <!-- ==================== CABLEADO ULTRA-LIMPIO POR CALLEJONES ==================== -->
  <g filter="url(#wire-glow)">
    
    <!-- 1. POTENCIA 12V -->
    <!-- Batería (+) [X=265, Y=190] ➔ INA219 VIN+ [X=440, Y=164] -->
    <path d="M 265 190 L 330 190 L 330 164 L 440 164" fill="none" stroke="#ef4444" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="265" cy="190" r="4.5" fill="#ffffff"/>
    <circle cx="440" cy="164" r="4.5" fill="#ffffff"/>

    <!-- INA219 VIN- [X=560, Y=164] ➔ Step-Down IN+ [X=695, Y=220] -->
    <path d="M 560 164 L 640 164 L 640 220 L 695 220" fill="none" stroke="#f87171" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="560" cy="164" r="4.5" fill="#ffffff"/>
    <circle cx="695" cy="220" r="4.5" fill="#ffffff"/>

    <!-- Batería (-) [X=165, Y=190] ➔ Step-Down IN- [X=695, Y=164] -->
    <path d="M 165 190 L 165 290 L 660 290 L 660 164 L 695 164" fill="none" stroke="#64748b" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="165" cy="190" r="4.5" fill="#ffffff"/>
    <circle cx="695" cy="164" r="4.5" fill="#ffffff"/>

    <!-- 2. SALIDA 5.1V REGULADA (LM2596 OUT+ / OUT-) -->
    <!-- Step-Down OUT+ (5.1V) [X=905, Y=220] ➔ Distribuidor [X=940, Y=330] -->
    <!-- Rama a Pi Zero Pin 2 [X=165, Y=474] -->
    <path d="M 905 220 L 940 220 L 940 330 L 165 330 L 165 474" fill="none" stroke="#ea580c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Rama a RNode 5V [X=1010, Y=460] -->
    <path d="M 940 220 L 970 220 L 970 460 L 1010 460" fill="none" stroke="#ea580c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="905" cy="220" r="4.5" fill="#ffffff"/>
    <circle cx="165" cy="474" r="4.5" fill="#ffffff"/>
    <circle cx="1010" cy="460" r="4.5" fill="#ffffff"/>

    <!-- Step-Down OUT- (GND) [X=905, Y=164] ➔ Distribuidor [X=955, Y=345] -->
    <!-- Rama a Pi Zero Pin 6 [X=245, Y=474] -->
    <path d="M 905 164 L 955 164 L 955 345 L 245 345 L 245 474" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Rama a RNode GND [X=1010, Y=515] -->
    <path d="M 955 164 L 980 164 L 980 515 L 1010 515" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="905" cy="164" r="4.5" fill="#ffffff"/>
    <circle cx="245" cy="474" r="4.5" fill="#ffffff"/>
    <circle cx="1010" cy="515" r="4.5" fill="#ffffff"/>

    <!-- 3. UART SERIAL (Pines 8 y 10 ➔ RNode) (Canal Superior Y=360 y Y=375) -->
    <!-- Pi Zero Pin 8 (TXD) [X=285, Y=474] ➔ RNode RX [X=1010, Y=570] -->
    <path d="M 285 474 L 285 360 L 960 360 L 960 570 L 1010 570" fill="none" stroke="#9333ea" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="285" cy="474" r="4" fill="#ffffff"/>
    <circle cx="1010" cy="570" r="4" fill="#ffffff"/>

    <!-- Pi Zero Pin 10 (RXD) [X=325, Y=474] ➔ RNode TX [X=1010, Y=625] -->
    <path d="M 325 474 L 325 375 L 945 375 L 945 625 L 1010 625" fill="none" stroke="#eab308" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="325" cy="474" r="4" fill="#ffffff"/>
    <circle cx="1010" cy="625" r="4" fill="#ffffff"/>

    <!-- 4. I2C DESDE RASPBERRY PI ZERO AL RIEL (Por el callejón izquierdo X=40 a X=80) -->
    <!-- Pin 1 (3.3V) [X=165, Y=446] ➔ Riel 3.3V (Y=785) -->
    <path d="M 165 446 L 165 420 L 45 420 L 45 785 L 125 785" fill="none" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="165" cy="446" r="4" fill="#ffffff"/>
    <circle cx="125" cy="785" r="4.5" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>

    <!-- Pin 6 (GND) [X=245, Y=474] ➔ Riel GND (Y=805) -->
    <path d="M 245 474 L 245 430 L 60 430 L 60 805 L 125 805" fill="none" stroke="#64748b" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="245" cy="474" r="4" fill="#ffffff"/>
    <circle cx="125" cy="805" r="4.5" fill="#64748b" stroke="#ffffff" stroke-width="1.5"/>

    <!-- Pin 5 (SCL) [X=245, Y=446] ➔ Riel SCL (Y=825) -->
    <path d="M 245 446 L 245 400 L 75 400 L 75 825 L 125 825" fill="none" stroke="#16a34a" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="245" cy="446" r="4" fill="#ffffff"/>
    <circle cx="125" cy="825" r="4.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>

    <!-- Pin 3 (SDA) [X=205, Y=446] ➔ Riel SDA (Y=845) -->
    <path d="M 205 446 L 205 410 L 90 410 L 90 845 L 125 845" fill="none" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="205" cy="446" r="4" fill="#ffffff"/>
    <circle cx="125" cy="845" r="4.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>

    <!-- 5. CONEXIÓN I2C DEL INA219 (Pasa por callejón izquierdo superior X=30..40 para NO tocar la Pi) -->
    <!-- INA219 VCC [X=415, Y=248] ➔ Riel 3.3V (Y=785) -->
    <path d="M 415 248 L 415 295 L 35 295 L 35 785 L 125 785" fill="none" stroke="#dc2626" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="415" cy="248" r="4" fill="#ffffff"/>

    <!-- INA219 GND [X=470, Y=248] ➔ Riel GND (Y=805) -->
    <path d="M 470 248 L 470 305 L 50 305 L 50 805 L 125 805" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="470" cy="248" r="4" fill="#ffffff"/>

    <!-- INA219 SCL [X=530, Y=248] ➔ Riel SCL (Y=825) -->
    <path d="M 530 248 L 530 315 L 65 315 L 65 825 L 125 825" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="530" cy="248" r="4" fill="#ffffff"/>

    <!-- INA219 SDA [X=585, Y=248] ➔ Riel SDA (Y=845) -->
    <path d="M 585 248 L 585 325 L 80 325 L 80 845 L 125 845" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="585" cy="248" r="4" fill="#ffffff"/>

    <!-- 6. DERIVACIONES DE SENSORES INFERIORES AL RIEL I2C (100% Verticales Rectas) -->
    <!-- SENSOR BME280 -->
    <!-- VIN [X=260, Y=945] ➔ Riel 3.3V (Y=785) -->
    <line x1="260" y1="945" x2="260" y2="785" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="260" cy="945" r="4" fill="#ffffff"/>
    <circle cx="260" cy="785" r="4.5" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>

    <!-- GND [X=370, Y=945] ➔ Riel GND (Y=805) -->
    <line x1="370" y1="945" x2="370" y2="805" stroke="#64748b" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="370" cy="945" r="4" fill="#ffffff"/>
    <circle cx="370" cy="805" r="4.5" fill="#64748b" stroke="#ffffff" stroke-width="1.5"/>

    <!-- SCL [X=480, Y=945] ➔ Riel SCL (Y=825) -->
    <line x1="480" y1="945" x2="480" y2="825" stroke="#16a34a" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="480" cy="945" r="4" fill="#ffffff"/>
    <circle cx="480" cy="825" r="4.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>

    <!-- SDA [X=590, Y=945] ➔ Riel SDA (Y=845) -->
    <line x1="590" y1="945" x2="590" y2="845" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="590" cy="945" r="4" fill="#ffffff"/>
    <circle cx="590" cy="845" r="4.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>

    <!-- SENSOR DS3231 RTC -->
    <!-- VCC [X=1110, Y=945] ➔ Riel 3.3V (Y=785) -->
    <line x1="1110" y1="945" x2="1110" y2="785" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="1110" cy="945" r="4" fill="#ffffff"/>
    <circle cx="1110" cy="785" r="4.5" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>

    <!-- GND [X=1220, Y=945] ➔ Riel GND (Y=805) -->
    <line x1="1220" y1="945" x2="1220" y2="805" stroke="#64748b" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="1220" cy="945" r="4" fill="#ffffff"/>
    <circle cx="1220" cy="805" r="4.5" fill="#64748b" stroke="#ffffff" stroke-width="1.5"/>

    <!-- SCL [X=1330, Y=945] ➔ Riel SCL (Y=825) -->
    <line x1="1330" y1="945" x2="1330" y2="825" stroke="#16a34a" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="1330" cy="945" r="4" fill="#ffffff"/>
    <circle cx="1330" cy="825" r="4.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>

    <!-- SDA [X=1440, Y=945] ➔ Riel SDA (Y=845) -->
    <line x1="1440" y1="945" x2="1440" y2="845" stroke="#0284c7" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="1440" cy="945" r="4" fill="#ffffff"/>
    <circle cx="1440" cy="845" r="4.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>

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

    print("Renderizando esquema con Chromium headless (1800x1350)...")
    subprocess.run([
        "chromium", "--headless", "--disable-gpu",
        f"--screenshot={png_file}",
        "--window-size=1800,1350",
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
