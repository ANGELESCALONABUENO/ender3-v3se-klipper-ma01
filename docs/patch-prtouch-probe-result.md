# Fix: `PRTOUCH_PROBE_ZOFFSET` internal error (`probe_result` is immutable)

## Síntoma
Al ejecutar `PRTOUCH_PROBE_ZOFFSET` (por ejemplo vía el macro `calibrar_punta`), Klipper entra en estado **shutdown** y muestra un error similar a:

- `Internal error on command:"PRTOUCH_PROBE_ZOFFSET"`
- `TypeError: 'probe_result' object does not support item assignment`

En los logs suele apuntar a:

- `/home/pi/klipper/klippy/extras/prtouch.py` cerca de la línea donde se hace `z_probe[2] = ...`

## Causa
En algunas versiones/entornos, `probe.run_single_probe(...)` devuelve un objeto tipo `probe_result` **inmutable**. El extra `prtouch.py` intenta modificarlo como si fuera una lista (`z_probe[2] = ...`), lo cual dispara el `TypeError`.

## Solución (parche)
En vez de asignar sobre `z_probe`, construir una lista mutable `[x, y, z]` y pasarla a `probe_calibrate_finalize(...)`.

Además, en algunos sistemas Klipper puede seguir ejecutando bytecode cacheado (`__pycache__/*.pyc`). Si el error persiste después del parche y un `FIRMWARE_RESTART`, borrar los `.pyc` y reiniciar el servicio de Klipper.

## Cómo aplicar en la Raspberry (se01/ma01/etc.)
1) Respaldar el archivo:

```bash
cp -a /home/pi/klipper/klippy/extras/prtouch.py \
  /home/pi/klipper/klippy/extras/prtouch.py.bak-$(date +%Y%m%d-%H%M%S)
```

2) Editar el bloque dentro de `cmd_PRTOUCH_PROBE_ZOFFSET`.

Recomendado (más robusto): convertir a lista mutable inmediatamente después de `run_single_probe(...)`.

Agregar justo después de obtener `z_probe`:

```py
z_probe = probe.run_single_probe(self.obj.probe, probe_gcmd)
# Klipper may return an immutable probe_result object. Convert to a
# mutable list immediately so downstream code can safely work with it.
z_probe = [z_probe[0], z_probe[1], z_probe[2]]
```

Reemplazar:

```py
z_probe[2] = homing_origin[2] + z_adjust - start_z_offset
self.probe_calibrate_finalize(z_probe)
```

Por:

```py
# Newer Klipper versions may return an immutable probe_result object
# from run_single_probe. Build a mutable [x, y, z] list for finalize.
z_probe_z = homing_origin[2] + z_adjust - start_z_offset
z_probe_pos = [z_probe[0], z_probe[1], z_probe_z]
self.probe_calibrate_finalize(z_probe_pos)
```

3) Reiniciar Klipper para cargar el cambio:

- Ejecutar `FIRMWARE_RESTART` desde Mainsail/Fluidd.

Si sigue fallando (o ves `nginx 504`/timeouts) después del reinicio normal, hacer un reinicio “duro” del servicio y limpiar caches:

```bash
sudo systemctl stop klipper
rm -f /home/pi/klipper/klippy/extras/__pycache__/prtouch*.pyc
rm -f /home/pi/klipper/klippy/extras/__pycache__/probe*.pyc
sudo systemctl start klipper
```

Luego ejecutar `FIRMWARE_RESTART` una vez y reintentar `PRTOUCH_PROBE_ZOFFSET`.

## Notas
- Este repo mantiene configs/macros; el archivo `prtouch.py` vive en la instalación de Klipper del host.
- Si usas KIAUH o actualizas Klipper, el archivo puede sobrescribirse y tendrás que reaplicar el parche.
