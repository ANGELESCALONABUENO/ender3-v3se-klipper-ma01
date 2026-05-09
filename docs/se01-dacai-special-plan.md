# SE01 - Plan individual (caso especial DACAI)

## Contexto

SE01 tiene instalada una pantalla DACAI (familia Ender 3 V2) y actualmente el host usa fork de Klipper con `prtouch` + `e3v3se_display`.

Esto genera un caso especial:

- `PRTOUCH_PROBE_ZOFFSET` se debe conservar (depende de `prtouch.py`, no de la pantalla).
- La UI de pantalla requiere ruta de migracion distinta (stack DWIN) por incompatibilidad de protocolo de display.

## Estado actual (2026-05-09)

- Semana 1 ejecutada para SE01: macro `EXTRAER_MATERIAL` disponible en Mainsail.
- En SE01 no se publica en pantalla por ahora.
- Se conserva flujo de calibracion por `PRTOUCH_PROBE_ZOFFSET`.

## Alcance inmediato (solo plan de display)

1. Mantener fork actual y no tocar bloques `prtouch`.
2. Migrar capa de pantalla a stack DWIN para DACAI.
3. Re-mapear acciones de pantalla para llamar macros activas (`EXTRAER_MATERIAL`, `calibrar_punta`, etc.).
4. Validar operacion UI sin afectar el sensor de presion.

## Nota operativa

El cambio de display de SE01 no bloquea la Semana 1 de macros: la extraccion ya se puede ejecutar desde Mainsail mientras se completa la migracion de pantalla.
