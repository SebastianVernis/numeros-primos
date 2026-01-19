#!/usr/bin/env python3
"""
Generador de mapas faltantes hasta llegar al tope máximo: 10,000 círculos × 1,300 segmentos.
Genera únicamente mapas lineales con todas las variables de filtros.
Completa la colección hasta el límite máximo de capacidad.
"""

import os
import json
import math
import gc
from datetime import datetime
import hashlib
from pathlib import Path

def criba_de_eratostenes_optimizada(n):
    """Criba de Eratóstenes optimizada para números grandes."""
    if n < 2:
        return []
    
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    
    return [i for i in range(2, n + 1) if sieve[i]]

def calcular_posicion_lineal(numero, divisiones_por_circulo):
    """Calcular posición lineal optimizada."""
    circulo = (numero - 1) // divisiones_por_circulo
    segmento = (numero - 1) % divisiones_por_circulo
    return circulo, segmento

def analizar_patrones_primos_optimizado(primos):
    """Analizar patrones en lista de primos - versión optimizada."""
    conjunto_primos = set(primos)
    patrones = {
        'gemelos': [],
        'primos': [],
        'sexy': [],
        'sophie_germain': [],
        'palindromicos': [],
        'mersenne': [],
        'fermat': []
    }
    
    # Pre-calcular números de Mersenne y Fermat conocidos
    mersenne_conocidos = {3, 7, 31, 127, 8191, 131071, 524287, 2147483647}
    fermat_conocidos = {3, 5, 17, 257, 65537}
    
    for primo in primos:
        # Primos gemelos (p-2 o p+2 es primo)
        if (primo - 2 in conjunto_primos or primo + 2 in conjunto_primos):
            patrones['gemelos'].append(primo)
        
        # Primos primos (p-4 o p+4 es primo)
        if (primo - 4 in conjunto_primos or primo + 4 in conjunto_primos):
            patrones['primos'].append(primo)
        
        # Primos sexy (p-6 o p+6 es primo)
        if (primo - 6 in conjunto_primos or primo + 6 in conjunto_primos):
            patrones['sexy'].append(primo)
            
        # Sophie Germain (2p+1 es primo)
        if 2 * primo + 1 in conjunto_primos:
            patrones['sophie_germain'].append(primo)
            
        # Palindrómicos
        str_primo = str(primo)
        if str_primo == str_primo[::-1] and len(str_primo) > 1:
            patrones['palindromicos'].append(primo)
            
        # Mersenne y Fermat (números conocidos)
        if primo in mersenne_conocidos:
            patrones['mersenne'].append(primo)
        if primo in fermat_conocidos:
            patrones['fermat'].append(primo)
    
    return patrones

