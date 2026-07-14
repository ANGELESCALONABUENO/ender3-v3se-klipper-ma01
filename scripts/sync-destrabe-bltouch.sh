#!/bin/bash
# Script para sincronizar DESTRABAR_BLTOUCH desde el submódulo
# Usage: ./scripts/sync-destrabe-bltouch.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUBMODULE_SRC="${REPO_ROOT}/macros/destrabe-bltouch-src"
CONFIG_DEST="${REPO_ROOT}/config/macros/DESTRABAR_BLTOUCH.cfg"

echo "🔄 Sincronizando DESTRABAR_BLTOUCH desde submódulo..."

# Verificar que el submódulo existe
if [ ! -d "$SUBMODULE_SRC" ]; then
    echo "❌ Error: Submódulo no encontrado en $SUBMODULE_SRC"
    echo "   Ejecuta: git submodule init && git submodule update"
    exit 1
fi

# Buscar el archivo del macro en el submódulo
MACRO_FILE=$(find "$SUBMODULE_SRC" -name "DESTRABAR_BLTOUCH.cfg" -o -name "*.cfg" | head -1)

if [ -z "$MACRO_FILE" ]; then
    echo "❌ Error: No se encontró DESTRABAR_BLTOUCH.cfg en el submódulo"
    exit 1
fi

echo "📋 Fuente: $MACRO_FILE"
echo "📍 Destino: $CONFIG_DEST"

# Copiar archivo
cp "$MACRO_FILE" "$CONFIG_DEST"

echo "✅ Sincronización completada"
echo "📝 SHA del submódulo: $(cd $SUBMODULE_SRC && git rev-parse HEAD)"
