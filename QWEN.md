# 🎯 QWEN.md - Numeros_Primos

## 📋 Información General

| Campo | Valor |
|-------|-------|
| **Nombre del Proyecto** | Numeros_Primos |
| **Versión** | 1.0.0 |
| **Estado** | ✅ PRODUCCIÓN |
| **Tipo** | Aplicación Web Matemática |
| **Categoría** | Visualización Matemática Interactiva |
| **Fecha de Análisis** | 2026-01-09 |

---

## 🎯 Propósito del Proyecto

Sistema de visualización matemática de números primos con representación circular interactiva. Genera 980 mapas HTML pre-generados para respuesta ultra-rápida (<5ms). Combina matemáticas, arte y tecnología.

**Filosofía:** "Los números primos son el arte oculto de las matemáticas"

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

**Backend:**
- Python 3.8+
- Flask (Web framework)
- NumPy (Cálculos matemáticos)
- Matplotlib (Visualización)

**Frontend:**
- HTML5/CSS3/JavaScript
- Canvas API (Visualización circular)
- Vanilla JS (Sin frameworks)

**Matemáticas:**
- Criba de Eratóstenes (Generación de primos)
- Representación polar
- Algoritmos de optimización

**Deployment:**
- Flask development server
- Puerto 3000
- Versión estática (producción)
- Versión dinámica (desarrollo)

---

## ✨ Características Principales

### 1. 980 Mapas HTML Pre-Generados
- Rango: 1 a 10,000
- Incrementos de 10
- Respuesta <5ms
- Sin cálculo en tiempo real

### 2. Visualización Circular de Números Primos
- Representación polar
- Colores diferenciados
- Interactiva (hover)
- Zoom y pan

### 3. API REST
```python
# Endpoints
GET /                    # Home page
GET /map/<numero>        # Mapa específico
GET /api/primes/<n>      # API JSON
GET /api/range/<start>/<end>  # Rango de primos
```

### 4. Versión Estática (Producción)
- 980 archivos HTML pre-generados
- Sin servidor Python necesario
- Hosting estático simple
- Respuesta instantánea

### 5. Versión Dinámica (Desarrollo)
- Generación en tiempo real
- Cualquier rango
- Testing y desarrollo
- Flask server

### 6. Algoritmos Optimizados
- Criba de Eratóstenes optimizada
- Cache de resultados
- Generación batch
- Memoria eficiente

---

## 📂 Estructura del Proyecto

```
Numeros_Primos/
├── app.py                     # Flask application
├── generate_maps.py           # Generador de mapas
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── visualization.js
│   └── maps/                  # 980 mapas pre-generados
│       ├── map_10.html
│       ├── map_20.html
│       └── ...
├── templates/
│   ├── index.html
│   └── map_template.html
├── utils/
│   ├── primes.py              # Algoritmos de primos
│   └── visualization.py       # Generación de visualización
├── tests/
│   └── test_primes.py
└── requirements.txt
```

---

## 🚀 Deployment

### Versión Estática (Producción)
```bash
# Generar todos los mapas
python generate_maps.py

# Servir con cualquier servidor estático
# Nginx, Apache, Cloudflare Pages, etc.
```

### Versión Dinámica (Desarrollo)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py

# Acceder
http://localhost:3000
```

---

## 🔧 Configuración

### Variables de Entorno

```bash
# Flask
FLASK_APP="app.py"
FLASK_ENV="development"  # o "production"
PORT="3000"

# Generación
MAX_NUMBER="10000"
INCREMENT="10"
OUTPUT_DIR="static/maps"
```

### Configuración de Generación

```python
# generate_maps.py
CONFIG = {
    'max_number': 10000,
    'increment': 10,
    'output_dir': 'static/maps',
    'template': 'templates/map_template.html',
    'colors': {
        'prime': '#FF6B6B',
        'composite': '#4ECDC4',
        'background': '#1A1A2E'
    }
}
```

---

## 📊 Métricas del Proyecto

### Performance
- **Respuesta (Estática):** <5ms
- **Respuesta (Dinámica):** <100ms
- **Generación de Mapa:** ~50ms
- **Tamaño por Mapa:** ~50KB

### Cobertura
- **Mapas Pre-Generados:** 980
- **Rango:** 1 - 10,000
- **Números Primos:** 1,229 (hasta 10,000)

### Matemáticas
- **Algoritmo:** Criba de Eratóstenes
- **Complejidad:** O(n log log n)
- **Precisión:** 100%

---

## 🎮 Funcionalidades Principales

### Para Usuarios
1. **Explorar Mapas**
   - Seleccionar rango
   - Ver visualización circular
   - Hover para detalles
   - Zoom interactivo

2. **API REST**
   - Obtener primos en JSON
   - Rangos personalizados
   - Integración con otros proyectos

3. **Educación**
   - Aprender sobre números primos
   - Visualizar patrones
   - Explorar matemáticas

### Para Desarrolladores
- API REST documentada
- Código fuente abierto
- Algoritmos optimizados
- Fácil de extender

---

## 📚 Documentación Disponible

### Técnica
- README.md
- Documentación de API
- Comentarios en código
- Tests unitarios

### Matemática
- Explicación de números primos
- Criba de Eratóstenes
- Representación polar
- Patrones en primos

---

## 🔗 Enlaces y Recursos

- **Producción:** http://localhost:3000
- **API:** http://localhost:3000/api
- **Repositorio:** (Local)
- **Licencia:** MIT

---

## ⚠️ Notas Importantes

### Dependencias Críticas
- Python 3.8+ requerido
- Flask para versión dinámica
- NumPy para cálculos
- Matplotlib para visualización (generación)

### Limitaciones
- Rango pre-generado: 1-10,000
- Incrementos de 10
- Versión dinámica: cualquier rango (más lento)

### Performance
- Versión estática: ultra-rápida
- Versión dinámica: rápida pero requiere cálculo
- Generación batch: ~1 minuto para 980 mapas

---

## 🎯 Estado del Proyecto

| Aspecto | Estado | Notas |
|---------|--------|-------|
| **Desarrollo** | ✅ Completo | v1.0.0 estable |
| **Testing** | ✅ Completo | Tests unitarios |
| **Documentación** | ✅ Completa | README detallado |
| **Producción** | ✅ Ready | Funcional |
| **Mantenimiento** | 🟢 Activo | Estable |

---

## 🔄 Relación con Otros Proyectos

**Proyectos Relacionados:** Ninguno (único en el portfolio)

**Tecnologías Compartidas:**
- Python (con Bet-Copilot, tarot-app)
- Flask (con tarot-app)
- Vanilla JS (con DragNDrop, vanilla-editor)

**Diferenciadores:**
- Único proyecto matemático
- Único con visualización de números primos
- Único con representación circular
- Único con 980 mapas pre-generados
- Único enfocado en educación matemática

---

## 📈 Próximos Pasos / Roadmap

- [ ] Extender rango a 100,000
- [ ] Más tipos de visualización (espiral, grid)
- [ ] Visualización 3D
- [ ] Animaciones de patrones
- [ ] Más algoritmos (Sieve of Atkin)
- [ ] Comparación de algoritmos
- [ ] Exportar visualizaciones (PNG, SVG)
- [ ] Modo educativo interactivo
- [ ] Desafíos matemáticos
- [ ] Integración con Wolfram Alpha
- [ ] App móvil
- [ ] Realidad aumentada (AR)

---

**Última Actualización:** 2026-01-09  
**Analizado por:** Blackbox AI  
**Versión QWEN:** 1.0
