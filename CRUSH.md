# CRUSH.md - Development Guide

## Development Workflow Directives

### IMPORTANT - Development Rules:
- **NO SIDE EFFECTS**: Al realizar cualquier edición, NO se debe generar o cambiar ninguna otra parte del código
- **ALWAYS COMMIT**: Siempre se debe realizar commit al finalizar el cambio solicitado
- **BRANCH STRATEGY**: Se trabajará sobre la rama `dev`, SIN hacer PR jamás a la rama `main`
- **DOCUMENTATION**: Se debe actualizar y organizar la documentación y los scripts después de utilizarse o actualizarse

## Build/Run Commands
```bash
# Run Flask app (default port 3000) - MAPA INTERACTIVO AVANZADO
# ⚡ NUEVOS PARÁMETROS: 10,000 círculos x 1,300 segmentos = 13M números
export PATH="$(pwd)/venv/bin:$PATH" && python3 app_optimized.py

# Start app in background
./start_app.sh

# Run with custom port
python3 app_optimized.py --port=8080

# Install dependencies
pip install -r requirements.txt

# Run single test file
python3 test_memory_optimization.py
python3 test_flask_route.py

# Check system info and validate setup
curl http://localhost:3000/api/info

# Memory & Cache Operations
curl http://localhost:3000/memory/stats
curl -X POST http://localhost:3000/memory/optimize
curl -X POST http://localhost:3000/cache/clear

# API Testing
curl http://localhost:3000/api/number/97
curl -X POST http://localhost:3000/api/interactive-map -H "Content-Type: application/json" -d '{"num_circulos": 10000, "divisiones_por_circulo": 1300}'

# Probar capacidad extrema (13M números)
curl -X POST http://localhost:3000/api/interactive-map -H "Content-Type: application/json" -d '{"num_circulos": 10000, "divisiones_por_circulo": 1300}' --max-time 600
```

## Desplegar Aplicación ESTÁTICA (RENDIMIENTO MÁXIMO)
```bash
# 🔥 PRE-GENERAR MAPAS ESTÁTICOS (Una sola vez)
python3 pregenerate_static_maps.py

# ⚡ GENERAR MAPAS COMPLETOS HASTA EL TOPE MÁXIMO (10,000×1,300=13M números)
# Solo mapeo lineal con todas las variables de filtros
python3 pregenerate_complete_linear_maps.py

# 🌐 DESPLEGAR EN PUERTO PÚBLICO 3000 - VERSIÓN ESTÁTICA
./scripts/deployment/deploy_static_final.sh

# Ver logs de la aplicación estática
tail -f static_deployment.log

# Ver logs de generación completa
tail -f complete_generation.log

# Detener aplicación estática
pkill -f static_app.py

# Verificar mapas disponibles
curl http://localhost:3000/api/maps | head -20

# Verificar mapas de alta resolución generados
ls -la static_maps_hires/ | head -20
```

## Interfaces Estáticas Disponibles (PUERTO PÚBLICO 3000)
```bash
# 🔥 APLICACIÓN ESTÁTICA - RENDIMIENTO MÁXIMO - DESPLEGADA
http://localhost:3000/                   # Selector de 980 mapas pre-generados
http://localhost:3000/enhanced           # Selector de mapas (alias)
http://localhost:3000/api/maps           # Lista de mapas disponibles (JSON)
http://localhost:3000/api/interactive-map # Búsqueda en mapas pre-generados (POST)
http://localhost:3000/api/random-map     # Mapa aleatorio instantáneo
http://localhost:3000/api/number/97      # Análisis matemático rápido
http://localhost:3000/api/info           # Info del sistema estático
http://localhost:3000/static_map/map_XXX.html # Mapas HTML individuales

# 🌐 ACCESO PÚBLICO ESTÁTICO
http://TU_DOMINIO:3000/                  # 🔥 980 mapas instantáneos

# 📈 CARACTERÍSTICAS ESTÁTICAS:
# • 980 mapas HTML pre-generados (sin cálculos)
# • Respuesta <5ms (archivos estáticos)
# • RAM mínima (sin procesamiento)
# • Máximo rendimiento y escalabilidad
```

## Code Style Guidelines

### Python Conventions:
- **Imports**: Group stdlib, third-party, local with blank lines; no unused imports
- **Functions**: snake_case with docstrings for complex functions; use type hints
- **Variables**: snake_case, descriptive names (e.g., `num_circulos`, `datos_img`)
- **Constants**: ALL_CAPS with prefixes (e.g., `MAX_CONTENT_LENGTH`)
- **Classes**: PascalCase with docstrings

### Performance Patterns (MEMORIA OPTIMIZADA):
- **DISCO CACHE**: Use disk-based cache, not RAM (DiskBasedCache class)
- **NO LRU_CACHE**: Remove @lru_cache decorators to free RAM
- **GC AGGRESSIVE**: Use gc.collect() after large operations
- **MATPLOTLIB CLEANUP**: Always plt.close() and plt.clf() after plots
- Delete large variables explicitly: `del variable; gc.collect()`

### Error Handling:
- Try-except for external APIs and file operations
- Log with `print(f"Error: {str(e)}")` and `traceback.print_exc()`
- Return structured JSON: `{'error': 'desc', 'timestamp': datetime.now().isoformat()}`
- Use appropriate HTTP status codes (400/500)

### API Design:
- REST endpoints return consistent JSON with timestamp/version
- Validate inputs with sensible defaults
- Include cache headers and compression for large responses
- New /api/interactive-map endpoint for responsive HTML maps
- Async tooltip loading with /api/number/<int:number> for detailed math

### Frontend Patterns:
- Use fetch() API with proper error handling
- Implement debouncing for real-time controls (300ms)
- Responsive design with mobile-first approach
- CSS custom properties for theming and consistency

## 📚 Documentation Structure

### Main Documentation:
- `README.md` - Project overview and quick start
- `CRUSH.md` - This file, development guide
- `docs/INDEX.md` - Documentation index with all links
- `docs/SCRIPTS_DOCUMENTATION.md` - Detailed script descriptions

### Script Organization:
- `scripts/deployment/` - Deployment scripts
- `scripts/maintenance/` - System maintenance scripts  
- `scripts/testing/` - Verification and testing scripts
- `archive/` - Old/deprecated files and scripts