def generar_elementos_mapa_optimizado(num_circulos, divisiones_por_circulo, filtros_tipos):
    """Generar elementos del mapa optimizado para grandes volúmenes."""
    total_numeros = num_circulos * divisiones_por_circulo
    
    print(f"   🔍 Generando criba para {total_numeros:,} números...")
    
    # Generar primos
    primos = criba_de_eratostenes_optimizada(total_numeros)
    conjunto_primos = set(primos)
    
    print(f"   📊 Encontrados {len(primos):,} primos")
    print(f"   🧮 Analizando patrones...")
    
    # Analizar patrones
    patrones = analizar_patrones_primos_optimizado(primos)
    
    elementos = []
    batch_size = 50000  # Procesar en lotes
    
    print(f"   ⚡ Procesando elementos en lotes de {batch_size:,}...")
    
    for batch_start in range(1, total_numeros + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, total_numeros)
        
        for numero in range(batch_start, batch_end + 1):
            es_primo = numero in conjunto_primos
            
            # Determinar tipos
            tipos = []
            
            if es_primo:
                if numero in patrones['gemelos'] and filtros_tipos.get('gemelos', False):
                    tipos.append('gemelo')
                if numero in patrones['primos'] and filtros_tipos.get('primos', False):
                    tipos.append('primo')
                if numero in patrones['sexy'] and filtros_tipos.get('sexy', False):
                    tipos.append('sexy')
                if numero in patrones['sophie_germain'] and filtros_tipos.get('sophie_germain', False):
                    tipos.append('sophie_germain')
                if numero in patrones['palindromicos'] and filtros_tipos.get('palindromicos', False):
                    tipos.append('palindromico')
                if numero in patrones['mersenne'] and filtros_tipos.get('mersenne', False):
                    tipos.append('mersenne')
                if numero in patrones['fermat'] and filtros_tipos.get('fermat', False):
                    tipos.append('fermat')
                    
                if not tipos and filtros_tipos.get('regulares', True):
                    tipos.append('regular')
            else:
                if filtros_tipos.get('compuestos', True):
                    tipos.append('compuesto')
            
            # Calcular posición lineal
            circulo, segmento = calcular_posicion_lineal(numero, divisiones_por_circulo)
            
            if tipos:
                elementos.append({
                    'numero': numero,
                    'es_primo': es_primo,
                    'tipos': tipos,
                    'circulo': circulo,
                    'segmento': segmento,
                    'posicion': {
                        'radio': (circulo + 0.5) / num_circulos if num_circulos > 0 else 0,
                        'angulo': segmento * 2 * math.pi / divisiones_por_circulo - math.pi / 2 if divisiones_por_circulo > 0 else 0
                    }
                })
        
        # Limpieza de memoria cada lote
        if batch_end % (batch_size * 4) == 0:
            gc.collect()
            print(f"     📈 Procesados {batch_end:,}/{total_numeros:,} números ({batch_end/total_numeros*100:.1f}%)")
    
    # Estadísticas finales
    estadisticas = {
        'total_numeros': total_numeros,
        'total_primos': len(primos),
        'densidad_primos': len(primos) / total_numeros * 100 if total_numeros > 0 else 0,
        'patrones': {
            'gemelos': len(patrones['gemelos']),
            'primos': len(patrones['primos']),
            'sexy': len(patrones['sexy']),
            'sophie_germain': len(patrones['sophie_germain']),
            'palindromicos': len(patrones['palindromicos']),
            'mersenne': len(patrones['mersenne']),
            'fermat': len(patrones['fermat'])
        },
        'configuracion': {
            'circulos': num_circulos,
            'segmentos': divisiones_por_circulo,
            'mapeo': 'lineal'
        }
    }
    
    # Limpieza final
    del primos, conjunto_primos, patrones
    gc.collect()
    
    return elementos, estadisticas

