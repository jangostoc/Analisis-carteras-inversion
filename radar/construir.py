"""Construye la página del Radar de Valoración a partir de la plantilla y un fichero de datos.

Uso:
    python generar_demo.py                       # crea datos_demo.json (datos ficticios)
    python construir.py datos_demo.json ../index.html

Formato del fichero de datos (JSON): {"rows": [...], "tv": {...}}; ver ESQUEMA_DATOS.md.
"""
import json, sys

datos = sys.argv[1] if len(sys.argv) > 1 else 'datos_demo.json'
salida = sys.argv[2] if len(sys.argv) > 2 else '../index.html'
d = json.load(open(datos, encoding='utf-8'))
demo = 'demo' in datos
payload = {
    'asof': d.get('asof', '16 oct 2026'),
    'cart': [],
    'seg': [r[0] for r in d['rows']],
    'segTitle': d.get('titulo', 'Empresas analizadas'),
    'rows': d['rows'],
    'failed': {},
    'notes': '',
    'tv': d.get('tv', {}),
    'source': 'datos ficticios (demo)' if demo else d.get('fuente', 'datos de mercado'),
    'banner': 'Demostración con compañías y datos FICTICIOS: los valores no corresponden a ninguna empresa real.' if demo else '',
}
html = open('plantilla.html', encoding='utf-8').read().replace('/*__DATA__*/', json.dumps(payload, ensure_ascii=False).replace('</', '<\\/'))
open(salida, 'w', encoding='utf-8').write(html)
print(f'{len(d["rows"])} empresas -> {salida}')
