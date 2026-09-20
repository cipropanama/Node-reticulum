#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama Vectorial de Alta Precisión
CIPRO Panamá — Tecnología para ayudar (https://www.cipropanama.org)
"""

import os
import subprocess
from PIL import Image

SVG_DATA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1760 1120" width="1760" height="1120" style="background:#f8fafc; font-family:'Segoe UI', Inter, -apple-system, Roboto, Helvetica, Arial, sans-serif;">
  
  <!-- ==================== HEADER ==================== -->
  <rect x="0" y="0" width="1760" height="75" fill="#0f172a"/>
  <text x="40" y="46" font-size="23" font-weight="bold" fill="#ffffff" letter-spacing="0.5">ESQUEMA DE CONEXIONADO Y PINOUT - NODO DE EMERGENCIA RETICULUM</text>
  <text x="1340" y="46" font-size="16" font-weight="600" fill="#38bdf8">CIPRO Panamá — www.cipropanama.org</text>

  <!-- ==================== TOP BAR BADGE ==================== -->
  <rect x="40" y="85" width="500" height="32" rx="6" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1"/>
  <text x="55" y="106" font-size="13" font-weight="bold" fill="#1e293b">Microcomputador Central: Raspberry Pi Zero W / 2W (Header 40 Pines)</text>

  <!-- ==================== POWER & BATTERY SECTION (LEFT) ==================== -->
  
  <!-- 1. BATERIA SOLAR 12V -->
  <g transform="translate(40, 180)">
    <rect x="0" y="0" width="200" height="160" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>
    <rect x="0" y="0" width="200" height="35" rx="8" fill="#0f172a"/>
    <text x="100" y="23" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🔋 BATERÍA SOLAR 12V</text>
    
    <!-- Bornes -->
    <circle cx="50" cy="75" r="14" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <text x="50" y="80" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">-</text>
    <text x="50" y="108" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">GND (Masa)</text>

    <circle cx="150" cy="75" r="14" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>
    <text x="150" y="80" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">+</text>
    <text x="150" y="108" font-size="11" font-weight="bold" fill="#f87171" text-anchor="middle">+12V DC</text>

    <text x="100" y="135" font-size="11" fill="#cbd5e1" text-anchor="middle">LiFePO4 / AGM / Gel</text>
    <text x="100" y="150" font-size="10" fill="#64748b" text-anchor="middle">(Panel Solar + Controlador)</text>
  </g>

  <!-- 2. CONVERSOR STEP-DOWN -->
  <g transform="translate(280, 180)">
    <rect x="0" y="0" width="200" height="160" rx="8" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
    <rect x="0" y="0" width="200" height="35" rx="8" fill="#0369a1"/>
    <text x="100" y="23" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">⚡ STEP-DOWN (12V A 5V)</text>
    
    <!-- Bornes Entrada -->
    <text x="50" y="60" font-size="10" font-weight="bold" fill="#e0f2fe" text-anchor="middle">ENTRADA 12V</text>
    <circle cx="35" cy="85" r="9" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="35" y="110" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">IN -</text>

    <circle cx="65" cy="85" r="9" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"/>
    <text x="65" y="110" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">IN +</text>

    <!-- Bornes Salida -->
    <text x="150" y="60" font-size="10" font-weight="bold" fill="#e0f2fe" text-anchor="middle">SALIDA 5.1V</text>
    <circle cx="135" cy="85" r="9" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="135" y="110" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">GND</text>

    <circle cx="165" cy="85" r="9" fill="#ea580c" stroke="#ffffff" stroke-width="1.5"/>
    <text x="165" y="110" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">5.1V</text>

    <text x="100" y="145" font-size="10" fill="#e0f2fe" text-anchor="middle">LM2596 / MP1584 (3A)</text>
  </g>

  <!-- ==================== CÓDIGO DE COLORES (BOTTOM LEFT) ==================== -->
  <g transform="translate(40, 365)">
    <rect x="0" y="0" width="440" height="715" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="440" height="38" rx="10" fill="#334155"/>
    <text x="220" y="24" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">📋 CÓDIGO DE COLORES Y ASIGNACIÓN DE PINES</text>

    <!-- Item 1 -->
    <g transform="translate(20, 65)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#b91c1c" stroke-width="4"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Rojo Grueso: +12V DC Positivo Batería (a VIN+)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Alimenta el sensor de medición de corriente en lado alto.</text>
    </g>

    <!-- Item 2 -->
    <g transform="translate(20, 115)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#dc2626" stroke-width="4"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Rojo Normal: 12V Conmutado (VIN- a IN+ Step-Down)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Entrega energía al regulador tras pasar por la resistencia shunt.</text>
    </g>

    <!-- Item 3 -->
    <g transform="translate(20, 165)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#ea580c" stroke-width="3.5"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Naranja: +5.1V DC Regulado (OUT+ a Pin 2 de Pi Zero)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Alimentación principal del microcomputador y RNode LoRa.</text>
    </g>

    <!-- Item 4 -->
    <g transform="translate(20, 215)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#e11d48" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Rojo Fino: +3.3V DC Lógica (Pin 1 a VCC de Sensores)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Alimentación de 3.3V para INA219, BME280 y RTC DS3231.</text>
    </g>

    <!-- Item 5 -->
    <g transform="translate(20, 265)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#0f172a" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Negro: Tierra Común (GND - Pin 6 y Masa General)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Referencia de 0V unificada para todo el sistema.</text>
    </g>

    <!-- Item 6 -->
    <g transform="translate(20, 315)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#0284c7" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Azul: Datos I2C - SDA (Pin 3 / GPIO 2 en paralelo)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Línea bidireccional de datos para los 3 módulos I2C.</text>
    </g>

    <!-- Item 7 -->
    <g transform="translate(20, 365)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#059669" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Verde: Reloj I2C - SCL (Pin 5 / GPIO 3 en paralelo)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Señal de sincronismo para los 3 módulos I2C.</text>
    </g>

    <!-- Item 8 -->
    <g transform="translate(20, 415)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#8b5cf6" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Morado: UART TX SBC (Pin 8 / GPIO 14 a RX RNode)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Transmisión de paquetes de radio hacia el módem.</text>
    </g>

    <!-- Item 9 -->
    <g transform="translate(20, 465)">
      <line x1="0" y1="0" x2="45" y2="0" stroke="#f59e0b" stroke-width="3"/>
      <text x="55" y="4" font-size="12" font-weight="bold" fill="#0f172a">Amarillo: UART RX SBC (Pin 10 / GPIO 15 de TX RNode)</text>
      <text x="55" y="20" font-size="11" fill="#64748b">Recepción de paquetes de radio desde el módem.</text>
    </g>

    <!-- Info Box -->
    <g transform="translate(15, 525)">
      <rect x="0" y="0" width="410" height="165" rx="8" fill="#e0f2fe" stroke="#38bdf8"/>
      <text x="15" y="24" font-size="12" font-weight="bold" fill="#0369a1">💡 Principio de Conexión en Paralelo I2C:</text>
      <text x="15" y="46" font-size="11" fill="#0c4a6e">• INA219 (0x40), BME280 (0x76) y DS3231 (0x68)</text>
      <text x="15" y="64" font-size="11" fill="#0c4a6e">  se conectan todos a los mismos 4 cables:</text>
      <text x="25" y="82" font-size="11" font-weight="bold" fill="#0369a1">  3.3V (Pin 1), GND (Pin 6), SDA (Pin 3), SCL (Pin 5)</text>
      <text x="15" y="104" font-size="11" fill="#0c4a6e">• El bus I2C distingue a cada sensor por su dirección única.</text>
      <text x="15" y="122" font-size="11" fill="#0c4a6e">• RNode LoRa opera en bus UART serie (Pines 8 y 10).</text>
      <text x="15" y="142" font-size="11" font-weight="bold" fill="#0369a1">✓ Cero conflictos de pines y máxima estabilidad.</text>
    </g>
  </g>

  <!-- ==================== WIRING BUS TRACES (UNDERNEATH) ==================== -->

  <!-- 1. Bat+ (190, 255) to INA219 VIN+ (1380, 290) via top trace Y=130 -->
  <path d="M 190 255 L 190 130 L 1380 130 L 1380 280" fill="none" stroke="#b91c1c" stroke-width="4"/>

  <!-- 2. INA219 VIN- (1380, 320) to Step-Down IN+ (345, 265) via bottom trace Y=350 -->
  <path d="M 1380 320 L 1380 355 L 345 355 L 345 265" fill="none" stroke="#dc2626" stroke-width="4"/>

  <!-- 3. Bat- (90, 255) to Step-Down IN- (315, 265) -->
  <path d="M 90 255 L 90 300 L 315 300 L 315 265" fill="none" stroke="#0f172a" stroke-width="4"/>

  <!-- 4. Step-Down 5.1V OUT+ (445, 265) to Pi Zero Pin 2 (700, 280) & RNode 5V (1540, 340) via Y=145 -->
  <path d="M 445 265 L 445 145 L 700 145 L 700 270" fill="none" stroke="#ea580c" stroke-width="3.5"/>
  <path d="M 700 145 L 1540 145 L 1540 330" fill="none" stroke="#ea580c" stroke-width="3" stroke-dasharray="5,4"/>

  <!-- 5. Step-Down GND (415, 265) to System GND (Common Rail) via Y=160 -->
  <path d="M 415 265 L 415 160 L 700 160 L 700 340" fill="none" stroke="#0f172a" stroke-width="3.5"/>

  <!-- I2C SHARED VERTICAL RAILS (Between Pi Zero and I2C Modules) -->
  <!-- 3.3V Rail (X=860) from Pin 1 (650, 280) -->
  <path d="M 650 280 L 860 280 L 860 1000" fill="none" stroke="#e11d48" stroke-width="3"/>
  <circle cx="860" cy="280" r="4" fill="#e11d48"/>
  <path d="M 860 280 L 1070 280" fill="none" stroke="#e11d48" stroke-width="3"/> <!-- to INA219 VCC -->
  <circle cx="860" cy="540" r="4" fill="#e11d48"/>
  <path d="M 860 540 L 1070 540" fill="none" stroke="#e11d48" stroke-width="3"/> <!-- to BME280 VCC -->
  <circle cx="860" cy="800" r="4" fill="#e11d48"/>
  <path d="M 860 800 L 1070 800" fill="none" stroke="#e11d48" stroke-width="3"/> <!-- to DS3231 VCC -->

  <!-- GND Rail (X=890) from Pin 6 (700, 340) -->
  <path d="M 700 340 L 890 340 L 890 1000" fill="none" stroke="#0f172a" stroke-width="3"/>
  <circle cx="890" cy="310" r="4" fill="#0f172a"/>
  <path d="M 890 310 L 1070 310" fill="none" stroke="#0f172a" stroke-width="3"/> <!-- to INA219 GND -->
  <circle cx="890" cy="570" r="4" fill="#0f172a"/>
  <path d="M 890 570 L 1070 570" fill="none" stroke="#0f172a" stroke-width="3"/> <!-- to BME280 GND -->
  <circle cx="890" cy="830" r="4" fill="#0f172a"/>
  <path d="M 890 830 L 1070 830" fill="none" stroke="#0f172a" stroke-width="3"/> <!-- to DS3231 GND -->
  <!-- GND to RNode -->
  <path d="M 890 340 L 890 170 L 1570 170 L 1570 330" fill="none" stroke="#0f172a" stroke-width="3"/>

  <!-- SDA Rail (X=920) from Pin 3 (650, 310) -->
  <path d="M 650 310 L 920 310 L 920 1000" fill="none" stroke="#0284c7" stroke-width="3"/>
  <circle cx="920" cy="340" r="4" fill="#0284c7"/>
  <path d="M 920 340 L 1070 340" fill="none" stroke="#0284c7" stroke-width="3"/> <!-- to INA219 SDA -->
  <circle cx="920" cy="600" r="4" fill="#0284c7"/>
  <path d="M 920 600 L 1070 600" fill="none" stroke="#0284c7" stroke-width="3"/> <!-- to BME280 SDA -->
  <circle cx="920" cy="860" r="4" fill="#0284c7"/>
  <path d="M 920 860 L 1070 860" fill="none" stroke="#0284c7" stroke-width="3"/> <!-- to DS3231 SDA -->

  <!-- SCL Rail (X=950) from Pin 5 (650, 340) -->
  <path d="M 650 340 L 950 340 L 950 1000" fill="none" stroke="#059669" stroke-width="3"/>
  <circle cx="950" cy="370" r="4" fill="#059669"/>
  <path d="M 950 370 L 1070 370" fill="none" stroke="#059669" stroke-width="3"/> <!-- to INA219 SCL -->
  <circle cx="950" cy="630" r="4" fill="#059669"/>
  <path d="M 950 630 L 1070 630" fill="none" stroke="#059669" stroke-width="3"/> <!-- to BME280 SCL -->
  <circle cx="950" cy="890" r="4" fill="#059669"/>
  <path d="M 950 890 L 1070 890" fill="none" stroke="#059669" stroke-width="3"/> <!-- to DS3231 SCL -->

  <!-- UART SERIAL LINES to RNode -->
  <!-- RPi Pin 8 (TX / GPIO 14) (700, 370) to RNode RX (1600, 340) via Y=185 -->
  <path d="M 700 370 L 780 370 L 780 185 L 1600 185 L 1600 330" fill="none" stroke="#8b5cf6" stroke-width="3"/>
  <!-- RPi Pin 10 (RX / GPIO 15) (700, 400) to RNode TX (1630, 340) via Y=200 -->
  <path d="M 700 400 L 760 400 L 760 200 L 1630 200 L 1630 330" fill="none" stroke="#f59e0b" stroke-width="3"/>

  <!-- ==================== PLACA CENTRAL: RASPBERRY PI ZERO W ==================== -->
  <g transform="translate(530, 180)">
    <!-- Board Outline -->
    <rect x="0" y="0" width="240" height="900" rx="16" fill="#15803d" stroke="#166534" stroke-width="2.5"/>
    
    <!-- Header Title -->
    <rect x="0" y="0" width="240" height="42" rx="16" fill="#166534"/>
    <text x="120" y="26" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">RASPBERRY PI ZERO W</text>

    <!-- SoC & ICs -->
    <rect x="25" y="480" width="80" height="80" rx="4" fill="#1e293b" stroke="#334155"/>
    <text x="65" y="520" font-size="11" font-weight="bold" fill="#cbd5e1" text-anchor="middle">SoC BCM2835</text>
    <text x="65" y="538" font-size="9" fill="#94a3b8" text-anchor="middle">1GHz / 512MB</text>

    <rect x="25" y="730" width="60" height="50" rx="4" fill="#cbd5e1"/>
    <text x="55" y="760" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">MicroSD</text>

    <!-- 40 Pin Header Box -->
    <rect x="110" y="60" width="80" height="810" rx="6" fill="#0f172a"/>
    <text x="150" y="80" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">GPIO (40 PIN)</text>

    <!-- PINS REPRESENTATION (Pin 1 to 40) -->
    <!-- Row 1: Pin 1 (3.3V) & Pin 2 (5V) -->
    <circle cx="120" cy="100" r="7" fill="#e11d48"/>
    <text x="105" y="104" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="end">Pin 1 (3.3V)</text>
    
    <circle cx="170" cy="100" r="7" fill="#ea580c"/>
    <text x="185" y="104" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="start">Pin 2 (5V)</text>

    <!-- Row 2: Pin 3 (SDA) & Pin 4 (5V) -->
    <circle cx="120" cy="130" r="7" fill="#0284c7"/>
    <text x="105" y="134" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="end">Pin 3 (SDA)</text>
    
    <circle cx="170" cy="130" r="5" fill="#475569"/>
    <text x="185" y="134" font-size="9" fill="#94a3b8" text-anchor="start">Pin 4</text>

    <!-- Row 3: Pin 5 (SCL) & Pin 6 (GND) -->
    <circle cx="120" cy="160" r="7" fill="#059669"/>
    <text x="105" y="164" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="end">Pin 5 (SCL)</text>
    
    <circle cx="170" cy="160" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
    <text x="185" y="164" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="start">Pin 6 (GND)</text>

    <!-- Row 4: Pin 7 (GPIO4) & Pin 8 (TXD) -->
    <circle cx="120" cy="190" r="5" fill="#475569"/>
    <text x="105" y="194" font-size="9" fill="#94a3b8" text-anchor="end">Pin 7</text>
    
    <circle cx="170" cy="190" r="7" fill="#8b5cf6"/>
    <text x="185" y="194" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="start">Pin 8 (TX)</text>

    <!-- Row 5: Pin 9 (GND) & Pin 10 (RXD) -->
    <circle cx="120" cy="220" r="5" fill="#475569"/>
    <text x="105" y="224" font-size="9" fill="#94a3b8" text-anchor="end">Pin 9</text>
    
    <circle cx="170" cy="220" r="7" fill="#f59e0b"/>
    <text x="185" y="224" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="start">Pin 10 (RX)</text>

    <!-- Remaining Pins (Unused / Dark Gray) -->
    <g fill="#334155">
      <circle cx="120" cy="250" r="5"/><circle cx="170" cy="250" r="5"/>
      <circle cx="120" cy="280" r="5"/><circle cx="170" cy="280" r="5"/>
      <circle cx="120" cy="310" r="5"/><circle cx="170" cy="310" r="5"/>
      <circle cx="120" cy="340" r="5"/><circle cx="170" cy="340" r="5"/>
      <circle cx="120" cy="370" r="5"/><circle cx="170" cy="370" r="5"/>
      <circle cx="120" cy="400" r="5"/><circle cx="170" cy="400" r="5"/>
      <circle cx="120" cy="430" r="5"/><circle cx="170" cy="430" r="5"/>
      <circle cx="120" cy="460" r="5"/><circle cx="170" cy="460" r="5"/>
      <circle cx="120" cy="490" r="5"/><circle cx="170" cy="490" r="5"/>
      <circle cx="120" cy="520" r="5"/><circle cx="170" cy="520" r="5"/>
      <circle cx="120" cy="550" r="5"/><circle cx="170" cy="550" r="5"/>
      <circle cx="120" cy="580" r="5"/><circle cx="170" cy="580" r="5"/>
      <circle cx="120" cy="610" r="5"/><circle cx="170" cy="610" r="5"/>
      <circle cx="120" cy="640" r="5"/><circle cx="170" cy="640" r="5"/>
      <circle cx="120" cy="670" r="5"/><circle cx="170" cy="670" r="5"/>
      <circle cx="120" cy="700" r="5"/><circle cx="170" cy="700" r="5"/>
      <circle cx="120" cy="730" r="5"/><circle cx="170" cy="730" r="5"/>
      <circle cx="120" cy="760" r="5"/><circle cx="170" cy="760" r="5"/>
      <circle cx="120" cy="790" r="5"/><circle cx="170" cy="790" r="5"/>
      <circle cx="120" cy="820" r="5"/><circle cx="170" cy="820" r="5"/>
    </g>
  </g>

  <!-- ==================== I2C BREAKOUT MODULES (CENTER RIGHT) ==================== -->
  <g transform="translate(1000, 180)">
    <!-- Container Outline -->
    <rect x="0" y="0" width="460" height="900" rx="12" fill="#ffffff" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6,4"/>
    <text x="230" y="30" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">BUS I2C COMPARTIDO EN PARALELO</text>
    <text x="230" y="48" font-size="11" fill="#64748b" text-anchor="middle">Líneas comunes: 3.3V (Pin 1) | GND (Pin 6) | SDA (Pin 3) | SCL (Pin 5)</text>

    <!-- MODULE 1: INA219 (I2C 0x40) -->
    <g transform="translate(20, 65)">
      <rect x="0" y="0" width="420" height="230" rx="8" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
      <rect x="0" y="0" width="420" height="34" rx="8" fill="#172554"/>
      <text x="210" y="23" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🔋 SENSOR DE BATERÍA SOLAR: INA219 (I2C: 0x40)</text>

      <!-- Logic Pins (Left) -->
      <g transform="translate(15, 45)">
        <circle cx="35" cy="0" r="7" fill="#e11d48"/>
        <text x="50" y="4" font-size="11" font-weight="bold" fill="#ffffff">VCC (3.3V)</text>

        <circle cx="35" cy="30" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
        <text x="50" y="34" font-size="11" font-weight="bold" fill="#ffffff">GND (Tierra)</text>

        <circle cx="35" cy="60" r="7" fill="#0284c7"/>
        <text x="50" y="64" font-size="11" font-weight="bold" fill="#ffffff">SDA (Datos)</text>

        <circle cx="35" cy="90" r="7" fill="#059669"/>
        <text x="50" y="94" font-size="11" font-weight="bold" fill="#ffffff">SCL (Reloj)</text>
      </g>

      <!-- Shunt Bornera (Right) -->
      <g transform="translate(240, 50)">
        <rect x="0" y="0" width="165" height="125" rx="6" fill="#0f172a" stroke="#38bdf8"/>
        <text x="82" y="24" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">BORNERA DE POTENCIA</text>
        
        <circle cx="30" cy="60" r="8" fill="#b91c1c"/>
        <text x="45" y="64" font-size="11" font-weight="bold" fill="#ffffff">VIN +</text>
        <text x="45" y="78" font-size="9" fill="#cbd5e1">(De Batería +12V)</text>

        <circle cx="30" cy="100" r="8" fill="#dc2626"/>
        <text x="45" y="104" font-size="11" font-weight="bold" fill="#ffffff">VIN -</text>
        <text x="45" y="118" font-size="9" fill="#cbd5e1">(A Step-Down IN+)</text>
      </g>
      <text x="210" y="208" font-size="11" fill="#93c5fd" text-anchor="middle">Mide Voltaje real de Batería (0-26V DC) y Consumo en mA</text>
    </g>

    <!-- MODULE 2: BME280 / BMP280 (I2C 0x76 / 0x77) -->
    <g transform="translate(20, 325)">
      <rect x="0" y="0" width="420" height="230" rx="8" fill="#6b21a8" stroke="#7e22ce" stroke-width="2"/>
      <rect x="0" y="0" width="420" height="34" rx="8" fill="#3b0764"/>
      <text x="210" y="23" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🌦️ SENSOR AMBIENTAL Y CLIMA: BME280 (I2C: 0x76 / 0x77)</text>

      <!-- Logic Pins (Left) -->
      <g transform="translate(15, 45)">
        <circle cx="35" cy="0" r="7" fill="#e11d48"/>
        <text x="50" y="4" font-size="11" font-weight="bold" fill="#ffffff">VIN / VCC (3.3V)</text>

        <circle cx="35" cy="30" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
        <text x="50" y="34" font-size="11" font-weight="bold" fill="#ffffff">GND (Tierra)</text>

        <circle cx="35" cy="60" r="7" fill="#0284c7"/>
        <text x="50" y="64" font-size="11" font-weight="bold" fill="#ffffff">SDA / SDI (Datos)</text>

        <circle cx="35" cy="90" r="7" fill="#059669"/>
        <text x="50" y="94" font-size="11" font-weight="bold" fill="#ffffff">SCL / SCK (Reloj)</text>
      </g>

      <!-- Feature Description Box -->
      <g transform="translate(210, 50)">
        <rect x="0" y="0" width="195" height="125" rx="6" fill="#3b0764" stroke="#c084fc"/>
        <text x="97" y="26" font-size="11" font-weight="bold" fill="#f3e8ff" text-anchor="middle">MÉTRICAS REPORTADAS</text>
        <text x="15" y="54" font-size="10" fill="#e9d5ff">• Presión Barométrica (hPa)</text>
        <text x="15" y="76" font-size="10" fill="#e9d5ff">• Temperatura Ambiental (°C)</text>
        <text x="15" y="98" font-size="10" fill="#e9d5ff">• Alerta Temprana de Tormentas</text>
      </g>
      <text x="210" y="208" font-size="11" fill="#e9d5ff" text-anchor="middle">Conectado en paralelo a los mismos 4 hilos del bus I2C</text>
    </g>

    <!-- MODULE 3: DS3231 RTC (I2C 0x68) -->
    <g transform="translate(20, 585)">
      <rect x="0" y="0" width="420" height="230" rx="8" fill="#0f766e" stroke="#115e59" stroke-width="2"/>
      <rect x="0" y="0" width="420" height="34" rx="8" fill="#134e4a"/>
      <text x="210" y="23" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🕒 RELOJ OFFLINE POR HARDWARE: DS3231 (I2C: 0x68)</text>

      <!-- Logic Pins (Left) -->
      <g transform="translate(15, 45)">
        <circle cx="35" cy="0" r="7" fill="#e11d48"/>
        <text x="50" y="4" font-size="11" font-weight="bold" fill="#ffffff">VCC (3.3V)</text>

        <circle cx="35" cy="30" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
        <text x="50" y="34" font-size="11" font-weight="bold" fill="#ffffff">GND (Tierra)</text>

        <circle cx="35" cy="60" r="7" fill="#0284c7"/>
        <text x="50" y="64" font-size="11" font-weight="bold" fill="#ffffff">SDA (Datos)</text>

        <circle cx="35" cy="90" r="7" fill="#059669"/>
        <text x="50" y="94" font-size="11" font-weight="bold" fill="#ffffff">SCL (Reloj)</text>
      </g>

      <!-- Coin Cell Battery Representation -->
      <g transform="translate(240, 50)">
        <rect x="0" y="0" width="165" height="125" rx="6" fill="#134e4a" stroke="#5eead4"/>
        <circle cx="45" cy="62" r="30" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
        <text x="45" y="58" font-size="10" font-weight="bold" fill="#1e293b" text-anchor="middle">CR2032</text>
        <text x="45" y="74" font-size="9" fill="#64748b" text-anchor="middle">Pila 3V</text>
        <text x="120" y="52" font-size="11" font-weight="bold" fill="#ccfbf1" text-anchor="middle">RELOJ RTC</text>
        <text x="120" y="72" font-size="9" fill="#99f6e4" text-anchor="middle">Sincroniza hora</text>
        <text x="120" y="88" font-size="9" fill="#99f6e4" text-anchor="middle">sin Internet</text>
      </g>
      <text x="210" y="208" font-size="11" fill="#ccfbf1" text-anchor="middle">Mantiene marcas de tiempo de mensajes LXMF precisas en cerros aislados</text>
    </g>
  </g>

  <!-- ==================== RNODE LORA TRANSCEIVER (FAR RIGHT) ==================== -->
  <g transform="translate(1500, 180)">
    <rect x="0" y="0" width="220" height="520" rx="12" fill="#1e293b" stroke="#475569" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="35" rx="12" fill="#0f172a"/>
    <text x="110" y="23" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">📡 RNODE LORA</text>

    <!-- Antenna at TOP -->
    <g transform="translate(110, 45)">
      <rect x="-10" y="0" width="20" height="25" fill="#cbd5e1" stroke="#475569"/>
      <line x1="0" y1="25" x2="0" y2="70" stroke="#38bdf8" stroke-width="4"/>
      <polygon points="-12,70 12,70 0,90" fill="#38bdf8"/>
      <text x="0" y="105" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">ANTENA RF</text>
    </g>

    <!-- Connectors -->
    <g transform="translate(20, 160)">
      <circle cx="10" cy="15" r="7" fill="#ea580c"/>
      <text x="25" y="19" font-size="11" font-weight="bold" fill="#ffffff">5V / VCC (Pwr)</text>

      <circle cx="10" cy="45" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
      <text x="25" y="49" font-size="11" font-weight="bold" fill="#ffffff">GND (Tierra)</text>

      <circle cx="10" cy="75" r="7" fill="#8b5cf6"/>
      <text x="25" y="79" font-size="11" font-weight="bold" fill="#ffffff">RX (a TX Pin 8)</text>

      <circle cx="10" cy="105" r="7" fill="#f59e0b"/>
      <text x="25" y="109" font-size="11" font-weight="bold" fill="#ffffff">TX (a RX Pin 10)</text>
    </g>

    <!-- Radio Chip Box -->
    <g transform="translate(15, 300)">
      <rect x="0" y="0" width="190" height="110" rx="6" fill="#0f172a" stroke="#64748b"/>
      <text x="95" y="28" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">ESP32 / T-Beam / Heltec</text>
      <text x="95" y="50" font-size="11" fill="#ffffff" text-anchor="middle">SX1262 / SX1276</text>
      <text x="95" y="70" font-size="10" fill="#94a3b8" text-anchor="middle">915 / 868 / 433 MHz LoRa</text>
      <text x="95" y="92" font-size="10" fill="#cbd5e1" text-anchor="middle">Firmware RNode (KISS)</text>
    </g>

    <text x="110" y="450" font-size="11" fill="#cbd5e1" text-anchor="middle">Conexión UART Serie</text>
    <text x="110" y="470" font-size="10" fill="#94a3b8" text-anchor="middle">(o Cable Micro-USB OTG)</text>
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

    print("Renderizando SVG con Chromium headless (1760x1120)...")
    subprocess.run([
        "chromium", "--headless", "--disable-gpu",
        f"--screenshot={png_file}",
        "--window-size=1760,1120",
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
