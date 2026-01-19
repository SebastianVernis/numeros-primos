#!/bin/bash
# Preparar proyecto para despliegue limpio

echo "🧹 Preparando proyecto para despliegue..."

# Directorio base
BASE_DIR="/home/sebastianvernis/Desarrollo/Numeros_Primos"
cd "$BASE_DIR"

# Crear directorio de despliegue limpio
DEPLOY_DIR="$BASE_DIR/deploy_clean"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

echo "📦 Copiando archivos esenciales..."

# Copiar archivos principales
cp -v vercel.json "$DEPLOY_DIR/"
cp -v requirements.txt "$DEPLOY_DIR/"
cp -v README_DEPLOY.md "$DEPLOY_DIR/README.md"
cp -v .gitignore "$DEPLOY_DIR/"

# Copiar API
mkdir -p "$DEPLOY_DIR/api"
cp -v api/index.py "$DEPLOY_DIR/api/"

# Copiar solo algunos mapas de muestra (para no exceder límites)
echo "📊 Copiando mapas de muestra..."
mkdir -p "$DEPLOY_DIR/static_maps_hires"

# Copiar índice y 50 mapas de muestra
cp -v static_maps_hires/index.html "$DEPLOY_DIR/static_maps_hires/" 2>/dev/null || echo "No index.html"
ls static_maps_hires/map_*.html 2>/dev/null | head -50 | xargs -I {} cp {} "$DEPLOY_DIR/static_maps_hires/"
ls static_maps_hires/data_*.json 2>/dev/null | head -50 | xargs -I {} cp {} "$DEPLOY_DIR/static_maps_hires/"

# Crear un índice simple si no existe
if [ ! -f "$DEPLOY_DIR/static_maps_hires/index.html" ]; then
    echo "<!DOCTYPE html><html><head><title>Mapas</title></head><body><h1>Mapas de Números Primos</h1></body></html>" > "$DEPLOY_DIR/static_maps_hires/index.html"
fi

# Verificar tamaño
echo "📏 Tamaño del directorio de despliegue:"
du -sh "$DEPLOY_DIR"

echo "✅ Proyecto preparado en: $DEPLOY_DIR"
echo ""
echo "📝 Próximos pasos:"
echo "1. cd $DEPLOY_DIR"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial deployment'"
echo "5. vercel (o push a GitHub y conectar con Vercel)"