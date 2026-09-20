#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama de Hardware de Nivel Profesional (Ultra-Clean Dark Aesthetic)
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)
"""

import os
import subprocess
from PIL import Image

SVG_DATA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000" style="background:#0b0f19; font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  
  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.75" stroke-opacity="0.6"/>
    </pattern>

    <!-- Gradients -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <linearGradient id="rpi-pcb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#166534"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>

    <linearGradient id="chip-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="metal-silver" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e2e8f0"/>
      <stop offset="50%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>

    <linearGradient id="gold-pin" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>

    <linearGradient id="blue-mod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1d4ed8"/>
      <stop offset="100%" stop-color="#1e3a8a"/>
    </linearGradient>

    <linearGradient id="purple-mod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7e22ce"/>
      <stop offset="100%" stop-color="#581c87"/>
    </linearGradient>

    <linearGradient id="teal-mod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f766e"/>
      <stop offset="100%" stop-color="#134e4a"/>
    </linearGradient>

    <linearGradient id="slate-mod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <!-- Drop Shadows -->
    <filter id="glow-card" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Background Grid Canvas -->
  <rect width="1600" height="1000" fill="#0b0f19"/>
  <rect width="1600" height="1000" fill="url(#grid)"/>

  <!-- ==================== TOP NAVIGATION / HEADER ==================== -->
  <rect x="0" y="0" width="1600" height="70" fill="url(#header-grad)" stroke="#1e293b" stroke-width="1"/>
  
  <g transform="translate(40, 22)">
    <circle cx="16" cy="14" r="14" fill="#0284c7"/>
    <text x="16" y="20" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">📡</text>
    <text x="42" y="19" font-size="18" font-weight="800" fill="#ffffff" letter-spacing="0.5">NODO DE EMERGENCIA RETICULUM</text>
    <text x="375" y="19" font-size="14" font-weight="500" fill="#64748b">|</text>
    <text x="390" y="19" font-size="14" font-weight="600" fill="#38bdf8">Guía de Cableado y Pinout de Hardware</text>
  </g>

  <g transform="translate(1260, 26)">
    <rect x="0" y="0" width="290" height="28" rx="14" fill="#1e293b" stroke="#334155"/>
    <text x="145" y="18" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">CIPRO Panamá — www.cipropanama.org</text>
  </g>

  <!-- ==================== WIRING TRACES (BACKGROUND LAYER) ==================== -->
  
  <!-- 12V Power from Battery to INA219 VIN+ (X=140 to X=1120) -->
  <path d="M 140 180 L 140 105 L 1120 105 L 1120 180" fill="none" stroke="#ef4444" stroke-width="3.5" stroke-linecap="round"/>

  <!-- 12V Switched from INA219 VIN- (X=1150) to Step-Down IN+ (X=360) -->
  <path d="M 1150 180 L 1150 120 L 360 120 L 360 180" fill="none" stroke="#f87171" stroke-width="3" stroke-linecap="round"/>

  <!-- Battery GND to Step-Down IN- -->
  <path d="M 80 180 L 80 135 L 330 135 L 330 180" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>

  <!-- Step-Down 5.1V OUT+ (X=430) to Pi Zero Pin 2 (X=660) & RNode 5V (X=1420) -->
  <path d="M 430 180 L 430 150 L 660 150 L 660 255" fill="none" stroke="#f97316" stroke-width="3" stroke-linecap="round"/>
  <path d="M 660 150 L 1420 150 L 1420 280" fill="none" stroke="#f97316" stroke-width="3" stroke-dasharray="6,4" stroke-linecap="round"/>

  <!-- Step-Down OUT- (GND) to System Common GND (X=400 to Pi Pin 6 X=660) -->
  <path d="M 400 180 L 400 162 L 720 162 L 720 315" fill="none" stroke="#475569" stroke-width="3" stroke-linecap="round"/>

  <!-- I2C SHARED VERTICAL RAILS (Right Side) -->
  
  <!-- 3.3V Rail (Red #f43f5e) from Pi Pin 1 (X=620, Y=255) -->
  <path d="M 620 255 L 820 255 L 820 900" fill="none" stroke="#f43f5e" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="820" cy="255" r="4" fill="#f43f5e"/>
  <!-- Branch to INA219 VCC -->
  <path d="M 820 255 L 940 255" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
  <!-- Branch to BME280 VCC -->
  <circle cx="820" cy="515" r="4" fill="#f43f5e"/>
  <path d="M 820 515 L 940 515" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
  <!-- Branch to DS3231 VCC -->
  <circle cx="820" cy="765" r="4" fill="#f43f5e"/>
  <path d="M 820 765 L 940 765" fill="none" stroke="#f43f5e" stroke-width="2.5"/>

  <!-- GND Rail (Gray #64748b) from Pi Pin 6 (X=660, Y=315) -->
  <path d="M 660 315 L 845 315 L 845 900" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="845" cy="285" r="4" fill="#64748b"/>
  <path d="M 845 285 L 940 285" fill="none" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="845" cy="545" r="4" fill="#64748b"/>
  <path d="M 845 545 L 940 545" fill="none" stroke="#64748b" stroke-width="2.5"/>
  <circle cx="845" cy="795" r="4" fill="#64748b"/>
  <path d="M 845 795 L 940 795" fill="none" stroke="#64748b" stroke-width="2.5"/>
  <!-- GND to RNode -->
  <path d="M 845 315 L 845 170 L 1445 170 L 1445 280" fill="none" stroke="#64748b" stroke-width="2.5"/>

  <!-- SDA Rail (Blue #0ea5e9) from Pi Pin 3 (X=620, Y=285) -->
  <path d="M 620 285 L 870 285 L 870 900" fill="none" stroke="#0ea5e9" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="870" cy="315" r="4" fill="#0ea5e9"/>
  <path d="M 870 315 L 940 315" fill="none" stroke="#0ea5e9" stroke-width="2.5"/>
  <circle cx="870" cy="575" r="4" fill="#0ea5e9"/>
  <path d="M 870 575 L 940 575" fill="none" stroke="#0ea5e9" stroke-width="2.5"/>
  <circle cx="870" cy="825" r="4" fill="#0ea5e9"/>
  <path d="M 870 825 L 940 825" fill="none" stroke="#0ea5e9" stroke-width="2.5"/>

  <!-- SCL Rail (Emerald #10b981) from Pi Pin 5 (X=620, Y=315) -->
  <path d="M 620 315 L 895 315 L 895 900" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="895" cy="345" r="4" fill="#10b981"/>
  <path d="M 895 345 L 940 345" fill="none" stroke="#10b981" stroke-width="2.5"/>
  <circle cx="895" cy="605" r="4" fill="#10b981"/>
  <path d="M 895 605 L 940 605" fill="none" stroke="#10b981" stroke-width="2.5"/>
  <circle cx="895" cy="855" r="4" fill="#10b981"/>
  <path d="M 895 855 L 940 855" fill="none" stroke="#10b981" stroke-width="2.5"/>

  <!-- UART SERIAL LINES to RNode -->
  <!-- Pi Pin 8 (TX / GPIO 14) (X=660, Y=345) to RNode RX (X=1470, Y=280) -->
  <path d="M 660 345 L 750 345 L 750 185 L 1470 185 L 1470 280" fill="none" stroke="#a855f7" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Pi Pin 10 (RX / GPIO 15) (X=660, Y=375) to RNode TX (X=1495, Y=280) -->
  <path d="M 660 375 L 730 375 L 730 200 L 1495 200 L 1495 280" fill="none" stroke="#eab308" stroke-width="2.5" stroke-linecap="round"/>

  <!-- ==================== COMPONENT 1: BATERIA SOLAR 12V ==================== -->
  <g transform="translate(40, 180)" filter="url(#glow-card)">
    <rect x="0" y="0" width="180" height="150" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <rect x="0" y="0" width="180" height="32" rx="10" fill="#0f172a"/>
    <text x="90" y="21" font-size="12" font-weight="700" fill="#f8fafc" text-anchor="middle">🔋 BATERÍA SOLAR 12V</text>

    <!-- Terminals -->
    <circle cx="40" cy="70" r="14" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
    <text x="40" y="75" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="40" y="100" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">GND</text>

    <circle cx="100" cy="70" r="14" fill="#991b1b" stroke="#f87171" stroke-width="2"/>
    <text x="100" y="75" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="100" y="100" font-size="10" font-weight="bold" fill="#fca5a5" text-anchor="middle">+12V</text>

    <text x="90" y="130" font-size="11" fill="#94a3b8" text-anchor="middle">LiFePO4 / 12V 10Ah-50Ah</text>
  </g>

  <!-- ==================== COMPONENT 2: STEP-DOWN DC-DC ==================== -->
  <g transform="translate(260, 180)" filter="url(#glow-card)">
    <rect x="0" y="0" width="200" height="150" rx="10" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <rect x="0" y="0" width="200" height="32" rx="10" fill="#075985"/>
    <text x="100" y="21" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">⚡ STEP-DOWN DC-DC</text>

    <!-- Terminals Input -->
    <text x="50" y="55" font-size="10" font-weight="700" fill="#bae6fd" text-anchor="middle">ENTRADA 12V</text>
    <circle cx="30" cy="75" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="30" y="98" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">IN -</text>
    
    <circle cx="70" cy="75" r="9" fill="#991b1b" stroke="#f87171" stroke-width="1.5"/>
    <text x="70" y="98" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">IN +</text>

    <!-- Terminals Output -->
    <text x="150" y="55" font-size="10" font-weight="700" fill="#bae6fd" text-anchor="middle">SALIDA 5.1V</text>
    <circle cx="130" cy="75" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="130" y="98" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>
    
    <circle cx="170" cy="75" r="9" fill="#c2410c" stroke="#fb923c" stroke-width="1.5"/>
    <text x="170" y="98" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">5.1V</text>

    <text x="100" y="132" font-size="10" fill="#e0f2fe" text-anchor="middle">Regulador 12V a 5.1V (3A)</text>
  </g>

  <!-- ==================== COMPONENT 3: PINOUT & COLOR GUIDE (LEFT BOTTOM) ==================== -->
  <g transform="translate(40, 360)" filter="url(#glow-card)">
    <rect x="0" y="0" width="420" height="600" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <rect x="0" y="0" width="420" height="34" rx="10" fill="#0f172a"/>
    <text x="210" y="22" font-size="12" font-weight="700" fill="#38bdf8" text-anchor="middle">📋 CÓDIGO DE LÍNEAS Y COLORES</text>

    <g transform="translate(20, 50)">
      <!-- Item 1 -->
      <line x1="0" y1="10" x2="35" y2="10" stroke="#ef4444" stroke-width="4"/>
      <text x="45" y="14" font-size="11" font-weight="700" fill="#f8fafc">+12V Batería Solar (Borne + a VIN+ INA219)</text>

      <!-- Item 2 -->
      <line x1="0" y1="45" x2="35" y2="45" stroke="#f87171" stroke-width="3.5"/>
      <text x="45" y="49" font-size="11" font-weight="700" fill="#f8fafc">+12V Conmutado (VIN- INA219 a IN+ Step-Down)</text>

      <!-- Item 3 -->
      <line x1="0" y1="80" x2="35" y2="80" stroke="#f97316" stroke-width="3.5"/>
      <text x="45" y="84" font-size="11" font-weight="700" fill="#f8fafc">+5.1V Regulado (OUT+ a Pin 2 de Pi Zero y RNode)</text>

      <!-- Item 4 -->
      <line x1="0" y1="115" x2="35" y2="115" stroke="#f43f5e" stroke-width="3"/>
      <text x="45" y="119" font-size="11" font-weight="700" fill="#f8fafc">+3.3V Lógica (Pin 1 a VCC de Sensores I2C)</text>

      <!-- Item 5 -->
      <line x1="0" y1="150" x2="35" y2="150" stroke="#64748b" stroke-width="3"/>
      <text x="45" y="154" font-size="11" font-weight="700" fill="#f8fafc">GND Común (Pin 6 y Masa General de Sistema)</text>

      <!-- Item 6 -->
      <line x1="0" y1="185" x2="35" y2="185" stroke="#0ea5e9" stroke-width="3"/>
      <text x="45" y="189" font-size="11" font-weight="700" fill="#f8fafc">SDA I2C Datos (Pin 3 / GPIO 2 en paralelo)</text>

      <!-- Item 7 -->
      <line x1="0" y1="220" x2="35" y2="220" stroke="#10b981" stroke-width="3"/>
      <text x="45" y="224" font-size="11" font-weight="700" fill="#f8fafc">SCL I2C Reloj (Pin 5 / GPIO 3 en paralelo)</text>

      <!-- Item 8 -->
      <line x1="0" y1="255" x2="35" y2="255" stroke="#a855f7" stroke-width="3"/>
      <text x="45" y="259" font-size="11" font-weight="700" fill="#f8fafc">UART TX SBC (Pin 8 / GPIO 14 a RX RNode)</text>

      <!-- Item 9 -->
      <line x1="0" y1="290" x2="35" y2="290" stroke="#eab308" stroke-width="3"/>
      <text x="45" y="294" font-size="11" font-weight="700" fill="#f8fafc">UART RX SBC (Pin 10 / GPIO 15 a TX RNode)</text>
    </g>

    <!-- Info Callout -->
    <g transform="translate(15, 390)">
      <rect x="0" y="0" width="390" height="185" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
      <text x="15" y="25" font-size="12" font-weight="700" fill="#38bdf8">💡 BUS I2C EN PARALELO (SIN CONFLICTOS):</text>
      <text x="15" y="50" font-size="11" fill="#cbd5e1">• INA219 (0x40), BME280 (0x76) y DS3231 (0x68)</text>
      <text x="15" y="70" fill="#cbd5e1" font-size="11">  se unen en los mismos 4 puntos:</text>
      <text x="25" y="92" font-size="11" font-weight="700" fill="#38bdf8">Pin 1 (3.3V) | Pin 6 (GND) | Pin 3 (SDA) | Pin 5 (SCL)</text>
      <text x="15" y="118" font-size="11" fill="#cbd5e1">• El protocolo I2C direcciona cada chip automáticamente.</text>
      <text x="15" y="138" font-size="11" fill="#cbd5e1">• El radio RNode usa UART independiente (Pines 8 y 10).</text>
      <text x="15" y="162" font-size="11" font-weight="700" fill="#10b981">✓ Consumo promedio del nodo completo: ~1.2W</text>
    </g>
  </g>

  <!-- ==================== COMPONENT 4: RASPBERRY PI ZERO W (CENTER) ==================== -->
  <g transform="translate(500, 180)" filter="url(#glow-card)">
    <!-- Realistic PCB -->
    <rect x="0" y="0" width="260" height="780" rx="14" fill="url(#rpi-pcb)" stroke="#22c55e" stroke-width="1.5"/>
    <circle cx="15" cy="15" r="7" fill="url(#gold-pin)"/>
    <circle cx="245" cy="15" r="7" fill="url(#gold-pin)"/>
    <circle cx="15" cy="765" r="7" fill="url(#gold-pin)"/>
    <circle cx="245" cy="765" r="7" fill="url(#gold-pin)"/>

    <!-- Header Title -->
    <rect x="0" y="0" width="260" height="38" rx="14" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
    <text x="130" y="24" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">RASPBERRY PI ZERO W</text>

    <!-- Broadcom Chip -->
    <rect x="25" y="440" width="85" height="85" rx="6" fill="url(#chip-grad)" stroke="#475569" stroke-width="1"/>
    <text x="67" y="480" font-size="11" font-weight="700" fill="#f8fafc" text-anchor="middle">Broadcom</text>
    <text x="67" y="496" font-size="9" fill="#94a3b8" text-anchor="middle">BCM2835 1GHz</text>

    <!-- MicroSD -->
    <rect x="25" y="680" width="65" height="50" rx="4" fill="url(#metal-silver)" stroke="#64748b"/>
    <text x="57" y="710" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="middle">MicroSD</text>

    <!-- GPIO 40-Pin Box -->
    <rect x="120" y="55" width="115" height="700" rx="8" fill="#020617" stroke="#334155" stroke-width="1"/>
    <text x="177" y="72" font-size="9" font-weight="800" fill="#94a3b8" text-anchor="middle">HEADER GPIO (40 PINES)</text>

    <!-- Row 1: Pin 1 (3.3V) & Pin 2 (5V) -->
    <circle cx="140" cy="95" r="6" fill="#f43f5e" stroke="#ffffff" stroke-width="1"/>
    <text x="110" y="99" font-size="9" font-weight="bold" fill="#f43f5e" text-anchor="end">Pin 1 (3.3V)</text>
    
    <circle cx="180" cy="95" r="6" fill="#f97316" stroke="#ffffff" stroke-width="1"/>
    <text x="195" y="99" font-size="9" font-weight="bold" fill="#f97316" text-anchor="start">Pin 2 (5V)</text>

    <!-- Row 2: Pin 3 (SDA) & Pin 4 (5V) -->
    <circle cx="140" cy="125" r="6" fill="#0ea5e9" stroke="#ffffff" stroke-width="1"/>
    <text x="110" y="129" font-size="9" font-weight="bold" fill="#0ea5e9" text-anchor="end">Pin 3 (SDA)</text>
    
    <circle cx="180" cy="125" r="4" fill="#334155"/>
    <text x="195" y="129" font-size="8" fill="#64748b" text-anchor="start">Pin 4</text>

    <!-- Row 3: Pin 5 (SCL) & Pin 6 (GND) -->
    <circle cx="140" cy="155" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1"/>
    <text x="110" y="159" font-size="9" font-weight="bold" fill="#10b981" text-anchor="end">Pin 5 (SCL)</text>
    
    <circle cx="180" cy="155" r="6" fill="#64748b" stroke="#ffffff" stroke-width="1"/>
    <text x="195" y="159" font-size="9" font-weight="bold" fill="#cbd5e1" text-anchor="start">Pin 6 (GND)</text>

    <!-- Row 4: Pin 7 (GPIO4) & Pin 8 (TXD) -->
    <circle cx="140" cy="185" r="4" fill="#334155"/>
    <text x="110" y="189" font-size="8" fill="#64748b" text-anchor="end">Pin 7</text>
    
    <circle cx="180" cy="185" r="6" fill="#a855f7" stroke="#ffffff" stroke-width="1"/>
    <text x="195" y="189" font-size="9" font-weight="bold" fill="#a855f7" text-anchor="start">Pin 8 (TX)</text>

    <!-- Row 5: Pin 9 (GND) & Pin 10 (RXD) -->
    <circle cx="140" cy="215" r="4" fill="#334155"/>
    <text x="110" y="219" font-size="8" fill="#64748b" text-anchor="end">Pin 9</text>
    
    <circle cx="180" cy="215" r="6" fill="#eab308" stroke="#ffffff" stroke-width="1"/>
    <text x="195" y="219" font-size="9" font-weight="bold" fill="#eab308" text-anchor="start">Pin 10 (RX)</text>

    <!-- Pins 11-40 (Dimmed / Realistic) -->
    <g fill="#1e293b" stroke="#334155">
      <circle cx="140" cy="245" r="4"/><circle cx="180" cy="245" r="4"/>
      <circle cx="140" cy="275" r="4"/><circle cx="180" cy="275" r="4"/>
      <circle cx="140" cy="305" r="4"/><circle cx="180" cy="305" r="4"/>
      <circle cx="140" cy="335" r="4"/><circle cx="180" cy="335" r="4"/>
      <circle cx="140" cy="365" r="4"/><circle cx="180" cy="365" r="4"/>
      <circle cx="140" cy="395" r="4"/><circle cx="180" cy="395" r="4"/>
      <circle cx="140" cy="425" r="4"/><circle cx="180" cy="425" r="4"/>
      <circle cx="140" cy="455" r="4"/><circle cx="180" cy="455" r="4"/>
      <circle cx="140" cy="485" r="4"/><circle cx="180" cy="485" r="4"/>
      <circle cx="140" cy="515" r="4"/><circle cx="180" cy="515" r="4"/>
      <circle cx="140" cy="545" r="4"/><circle cx="180" cy="545" r="4"/>
      <circle cx="140" cy="575" r="4"/><circle cx="180" cy="575" r="4"/>
      <circle cx="140" cy="605" r="4"/><circle cx="180" cy="605" r="4"/>
      <circle cx="140" cy="635" r="4"/><circle cx="180" cy="635" r="4"/>
      <circle cx="140" cy="665" r="4"/><circle cx="180" cy="665" r="4"/>
      <circle cx="140" cy="695" r="4"/><circle cx="180" cy="695" r="4"/>
      <circle cx="140" cy="725" r="4"/><circle cx="180" cy="725" r="4"/>
    </g>
  </g>

  <!-- ==================== COMPONENT 5: I2C MODULES CONTAINER ==================== -->
  <g transform="translate(940, 180)">
    <!-- Container -->
    <rect x="0" y="0" width="450" height="780" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1.5" stroke-dasharray="6,4"/>
    <text x="225" y="28" font-size="13" font-weight="800" fill="#38bdf8" text-anchor="middle">BUS I2C COMPARTIDO EN PARALELO</text>
    <text x="225" y="44" font-size="10" fill="#94a3b8" text-anchor="middle">3.3V (Pin 1) | GND (Pin 6) | SDA (Pin 3) | SCL (Pin 5)</text>

    <!-- MODULE 1: INA219 (0x40) -->
    <g transform="translate(20, 60)" filter="url(#glow-card)">
      <rect x="0" y="0" width="410" height="200" rx="10" fill="url(#blue-mod)" stroke="#3b82f6" stroke-width="1.5"/>
      <rect x="0" y="0" width="410" height="30" rx="10" fill="#1e3a8a"/>
      <text x="205" y="20" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">🔋 SENSOR BATERÍA SOLAR: INA219 (I2C: 0x40)</text>

      <!-- Pins -->
      <g transform="translate(15, 45)">
        <circle cx="20" cy="0" r="6" fill="#f43f5e" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="4" font-size="10" font-weight="bold" fill="#ffffff">VCC (3.3V)</text>

        <circle cx="20" cy="28" r="6" fill="#64748b" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="32" font-size="10" font-weight="bold" fill="#ffffff">GND</text>

        <circle cx="20" cy="56" r="6" fill="#0ea5e9" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="60" font-size="10" font-weight="bold" fill="#ffffff">SDA</text>

        <circle cx="20" cy="84" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="88" font-size="10" font-weight="bold" fill="#ffffff">SCL</text>
      </g>

      <!-- Terminal Block -->
      <g transform="translate(220, 45)">
        <rect x="0" y="0" width="170" height="110" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="85" y="22" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">BORNERA 12V (POTENCIA)</text>
        
        <circle cx="35" cy="55" r="8" fill="#ef4444" stroke="#ffffff" stroke-width="1"/>
        <text x="50" y="59" font-size="10" font-weight="bold" fill="#ffffff">VIN + (Bat +12V)</text>

        <circle cx="35" cy="88" r="8" fill="#f87171" stroke="#ffffff" stroke-width="1"/>
        <text x="50" y="92" font-size="10" font-weight="bold" fill="#ffffff">VIN - (A Step-Down)</text>
      </g>
      <text x="205" y="182" font-size="10" fill="#93c5fd" text-anchor="middle">Mide Voltaje real de Batería (0-26V DC) y Consumo en mA</text>
    </g>

    <!-- MODULE 2: BME280 (0x76) -->
    <g transform="translate(20, 290)" filter="url(#glow-card)">
      <rect x="0" y="0" width="410" height="200" rx="10" fill="url(#purple-mod)" stroke="#a855f7" stroke-width="1.5"/>
      <rect x="0" y="0" width="410" height="30" rx="10" fill="#581c87"/>
      <text x="205" y="20" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">🌦️ SENSOR AMBIENTAL: BME280 (I2C: 0x76 / 0x77)</text>

      <!-- Pins -->
      <g transform="translate(15, 45)">
        <circle cx="20" cy="0" r="6" fill="#f43f5e" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="4" font-size="10" font-weight="bold" fill="#ffffff">VIN / VCC (3.3V)</text>

        <circle cx="20" cy="28" r="6" fill="#64748b" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="32" font-size="10" font-weight="bold" fill="#ffffff">GND</text>

        <circle cx="20" cy="56" r="6" fill="#0ea5e9" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="60" font-size="10" font-weight="bold" fill="#ffffff">SDA / SDI</text>

        <circle cx="20" cy="84" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="88" font-size="10" font-weight="bold" fill="#ffffff">SCL / SCK</text>
      </g>

      <!-- Metrics Card -->
      <g transform="translate(200, 45)">
        <rect x="0" y="0" width="190" height="110" rx="8" fill="#3b0764" stroke="#c084fc" stroke-width="1.5"/>
        <text x="95" y="24" font-size="10" font-weight="bold" fill="#f3e8ff" text-anchor="middle">TELEMETRÍA EN VIVO</text>
        <text x="15" y="50" font-size="10" fill="#e9d5ff">• Presión Barométrica (hPa)</text>
        <text x="15" y="70" font-size="10" fill="#e9d5ff">• Temperatura Ambiental (°C)</text>
        <text x="15" y="90" font-size="10" fill="#e9d5ff">• Alerta Temprana Tormenta</text>
      </g>
      <text x="205" y="182" font-size="10" fill="#e9d5ff" text-anchor="middle">Conectado en paralelo sobre las mismas 4 pistas I2C</text>
    </g>

    <!-- MODULE 3: DS3231 RTC (0x68) -->
    <g transform="translate(20, 520)" filter="url(#glow-card)">
      <rect x="0" y="0" width="410" height="200" rx="10" fill="url(#teal-mod)" stroke="#14b8a6" stroke-width="1.5"/>
      <rect x="0" y="0" width="410" height="30" rx="10" fill="#134e4a"/>
      <text x="205" y="20" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">🕒 RELOJ OFFLINE POR HARDWARE: DS3231 (I2C: 0x68)</text>

      <!-- Pins -->
      <g transform="translate(15, 45)">
        <circle cx="20" cy="0" r="6" fill="#f43f5e" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="4" font-size="10" font-weight="bold" fill="#ffffff">VCC (3.3V)</text>

        <circle cx="20" cy="28" r="6" fill="#64748b" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="32" font-size="10" font-weight="bold" fill="#ffffff">GND</text>

        <circle cx="20" cy="56" r="6" fill="#0ea5e9" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="60" font-size="10" font-weight="bold" fill="#ffffff">SDA</text>

        <circle cx="20" cy="84" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1"/>
        <text x="35" y="88" font-size="10" font-weight="bold" fill="#ffffff">SCL</text>
      </g>

      <!-- Battery Holder -->
      <g transform="translate(220, 45)">
        <rect x="0" y="0" width="170" height="110" rx="8" fill="#134e4a" stroke="#5eead4" stroke-width="1.5"/>
        <circle cx="45" cy="55" r="28" fill="url(#metal-silver)" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="45" y="52" font-size="9" font-weight="bold" fill="#0f172a" text-anchor="middle">CR2032</text>
        <text x="45" y="66" font-size="8" fill="#334155" text-anchor="middle">Pila 3V</text>
        <text x="120" y="48" font-size="10" font-weight="bold" fill="#ccfbf1" text-anchor="middle">HORA EXACTA</text>
        <text x="120" y="68" font-size="9" fill="#99f6e4" text-anchor="middle">Sin necesidad</text>
        <text x="120" y="82" font-size="9" fill="#99f6e4" text-anchor="middle">de Internet / NTP</text>
      </g>
      <text x="205" y="182" font-size="10" fill="#ccfbf1" text-anchor="middle">Garantiza marcas de tiempo de paquetes LXMF en cerros aislados</text>
    </g>
  </g>

  <!-- ==================== COMPONENT 6: RNODE LORA (FAR RIGHT) ==================== -->
  <g transform="translate(1420, 180)" filter="url(#glow-card)">
    <rect x="0" y="0" width="150" height="480" rx="12" fill="url(#slate-mod)" stroke="#475569" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="32" rx="12" fill="#0f172a"/>
    <text x="75" y="21" font-size="11" font-weight="800" fill="#38bdf8" text-anchor="middle">📡 RNODE LORA</text>

    <!-- Antenna at TOP -->
    <g transform="translate(75, 42)">
      <rect x="-8" y="0" width="16" height="20" fill="url(#gold-pin)"/>
      <line x1="0" y1="20" x2="0" y2="55" stroke="#38bdf8" stroke-width="3.5"/>
      <polygon points="-10,55 10,55 0,72" fill="#38bdf8"/>
      <text x="0" y="86" font-size="8" font-weight="bold" fill="#38bdf8" text-anchor="middle">ANTENA RF</text>
    </g>

    <!-- Connectors -->
    <g transform="translate(15, 145)">
      <circle cx="10" cy="15" r="6" fill="#f97316" stroke="#ffffff" stroke-width="1"/>
      <text x="24" y="19" font-size="9" font-weight="bold" fill="#ffffff">5V / VCC</text>

      <circle cx="10" cy="40" r="6" fill="#64748b" stroke="#ffffff" stroke-width="1"/>
      <text x="24" y="44" font-size="9" font-weight="bold" fill="#ffffff">GND</text>

      <circle cx="10" cy="65" r="6" fill="#a855f7" stroke="#ffffff" stroke-width="1"/>
      <text x="24" y="69" font-size="9" font-weight="bold" fill="#ffffff">RX (a TX Pin 8)</text>

      <circle cx="10" cy="90" r="6" fill="#eab308" stroke="#ffffff" stroke-width="1"/>
      <text x="24" y="94" font-size="9" font-weight="bold" fill="#ffffff">TX (a RX Pin 10)</text>
    </g>

    <!-- Chip Box -->
    <g transform="translate(15, 270)">
      <rect x="0" y="0" width="120" height="95" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1"/>
      <text x="60" y="24" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">ESP32 / Heltec</text>
      <text x="60" y="44" font-size="9" fill="#f8fafc" text-anchor="middle">SX1262 / SX1276</text>
      <text x="60" y="62" font-size="8" fill="#94a3b8" text-anchor="middle">915 / 868 / 433 MHz</text>
      <text x="60" y="80" font-size="8" fill="#cbd5e1" text-anchor="middle">Firmware RNode</text>
    </g>

    <text x="75" y="410" font-size="9" fill="#94a3b8" text-anchor="middle">Serie UART</text>
    <text x="75" y="425" font-size="8" fill="#64748b" text-anchor="middle">(o USB OTG)</text>
  </g>

</svg>
"""

def main():
    svg_file = "/tmp/esquema_vectorial_nodo.svg"
    png_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/esquema_conexion_rpi_zero_i2c.png"
    jpg_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/esquema_conexion_rpi_zero_i2c.jpg"
    ina_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/ina219_wiring.jpg"
    i2c_file = "/home/procchetta/Documents/Antigravity/ReticulumNode/docs/img/i2c_sensors_wiring.jpg"

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(SVG_DATA)

    print("Renderizando SVG con Chromium headless (1600x1000 Dark Mode)...")
    subprocess.run([
        "chromium", "--headless", "--disable-gpu",
        f"--screenshot={png_file}",
        "--window-size=1600,1000",
        svg_file
    ], check=True)

    print("Optimizando y convirtiendo a JPEG alta resolución...")
    im = Image.open(png_file).convert("RGB")
    im.save(jpg_file, "JPEG", quality=96)
    im.save(ina_file, "JPEG", quality=96)
    im.save(i2c_file, "JPEG", quality=96)

    print(f"✓ Diagrama generado con éxito:\n  {jpg_file}\n  {png_file}")

if __name__ == "__main__":
    main()
