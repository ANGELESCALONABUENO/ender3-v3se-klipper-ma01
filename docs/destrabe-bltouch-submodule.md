# DESTRABAR_BLTOUCH - Sincronización desde Submódulo Git

## Descripción

El macro `DESTRABAR_BLTOUCH` ahora está vinculado mediante un **submódulo de Git** que apunta al repositorio dedicado:

- **Repositorio del macro**: https://github.com/ANGELESCALONABUENO/ender3-v3se-crtouch-destrabe-macro
- **Ubicación del submódulo**: `macros/destrabe-bltouch-src/`
- **Macro en uso**: `config/macros/DESTRABAR_BLTOUCH.cfg`

## Clonar con submódulos

Cuando clonas este repositorio, necesitas inicializar los submódulos:

```bash
git clone https://github.com/ANGELESCALONABUENO/ender3-v3se-klipper-inmateriis.git
cd ender3-v3se-klipper-inmateriis
git submodule init
git submodule update
```

O en un solo comando:

```bash
git clone --recurse-submodules https://github.com/ANGELESCALONABUENO/ender3-v3se-klipper-inmateriis.git
```

## Actualizar el macro

### Opción 1: Usar el script de sincronización (Recomendado)

```bash
./scripts/sync-destrabe-bltouch.sh
```

Este script:
- Verifica que el submódulo esté inicializado
- Copia la última versión desde `macros/destrabe-bltouch-src/DESTRABAR_BLTOUCH.cfg`
- A `config/macros/DESTRABAR_BLTOUCH.cfg`
- Muestra el SHA del submódulo

### Opción 2: Actualizar submódulo manualmente

```bash
# Ir al directorio del submódulo
cd macros/destrabe-bltouch-src

# Descargar los últimos cambios del repositorio del macro
git fetch origin
git checkout origin/master

# Volver al directorio raíz
cd ../..

# Ejecutar el script de sincronización
./scripts/sync-destrabe-bltouch.sh
```

### Opción 3: Actualizar desde el repositorio del macro

Si hay cambios en el repositorio del macro (`ender3-v3se-crtouch-destrabe-macro`), puedes pullear directamente:

```bash
# Actualizar el submódulo a la rama master más reciente
git submodule update --remote --merge

# Sincronizar el archivo de configuración
./scripts/sync-destrabe-bltouch.sh
```

## Verificar estado del submódulo

```bash
# Ver estado de todos los submódulos
git submodule status

# Salida esperada:
# 1a2b3c4d5e6f... macros/destrabe-bltouch-src (heads/master)
```

## Actualizar a nivel de repositorio principal

Cuando sincronices el macro, Git detectará cambios. Commitea los cambios:

```bash
git add macros/destrabe-bltouch-src config/macros/DESTRABAR_BLTOUCH.cfg
git commit -m "chore: actualizar DESTRABAR_BLTOUCH desde submódulo"
git push origin master
```

## Flujo de actualización completo

```bash
# 1. Actualizar el submódulo a la rama remota más reciente
git submodule update --remote --merge

# 2. Ejecutar el script de sincronización
./scripts/sync-destrabe-bltouch.sh

# 3. Verificar cambios
git diff config/macros/DESTRABAR_BLTOUCH.cfg

# 4. Commitear cambios
git add -A
git commit -m "chore: actualizar DESTRABAR_BLTOUCH desde submódulo (SHA: ...)"
git push origin master
```

## Notas Importantes

- **No edites** `config/macros/DESTRABAR_BLTOUCH.cfg` directamente si quieres mantener sincronización.
- **Los cambios** deben hacerse en el repositorio dedicado (`ender3-v3se-crtouch-destrabe-macro`).
- **El script** puede ser ejecutado en CI/CD para automatizar la sincronización.
- **Los 3 equipos** (Se01, Se02, Ma01) pueden utilizar el macro sincronizado desde este repositorio.

## Troubleshooting

### Submódulo no actualizado

Si el submódulo no se actualizó automáticamente al hacer `git pull`:

```bash
git pull --recurse-submodules
```

O:

```bash
git submodule update --init --recursive
```

### Error: "No se encontró DESTRABAR_BLTOUCH.cfg"

El submódulo no está inicializado. Ejecuta:

```bash
git submodule init
git submodule update
```

### Conflictos al sincronizar

Si hay conflictos, revisa manualmente:

```bash
diff config/macros/DESTRABAR_BLTOUCH.cfg macros/destrabe-bltouch-src/DESTRABAR_BLTOUCH.cfg
```

Resuelve y ejecuta el script nuevamente.
