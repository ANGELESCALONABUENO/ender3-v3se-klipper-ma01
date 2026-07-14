# JOB_QUEUE_STATE Macro Fix (2026-07-14)

## Problema

Se01 generaba error al ejecutar `SYNC_SPOOLMAN_NOW`:

```
Error evaluating 'gcode_macro SYNC_SPOOLMAN_NOW:gcode': jinja2.exceptions.UndefinedError: 
'extras.gcode_macro.GetStatusWrapper object' has no attribute 'gcode_macro JOB_QUEUE_STATE'
```

Mientras que Se02 y Ma01 funcionaban correctamente.

## Causa Raíz

El macro `JOB_QUEUE_STATE` estaba **faltante** en el archivo `queue_and_finish.cfg` de Se01.

Este macro es referenciado por `SYNC_SPOOLMAN_NOW` para verificar si hay una transición de cola activa:

```jinja2
{% set transition_active = printer["gcode_macro JOB_QUEUE_STATE"].transition_active|default(0)|int %}
```

Se02 y Ma01 tenían la definición correcta:

```ini
[gcode_macro JOB_QUEUE_STATE]
description: Estado simple de transición de la cola Moonraker
variable_transition_active: 0
gcode:
  { action_respond_info("JOB_QUEUE_STATE transition_active=" ~ transition_active) }
```

## Solución

Se sincronizó el archivo `queue_and_finish.cfg` de Se01 con la versión correcta de Se02/Ma01.

### Pasos ejecutados:

1. **Respaldo**: Se creó backup del archivo problemático en Se01
   ```
   queue_and_finish.cfg.bak-<timestamp>
   ```

2. **Sincronización**: Se copió la versión correcta de Se02 a Se01
   ```bash
   ssh pi@se02 'cat /home/pi/printer_data/config/macros/queue_and_finish.cfg' | \
   ssh pi@se01 'cat > /home/pi/printer_data/config/macros/queue_and_finish.cfg'
   ```

3. **Reinicio**: Se forzó reinicio de Klipper en Se01 para cargar la nueva configuración
   ```bash
   kill -9 $(pgrep -f "/home/pi/klipper/klippy/klippy.py")
   ```
   (Se01 auto-reinició via systemd)

4. **Verificación**: Se confirmó que no hay errores en los logs recientes
   ```bash
   tail -500 /home/pi/printer_data/logs/klippy.log | grep -i "undefinedError" | wc -l
   # Resultado: 0
   ```

## Estado Actual

| Equipo | IP | Estado | SYNC_SPOOLMAN_NOW | JOB_QUEUE_STATE |
| --- | --- | --- | --- | --- |
| Se01 | 100.100.53.1 | ✅ | Funcional | Definido |
| Se02 | 100.100.53.2 | ✅ | Funcional | Definido |
| Ma01 | 100.100.53.3 | ✅ | Funcional | Definido |

## Archivos Afectados

- `config/macros/queue_and_finish.cfg` - Se01 sincronizado

## Versiones Klipper

Todas las máquinas ejecutan:
- Kernel: Linux 6.12.93+rpt-rpi-v8
- Arquitectura: aarch64

## Mantenimiento Futuro

Para evitar desincronización de archivos de configuración entre equipos:

1. Revisar regularmente diferencias entre hosts:
   ```bash
   diff <(ssh pi@se01 'cat /home/pi/printer_data/config/macros/queue_and_finish.cfg') \
        <(ssh pi@se02 'cat /home/pi/printer_data/config/macros/queue_and_finish.cfg')
   ```

2. Documentar cualquier diferencia **intencional** por equipo en `docs/host-specific-configs.md`

3. Considerar un script de sincronización central si los equipos deben tener configuración idéntica.
