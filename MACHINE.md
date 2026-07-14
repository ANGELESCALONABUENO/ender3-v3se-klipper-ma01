# MA01 - MainsailOS Printer 01

**Máquina:** MA01 (MainsailOS)  
**IP Tailscale:** 100.100.53.3  
**Usuario SSH:** pi  
**Repositorio:** https://github.com/ANGELESCALONABUENO/ender3-v3se-klipper-ma01

## Configuración específica de MA01

- Puerto serie: /dev/ttyAMA0
- Sensor: BLTouch/CRTouch
- Motherboard: Creality 4.2.2 (STM32F103)
- Pantalla: Display integrado (si aplica)

## Actualizar configuración

```bash
# En MA01:
cd /home/pi/printer_data/config
git pull origin master
```

O vía webhook en Moonraker para actualizaciones automáticas.
