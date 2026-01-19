#!/usr/bin/env python3
"""
API principal para Vercel - Aplicación optimizada de mapas de números primos
"""

from flask import Flask, request, jsonify, send_file, Response
import os
import json
import hashlib
import random
from datetime import datetime
from pathlib import Path
import traceback

app = Flask(__name__)

# Configuración para Vercel
STATIC_MAPS_DIR = Path("../static_maps_hires")
CACHE_INDEX = None

def cargar_indice_mapas():
    """Cargar índice de mapas pre-generados."""
    global CACHE_INDEX
    try:
        index_path = STATIC_MAPS_DIR / "index.html"
        if index_path.exists():
            # Leer mapas disponibles del directorio
            maps = {}
            for f in STATIC_MAPS_DIR.glob("map_*.html"):
                map_hash = f.stem.replace("map_", "")
                maps[map_hash] = {
                    "archivo": f.name,
                    "parametros": {"num_circulos": 100, "divisiones_por_circulo": 100}
                }
            
            CACHE_INDEX = {"maps": maps}
            print(f"✅ Índice cargado: {len(maps)} mapas disponibles")
            return True
    except Exception as e:
        print(f"❌ Error cargando índice: {e}")
        return False

@app.route('/')
def home():
    """Página principal con selector de mapas."""
    try:
        # Servir index.html estático
        index_path = STATIC_MAPS_DIR / "index.html"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                return Response(f.read(), mimetype='text/html')
        
        # HTML básico si no existe index
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mapa de Números Primos</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                h1 { color: #333; text-align: center; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .info { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                a { color: #1976d2; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔢 Mapa de Números Primos</h1>
                <div class="info">
                    <p>Visualización interactiva de números primos y sus propiedades matemáticas.</p>
                    <p>Endpoints disponibles:</p>
                    <ul>
                        <li><a href="/api/maps">/api/maps</a> - Lista de mapas disponibles</li>
                        <li><a href="/api/info">/api/info</a> - Información del sistema</li>
                        <li><a href="/api/random-map">/api/random-map</a> - Mapa aleatorio</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info')
def system_info():
    """Información del sistema."""
    return jsonify({
        'sistema': 'Mapa de Números Primos - Vercel',
        'version': '2.0',
        'estado': 'activo',
        'timestamp': datetime.now().isoformat(),
        'mapas_disponibles': len(CACHE_INDEX['maps']) if CACHE_INDEX else 0
    })

@app.route('/api/maps')
def listar_mapas():
    """Listar todos los mapas disponibles."""
    try:
        if not CACHE_INDEX:
            cargar_indice_mapas()
        
        return jsonify({
            'total': len(CACHE_INDEX['maps']) if CACHE_INDEX else 0,
            'maps': list(CACHE_INDEX['maps'].keys()) if CACHE_INDEX else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/random-map')
def mapa_aleatorio():
    """Retornar un mapa aleatorio."""
    try:
        if not CACHE_INDEX:
            cargar_indice_mapas()
        
        if CACHE_INDEX and CACHE_INDEX['maps']:
            map_hash = random.choice(list(CACHE_INDEX['maps'].keys()))
            map_path = STATIC_MAPS_DIR / f"map_{map_hash}.html"
            
            if map_path.exists():
                with open(map_path, 'r', encoding='utf-8') as f:
                    return Response(f.read(), mimetype='text/html')
        
        return jsonify({'error': 'No hay mapas disponibles'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/number/<int:number>')
def analizar_numero(number):
    """Análisis matemático de un número."""
    try:
        def es_primo(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        def factorizar(n):
            if n <= 1:
                return []
            factores = []
            d = 2
            while d * d <= n:
                while n % d == 0:
                    factores.append(d)
                    n //= d
                d += 1
            if n > 1:
                factores.append(n)
            return factores
        
        analisis = {
            'numero': number,
            'es_primo': es_primo(number),
            'factores': factorizar(number) if not es_primo(number) else [number],
            'es_par': number % 2 == 0,
            'es_palindromo': str(number) == str(number)[::-1],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(analisis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handler principal para Vercel
def handler(request):
    """Handler para Vercel serverless function."""
    # Cargar índice en primera petición
    if not CACHE_INDEX:
        cargar_indice_mapas()
    
    with app.test_request_context(request.path, method=request.method, data=request.data, headers=request.headers):
        response = app.full_dispatch_request()
        return response

# Para desarrollo local
if __name__ == '__main__':
    cargar_indice_mapas()
    app.run(host='0.0.0.0', port=3000, debug=False)