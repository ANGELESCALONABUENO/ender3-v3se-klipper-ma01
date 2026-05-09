# inMateriis - Planes futuros

## Produccion - Laboratorio de Prototipado

### Plan semanal de mejoras | Fecha: 2026-05-08

Plan semanal de mejoras para SE01, SE02 y MA01.

Enfoque actual: extraccion de material, `spoolman_active`, `calibrar_punta`, destrabar BLTouch y recuperacion controlada ante fallo de despliegue del probe.

#### Resumen de mejoras

| ID | Mejora | Prioridad | Estado |
| --- | --- | --- | --- |
| MJR-001 | Macro de extraccion y acceso en pantalla | Alta | Ejecutada (2026-05-09) |
| MJR-002 | Revision de `SPOOLMAN_ACTIVE` | Alta | Por iniciar |
| MJR-003 | Efectividad de `calibrar_punta` | Media | Por iniciar |
| MJR-004 | Mejora de `DESTRABAR_BLTOUCH` | Alta | Por iniciar |
| MJR-005 | Flujo para `BLTouch failed to deploy` | Alta | En analisis |

#### Semana 1

Macro de extraccion y acceso en pantalla:

- Implementado macro `EXTRAER_MATERIAL` en SE01, SE02 y MA01.
- Regla de temperatura aplicada: usa `SPOOLMAN_ACTIVE.nozzle_temp` al 70% para extraccion.
- Ejemplo: material a 220C -> extraccion a 154C.
- Publicado en display para SE02 y MA01 (slot `MACRO5`).
- En SE01 queda disponible por Mainsail (caso especial de pantalla DACAI; no se publica en display por ahora).
- Validacion operativa de 3 corridas por impresora queda pendiente de registro formal.

#### Plan individual SE01 (caso especial)

SE01 usa pantalla DACAI (familia Ender 3 V2), por lo que su camino de migracion de display es distinto.

- Ver plan individual: `docs/se01-dacai-special-plan.md`

#### Semana 2

Revision de `SPOOLMAN_ACTIVE`:

- Validar defaults y transiciones de synced.
- Verificar bloqueo de ventilador/temperatura.
- Completar 5 inicios de impresion consistentes.

#### Semana 3

Calibrar punta + destrabe:

- 3 corridas por impresora para `calibrar_punta`.
- Comparativo de primera capa.
- Ajustes de `DESTRABAR_BLTOUCH`.

#### Semana 4

Recuperacion semiautomatica BLTouch:

- Secuencia segura: destrabe, reintento, pausa confirmacion.
- Pruebas en pieza no critica.
- No continuar automatico sin validacion Z y probe.
