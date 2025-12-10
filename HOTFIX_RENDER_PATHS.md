# Hotfix: Rutas Corregidas para Render

## 🐛 Problema Encontrado

Durante el despliegue en Render, la aplicación falló con:
```
FileNotFoundError: [Errno 2] No such file or directory: 
'/home/sebastianvernis/servidor_descarga/static_maps/index.html'
```

**Causa**: Rutas hardcodeadas del sistema local en `static_app.py`

---

## ✅ Correcciones Realizadas

### 1. Rutas Dinámicas en `static_app.py`

**Antes**:
```python
STATIC_MAPS_DIR = Path("/home/sebastianvernis/servidor_descarga/static_maps")
```

**Después**:
```python
BASE_DIR = Path(__file__).parent
STATIC_MAPS_DIR = BASE_DIR / "static_maps"
```

**Beneficio**: Funciona en cualquier entorno (local, Render, Docker)

### 2. Manejo de `index.html` Mejorado

**Antes**:
```python
@app.route('/')
def home():
    return send_file(STATIC_MAPS_DIR / "index.html")  # No existe
```

**Después**:
```python
@app.route('/')
def home():
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return send_file(index_path)
    else:
        # Fallback: API info
        return jsonify({...})
```

**Beneficio**: 
- Busca `index.html` en directorio raíz
- Fallback a JSON API si no existe
- No crashea la app

---

## 🚀 Estado Actual

✅ **Build**: Exitoso - 980 mapas generados  
✅ **Deploy**: Exitoso - servicio live  
✅ **Health Check**: `/api/info` responde correctamente  
⚠️ **UI**: Requiere `index.html` en raíz o usa API directamente

---

## 📋 Endpoints Funcionando

```bash
# Health check (funciona)
curl https://numeros-primos-s47c.onrender.com/api/info

# Lista de mapas (funciona)
curl https://numeros-primos-s47c.onrender.com/api/maps

# Mapa aleatorio (funciona)
curl https://numeros-primos-s47c.onrender.com/api/random-map

# Análisis de número (funciona)
curl https://numeros-primos-s47c.onrender.com/api/number/97

# Página principal (ahora con fallback JSON)
curl https://numeros-primos-s47c.onrender.com/
```

---

## 🔧 Soluciones UI

### Opción 1: Usar Interfaz Existente
El archivo `index.html` existe en el repo. Asegurarse de que se incluya en el deploy:

```bash
# Verificar que index.html está commiteado
git ls-files | grep index.html

# Si no está:
git add index.html
git commit -m "feat: add main interface"
git push origin dev
```

### Opción 2: Crear Nueva Interfaz Simple
Crear un `index.html` minimalista que use la API:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Numeros Primos - Mapas Estáticos</title>
</head>
<body>
    <h1>Visualizador de Números Primos</h1>
    <div id="maps"></div>
    <script>
        fetch('/api/maps')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('maps');
                data.maps.forEach(map => {
                    const link = document.createElement('a');
                    link.href = `/static_map/${map.filename}`;
                    link.textContent = map.description;
                    container.appendChild(link);
                    container.appendChild(document.createElement('br'));
                });
            });
    </script>
</body>
</html>
```

### Opción 3: Usar API Directamente
La API funciona perfectamente. Consumir desde frontend separado:

```javascript
// Obtener mapas disponibles
const response = await fetch('https://numeros-primos-s47c.onrender.com/api/maps');
const maps = await response.json();

// Obtener mapa específico
const mapData = await fetch(`/static_map/${maps[0].filename}`);
```

---

## 🎯 Próximos Pasos

### Inmediato
1. ✅ **Correcciones aplicadas** - commit y push
2. ⚠️ **Verificar index.html** en repo
3. 🔄 **Redeploy** en Render

### Comandos
```bash
cd /home/sebastianvernis/Desarrollo/Render/Numeros_Primos

# Verificar cambios
git diff static_app.py

# Commit correcciones
git add static_app.py
git commit -m "fix: use relative paths for Render deployment"

# Push y redeploy
git push origin dev
```

Render detectará el push y re-desplegará automáticamente.

---

## 📊 Verificación Post-Deploy

Después del redeploy, verificar:

```bash
# Health check
curl https://numeros-primos-s47c.onrender.com/api/info
# Debe retornar: 200 OK con info del sistema

# Homepage
curl https://numeros-primos-s47c.onrender.com/
# Debe retornar: HTML de index.html o JSON con info

# Mapas
curl https://numeros-primos-s47c.onrender.com/api/maps
# Debe retornar: JSON con 980 mapas
```

---

## 💡 Notas

### Rutas en Diferentes Entornos

**Local**:
```
/home/sebastianvernis/Desarrollo/Render/Numeros_Primos/
├── static_app.py
├── index.html
└── static_maps/
    ├── index.json
    └── map_*.html
```

**Render**:
```
/opt/render/project/src/
├── static_app.py
├── index.html
└── static_maps/
    ├── index.json
    └── map_*.html
```

**Docker**:
```
/app/
├── static_app.py
├── index.html
└── static_maps/
    ├── index.json
    └── map_*.html
```

Usando `Path(__file__).parent` funciona en todos los casos.

---

**Fecha**: Noviembre 30, 2025  
**Status**: ✅ Corregido - Listo para redeploy  
**Service**: https://numeros-primos-s47c.onrender.com