def generar_html_liviano(estadisticas, parametros, param_hash):
    """Generar HTML liviano para mapas grandes (solo datos JSON)."""
    
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa Lineal {parametros['num_circulos']}×{parametros['divisiones_por_circulo']} - 13M Primos</title>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary-color: #667eea;
            --accent-color: #FFD700;
            --bg-dark: rgba(0, 0, 0, 0.9);
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: white;
        }}
        
        .header {{
            background: var(--bg-dark);
            padding: 2rem;
            text-align: center;
            border-bottom: 3px solid var(--accent-color);
        }}
        
        .title {{
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, var(--accent-color), #FF6B9D, #00FFFF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }}
        
        .mega-stats {{
            font-size: 1rem;
            color: var(--accent-color);
            font-weight: bold;
        }}
        
        .container {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 60vh;
            padding: 2rem;
        }}
        
        .info-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 3rem;
            border-radius: 20px;
            backdrop-filter: blur(20px);
            text-align: center;
            max-width: 800px;
            border: 2px solid var(--accent-color);
        }}
        
        .massive-number {{
            font-size: 4rem;
            font-weight: 900;
            color: var(--accent-color);
            margin: 1rem 0;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .stat-item {{
            background: rgba(255,255,255,0.05);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(255,215,0,0.3);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-color);
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 0.5rem;
        }}
        
        .load-btn {{
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .load-btn:hover {{
            background: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255,215,0,0.3);
        }}
        
        .warning {{
            background: rgba(255, 100, 100, 0.1);
            border: 1px solid rgba(255, 100, 100, 0.3);
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            font-size: 0.9rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            opacity: 0.6;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .massive-number {{ font-size: 2.5rem; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .info-card {{ padding: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            🔢 Mapa Lineal Masivo de Primos
        </div>
        <div class="subtitle">
            {parametros['num_circulos']:,} círculos × {parametros['divisiones_por_circulo']:,} segmentos
        </div>
        <div class="mega-stats">
            ⚡ CAPACIDAD MÁXIMA: 13,000,000 números analizados
        </div>
    </div>
    
    <div class="container">
        <div class="info-card">
            <h2>🎯 Mapa Pre-calculado Disponible</h2>
            
            <div class="massive-number">
                {estadisticas['total_numeros']:,}
            </div>
            <p>números analizados matemáticamente</p>
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{estadisticas['total_primos']:,}</div>
                    <div class="stat-label">Números Primos</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{estadisticas['densidad_primos']:.2f}%</div>
                    <div class="stat-label">Densidad de Primos</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{estadisticas['patrones']['gemelos']:,}</div>
                    <div class="stat-label">Primos Gemelos</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{estadisticas['patrones']['sophie_germain']:,}</div>
                    <div class="stat-label">Sophie Germain</div>
                </div>
            </div>
            
            <button class="load-btn" onclick="loadFullMap()">
                🚀 Cargar Mapa Interactivo Completo
            </button>
            
            <div class="warning">
                ⚠️ <strong>Advertencia:</strong> Este mapa contiene {estadisticas['total_numeros']:,} números. 
                La carga puede tomar varios segundos y usar significant memoria RAM.
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Mapa pre-generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Hash: {param_hash} | Mapeo: Lineal | Primos hasta {estadisticas['total_numeros']:,}</p>
    </div>

    <script>
        function loadFullMap() {{
            const btn = document.querySelector('.load-btn');
            btn.innerHTML = '⏳ Cargando datos...';
            btn.disabled = true;
            
            // Cargar datos del mapa desde JSON
            fetch('data_{param_hash}.json')
                .then(response => response.json())
                .then(data => {{
                    console.log('📊 Datos cargados:', data.elementos.length, 'elementos');
                    
                    // Crear visualización básica
                    createMegaVisualization(data);
                    
                    btn.innerHTML = '✅ Mapa Cargado';
                }})
                .catch(error => {{
                    console.error('Error cargando datos:', error);
                    btn.innerHTML = '❌ Error de Carga';
                }});
        }}
        
        function createMegaVisualization(data) {{
            // Crear visualización básica de puntos para mega-mapas
            const container = document.querySelector('.container');
            const canvas = document.createElement('canvas');
            canvas.width = 800;
            canvas.height = 600;
            canvas.style.border = '2px solid #FFD700';
            canvas.style.borderRadius = '10px';
            
            container.innerHTML = '';
            container.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const maxRadius = Math.min(centerX, centerY) - 20;
            
            // Renderizar muestra de elementos (primeros 5000 para rendimiento)
            const elementos = data.elementos.slice(0, 5000);
            
            elementos.forEach(elemento => {{
                const radius = elemento.posicion.radio * maxRadius;
                const angle = elemento.posicion.angulo;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                
                ctx.fillStyle = elemento.es_primo ? '#FFD700' : '#404040';
                ctx.beginPath();
                ctx.arc(x, y, elemento.es_primo ? 2 : 1, 0, 2 * Math.PI);
                ctx.fill();
            }});
            
            // Agregar información de muestra
            const info = document.createElement('div');
            info.innerHTML = `
                <p style="text-align: center; margin-top: 1rem; color: #FFD700;">
                    📊 Mostrando muestra de 5,000 elementos de {data.elementos.length:,} totales<br>
                    🟡 Amarillo: Primos | 🔘 Gris: Compuestos
                </p>
            `;
            container.appendChild(info);
        }}
        
        // Mostrar estadísticas en consola
        console.log('🔢 Mapa Masivo Cargado:');
        console.log('📊 Total números:', {estadisticas['total_numeros']:,});
        console.log('🔢 Total primos:', {estadisticas['total_primos']:,});
        console.log('📈 Densidad:', '{estadisticas['densidad_primos']:.2f}%');
    </script>
</body>
</html>"""
    
    return html_template

def generar_parametros_completos():
    """Generar combinaciones de parámetros para llegar al tope máximo."""
    
    # Configuraciones progresivas hacia el máximo
    configuraciones_base = [
        # Configuraciones medianas
        (50, 100),   (50, 200),   (50, 500),   (50, 1000),
        (100, 100),  (100, 200),  (100, 500),  (100, 1000),
        (200, 100),  (200, 200),  (200, 500),  (200, 1000),
        (500, 100),  (500, 200),  (500, 500),  (500, 1000),
        
        # Configuraciones grandes
        (1000, 100), (1000, 200), (1000, 500), (1000, 1000), (1000, 1300),
        (2000, 100), (2000, 200), (2000, 500), (2000, 1000), (2000, 1300),
        (3000, 100), (3000, 200), (3000, 500), (3000, 1000), (3000, 1300),
        (4000, 100), (4000, 200), (4000, 500), (4000, 1000), (4000, 1300),
        (5000, 100), (5000, 200), (5000, 500), (5000, 1000), (5000, 1300),
        
        # Configuraciones extremas
        (6000, 1300), (7000, 1300), (8000, 1300), (9000, 1300),
        
        # CONFIGURACIÓN MÁXIMA
        (10000, 1300)  # 13,000,000 números - LÍMITE MÁXIMO
    ]
    
    # Todas las combinaciones de filtros
    filtros_todas_combinaciones = [
        # Solo primos regulares
        {'regulares': True, 'compuestos': False},
        
        # Primos con patrones básicos
        {'regulares': True, 'gemelos': True, 'compuestos': False},
        {'regulares': True, 'gemelos': True, 'primos': True, 'compuestos': False},
        
        # Primos con patrones intermedios
        {'regulares': True, 'gemelos': True, 'primos': True, 'sexy': True, 'compuestos': False},
        {'regulares': True, 'gemelos': True, 'sophie_germain': True, 'compuestos': False},
        {'regulares': True, 'palindromicos': True, 'mersenne': True, 'fermat': True, 'compuestos': False},
        
        # Primos completos
        {'regulares': True, 'gemelos': True, 'primos': True, 'sexy': True, 'sophie_germain': True, 'compuestos': False},
        {'regulares': True, 'gemelos': True, 'primos': True, 'sexy': True, 'sophie_germain': True, 'palindromicos': True, 'compuestos': False},
        
        # Con compuestos
        {'regulares': True, 'gemelos': True, 'primos': True, 'compuestos': True},
        {'regulares': True, 'gemelos': True, 'primos': True, 'sexy': True, 'sophie_germain': True, 'compuestos': True},
        
        # CONFIGURACIÓN COMPLETA - TODAS LAS VARIABLES
        {'regulares': True, 'gemelos': True, 'primos': True, 'sexy': True, 'sophie_germain': True, 'palindromicos': True, 'mersenne': True, 'fermat': True, 'compuestos': True}
    ]
    
    combinaciones = []
    
    for num_circulos, divisiones in configuraciones_base:
        for filtros in filtros_todas_combinaciones:
            combinaciones.append({
                'num_circulos': num_circulos,
                'divisiones_por_circulo': divisiones,
                'tipo_mapeo': 'lineal',  # Solo lineal
                'filtros': filtros
            })
    
    return combinaciones

def generar_hash_parametros(parametros):
    """Generar hash único para combinación de parámetros."""
    param_str = json.dumps(parametros, sort_keys=True)
    return hashlib.md5(param_str.encode()).hexdigest()[:12]

def verificar_mapa_existente(param_hash, output_dir):
    """Verificar si un mapa ya existe."""
    html_path = output_dir / f"map_{param_hash}.html"
    json_path = output_dir / f"data_{param_hash}.json"
    return html_path.exists() and json_path.exists()

def generar_mapas_completos():
    """Función principal de generación completa hasta el tope máximo."""
    
    print("🚀 INICIANDO GENERACIÓN COMPLETA DE MAPAS LINEALES")
    print("🎯 Objetivo: 10,000 círculos × 1,300 segmentos = 13,000,000 números")
    print("⚡ Únicamente mapeo lineal con todas las variables de filtros")
    print("=" * 70)
    
    # Crear directorio de salida
    output_dir = Path("static_maps_hires")
    output_dir.mkdir(exist_ok=True)
    
    # Cargar índice existente si existe
    indice_filepath = output_dir / "index_hires.json"
    if indice_filepath.exists():
        with open(indice_filepath, 'r', encoding='utf-8') as f:
            indice_existente = json.load(f)
            indice_mapas = indice_existente.get('maps', {})
        print(f"📋 Mapas existentes encontrados: {len(indice_mapas)}")
    else:
        indice_mapas = {}
    
    # Obtener todas las combinaciones
    combinaciones = generar_parametros_completos()
    
    print(f"📊 Total combinaciones definidas: {len(combinaciones)}")
    
    # Filtrar combinaciones ya existentes
    combinaciones_nuevas = []
    for parametros in combinaciones:
        param_hash = generar_hash_parametros(parametros)
        if not verificar_mapa_existente(param_hash, output_dir):
            combinaciones_nuevas.append(parametros)
    
    print(f"🆕 Combinaciones nuevas a generar: {len(combinaciones_nuevas)}")
    print()
    
    if not combinaciones_nuevas:
        print("✅ Todos los mapas ya están generados!")
        return indice_mapas
    
    for i, parametros in enumerate(combinaciones_nuevas, 1):
        try:
            total_numeros = parametros['num_circulos'] * parametros['divisiones_por_circulo']
            
            print(f"⚡ [{i}/{len(combinaciones_nuevas)}] Generando: {parametros['num_circulos']:,}×{parametros['divisiones_por_circulo']:,}")
            print(f"   📊 Total números: {total_numeros:,}")
            print(f"   🔍 Filtros: {len([k for k, v in parametros['filtros'].items() if v])} tipos activos")
            
            # Generar elementos y estadísticas
            elementos, estadisticas = generar_elementos_mapa_optimizado(
                parametros['num_circulos'],
                parametros['divisiones_por_circulo'],
                parametros['filtros']
            )
            
            print(f"   ✅ Elementos generados: {len(elementos):,}")
            print(f"   🔢 Primos encontrados: {estadisticas['total_primos']:,}")
            
            # Crear hash único
            param_hash = generar_hash_parametros(parametros)
            
            # Generar HTML (liviano para mapas grandes)
            if total_numeros > 1000000:  # Más de 1M números
                html_content = generar_html_liviano(estadisticas, parametros, param_hash)
            else:
                # Para mapas más pequeños, usar HTML completo del script original
                from pregenerate_static_maps import generar_html_estatico
                html_content = generar_html_estatico(elementos[:1000], estadisticas, parametros)
            
            # Guardar archivos
            filename = f"map_{param_hash}.html"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Guardar datos JSON (limitado para mapas muy grandes)
            json_filename = f"data_{param_hash}.json"
            json_filepath = output_dir / json_filename
            
            # Para mapas muy grandes, guardar solo metadatos y muestra
            if len(elementos) > 100000:
                elementos_guardados = elementos[:10000]  # Solo primeros 10k
                print(f"   💾 Guardando muestra de 10,000 elementos (de {len(elementos):,})")
            else:
                elementos_guardados = elementos
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'elementos': elementos_guardados,
                    'estadisticas': estadisticas,
                    'parametros': parametros,
                    'timestamp': datetime.now().isoformat(),
                    'total_elementos_calculados': len(elementos),
                    'elementos_guardados': len(elementos_guardados)
                }, f, indent=2)
            
            # Agregar al índice
            file_size_kb = os.path.getsize(filepath) // 1024
            json_size_kb = os.path.getsize(json_filepath) // 1024
            
            indice_mapas[param_hash] = {
                'parametros': parametros,
                'html_file': filename,
                'json_file': json_filename,
                'elementos_count': len(elementos),
                'elementos_guardados': len(elementos_guardados),
                'primos_count': estadisticas['total_primos'],
                'densidad': estadisticas['densidad_primos'],
                'file_size_kb': file_size_kb,
                'json_size_kb': json_size_kb,
                'generated': datetime.now().isoformat(),
                'is_mega_map': total_numeros > 1000000
            }
            
            print(f"   💾 Archivos guardados: HTML={file_size_kb}KB, JSON={json_size_kb}KB")
            print(f"   🎯 Progreso total: {len(indice_mapas)}/{len(combinaciones)} mapas")
            print()
            
            # Guardar índice cada 10 mapas
            if i % 10 == 0:
                with open(indice_filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'generated': datetime.now().isoformat(),
                        'total_maps': len(indice_mapas),
                        'maps': indice_mapas,
                        'max_configuration': {
                            'circulos': 10000,
                            'segmentos': 1300,
                            'total_numeros': 13000000
                        }
                    }, f, indent=2)
                print(f"   💾 Índice actualizado ({len(indice_mapas)} mapas)")
            
            # Limpieza de memoria
            del elementos, estadisticas, html_content
            gc.collect()
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            continue
    
    # Guardar índice final
    with open(indice_filepath, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'total_maps': len(indice_mapas),
            'maps': indice_mapas,
            'max_configuration': {
                'circulos': 10000,
                'segmentos': 1300,
                'total_numeros': 13000000
            },
            'completion_stats': {
                'total_combinations': len(combinaciones),
                'generated_new': len(combinaciones_nuevas),
                'total_size_mb': sum(info['file_size_kb'] + info['json_size_kb'] for info in indice_mapas.values()) // 1024,
                'mega_maps': len([info for info in indice_mapas.values() if info.get('is_mega_map', False)])
            }
        }, f, indent=2)
    
    print("🎉 GENERACIÓN COMPLETA FINALIZADA!")
    print(f"📁 Directorio: {output_dir.absolute()}")
    print(f"📊 Total mapas: {len(indice_mapas)}")
    print(f"🔢 Mega-mapas (>1M números): {len([info for info in indice_mapas.values() if info.get('is_mega_map', False)])}")
    print(f"💾 Tamaño total: {sum(info['file_size_kb'] + info['json_size_kb'] for info in indice_mapas.values()) // 1024}MB")
    print(f"🎯 Configuración máxima alcanzada: 10,000×1,300 = 13,000,000 números")
    print(f"🌐 Índice: {indice_filepath}")
    
    return indice_mapas

if __name__ == "__main__":
    indice_mapas = generar_mapas_completos()