# 🚀 Guía de Despliegue - Mapa de Números Primos

## 📋 Verificación de Calidad

### ✅ Estructura del Proyecto
- **API**: `/api/index.py` - Handler serverless optimizado
- **Assets**: `/static_maps_hires/` - Mapas pre-generados
- **Config**: `vercel.json` - Configuración de rutas y builds
- **Deps**: `requirements.txt` - Dependencias Python mínimas

### ✅ Optimizaciones Implementadas
1. **Mapas Pre-generados**: 980 mapas HTML estáticos
2. **Respuesta Rápida**: <5ms al servir archivos estáticos
3. **RAM Mínima**: Sin procesamiento en tiempo real
4. **Caché Eficiente**: Índice en memoria para búsquedas rápidas

## 🌐 Despliegue en Vercel (Recomendado)

### Prerrequisitos
- Cuenta en [Vercel](https://vercel.com)
- Git configurado
- Archivos estáticos generados

### Pasos de Despliegue

1. **Preparar el proyecto**
```bash
# Asegurar que los mapas estén generados
ls static_maps_hires/*.html | wc -l  # Debe mostrar 980+

# Verificar configuración
cat vercel.json
```

2. **Inicializar Git** (si no está hecho)
```bash
git add .
git commit -m "Preparar proyecto para despliegue en Vercel"
```

3. **Desplegar con Vercel CLI**
```bash
# Instalar Vercel CLI (una vez)
npm i -g vercel

# Desplegar
vercel

# Seguir los prompts:
# - Set up and deploy: Y
# - Which scope: (tu cuenta)
# - Link to existing project: N
# - Project name: mapas-primos
# - Directory: ./
# - Override settings: N
```

4. **Despliegue Alternativo (GitHub)**
- Push a GitHub
- Conectar repo en dashboard de Vercel
- Deploy automático en cada push

### Variables de Entorno
No se requieren para la versión estática.

## 🔧 Configuración Post-Despliegue

### Dominio Personalizado
1. En dashboard de Vercel > Settings > Domains
2. Agregar dominio
3. Configurar DNS según instrucciones

### Optimización de Performance
```json
// Ya configurado en vercel.json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

## 📊 Endpoints Disponibles

- `/` - Interfaz principal con selector de mapas
- `/api/info` - Información del sistema
- `/api/maps` - Lista de mapas disponibles
- `/api/random-map` - Mapa aleatorio
- `/api/number/{n}` - Análisis matemático de número
- `/static_maps/map_{hash}.html` - Mapas individuales

## 🔍 Verificación de Despliegue

```bash
# Verificar estado
curl https://tu-app.vercel.app/api/info

# Probar mapa aleatorio
curl https://tu-app.vercel.app/api/random-map

# Verificar lista de mapas
curl https://tu-app.vercel.app/api/maps | jq '.total'
```

## 📈 Monitoreo

- **Analytics**: Dashboard de Vercel
- **Logs**: Vercel > Functions > Logs
- **Performance**: Vercel > Analytics > Web Vitals

## 🆘 Troubleshooting

### Error: "No maps found"
```bash
# Verificar que static_maps_hires tenga archivos
# Re-generar si es necesario:
python3 pregenerate_static_maps.py
```

### Error: "Module not found"
```bash
# Verificar requirements.txt
# Vercel instala automáticamente desde requirements.txt
```

### Límites de Vercel
- **Tamaño máximo**: 50MB por función
- **Timeout**: 30s (configurado)
- **Memory**: 1024MB (configurado)

## 🎯 Mejores Prácticas

1. **Versionado**: Usar tags de Git para releases
2. **Testing**: Probar en preview antes de producción
3. **Caché**: Los mapas estáticos se cachean automáticamente
4. **Seguridad**: No incluir archivos sensibles (.env, .pem)

## 📝 Notas Finales

- La app está optimizada para servir contenido estático
- No requiere base de datos ni servicios externos
- Escala automáticamente con Vercel
- Incluye fallbacks para casos edge

¿Necesitas ayuda? Los logs de Vercel son tu mejor amigo 🔍