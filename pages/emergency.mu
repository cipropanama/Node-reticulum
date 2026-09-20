# == MENSAJERÍA Y PROTOCOLO DE EMERGENCIA ==
`!C`_Buzón de Almacenamiento y Reenvío (Store-and-Forward)_`!c`
`!C`[Volver a la Portada](index.mu)`!c`

--------------------------------------------------------------------------------

`!Fd22`### ⚠️ INSTRUCCIONES EN CASO DE EMERGENCIA`!f`
1. *Si la persona destinataria no está conectada:*
   Este nodo actúa como **Nodo de Propagación LXMF** activo. Cuando envíes un mensaje mediante Sideband, NomadNet o MeshChat dirigido a un usuario desconectado, el nodo lo guardará de forma segura y encriptada en su almacén local.

2. *Despacho Automático:*
   Tan pronto como el destinatario se conecte o anuncie su presencia en la red de malla (directamente o a través de otro repetidor), el nodo despachará inmediatamente el mensaje en cola.

3. *Canales de Escucha y Frecuencias Locales:*
   - Frecuencia LoRa Primaria: `{LORA_FREQ}` MHz
   - Ancho de Banda (BW): `{LORA_BW}` kHz | Factor Dispersión (SF): `{LORA_SF}`
   - Canal de Difusión LXMF: `Emergencias y Rescate`

--------------------------------------------------------------------------------

`!F28b`### 📋 FORMATO RECOMENDADO PARA MENSAJES DE AUXILIO`!f`
Para facilitar el procesamiento de auxilio, incluye siempre:
- *QUIÉN:* Nombre de la persona o grupo afectado.
- *DÓNDE:* Ubicación geográfica o coordenadas aproximadas.
- *QUÉ:* Naturaleza de la emergencia (médica, rescate, suministros).
- *CÓMO CONTACTAR:* ID de Reticulum o frecuencia de escucha.

--------------------------------------------------------------------------------
`!C`[← Volver al Inicio](index.mu)`!c`
