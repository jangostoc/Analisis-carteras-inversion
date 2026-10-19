"""Genera un conjunto de datos FICTICIO para la demo pública del Radar de Valoración.

Las compañías, precios y estimaciones son inventados (paseos aleatorios con semilla fija);
sólo sirven para mostrar el funcionamiento de la herramienta.
"""
import json, math, random

CZA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
random.seed(7)

EMPRESAS = [  # ticker, nombre, mercado, PER actual, MC/FCF, crecimiento base, tendencia anual, volatilidad
    ('ALFA', 'Alfa Semiconductores S.A.', 'Demo', 18.0, 21.0, 38, 0.17, 0.12),
    ('BRSA', 'Bravo Software Corp.', 'Demo', 24.0, 22.5, 16, 0.14, 0.09),
    ('CNTR', 'Centauro Retail Inc.', 'Demo', 21.5, 24.0, 7, 0.06, 0.06),
    ('DLTA', 'Delta Energía S.A.', 'Demo', 7.5, 9.0, 4, 0.03, 0.08),
    ('ECOM', 'Eco Commerce Ltd.', 'Demo', 31.0, 28.0, 24, 0.10, 0.14),
    ('FARM', 'Farma Global plc', 'Demo', 15.0, 17.0, 6, 0.04, 0.05),
    ('GAMA', 'Gama Pagos Inc.', 'Demo', 26.0, 25.0, 14, 0.12, 0.07),
    ('HLIO', 'Helio Aeroespacial S.A.', 'Demo', -35.0, -20.0, 45, 0.20, 0.20),
    ('IBRA', 'Ibérica Banca S.A.', 'Demo', 9.0, None, 5, 0.07, 0.07),
    ('JUNO', 'Juno Robótica Corp.', 'Demo', 42.0, 55.0, 30, 0.22, 0.16),
    ('KAPA', 'Kapa Consumo Básico S.A.', 'Demo', 19.5, 21.0, 3, 0.02, 0.04),
    ('LUMA', 'Luma Redes Sociales Inc.', 'Demo', 12.0, 13.0, 9, -0.05, 0.13),
]

def encode(closes, y, m):
    L = [round(math.log(c) * 200) for c in closes]
    out = f"{y}-{m}|{L[0]}:"
    for a, b in zip(L, L[1:]):
        d = b - a
        out += CZA[d + 31] if -31 <= d <= 31 else f"~{d},"
    return out

def serie_mensual(n, mu, sigma, p0):
    c = [p0]
    for _ in range(n - 1):
        c.append(c[-1] * math.exp(mu / 12 + random.gauss(0, sigma)))
    return c

rows, tv = [], {}
for tk, name, ex, pe, fc, g, mu, sig in EMPRESAS:
    n = 240  # 20 años de cierres mensuales (2006-11 .. 2026-10)
    c = serie_mensual(n, mu, sig, random.uniform(5, 40))
    # máximo histórico y caída mes a mes de los últimos 10 años
    run, dd = 0, []
    for v in c:
        run = max(run, v); dd.append(round((v / run - 1) * 100))
    ath = round((c[-1] / max(c) - 1) * 100, 2)
    ann = [round(max(1.0, pe * random.uniform(0.7, 1.5)), 2) if pe > 0 else None for _ in range(10)]
    gy = [round(g * random.uniform(0.6, 1.4), 1) for _ in range(5)]
    gmed = sorted(gy)[2]
    rows.append([tk, tk, ex, name, pe, fc, gmed, '31/12', 2025, ann, '|'.join(map(str, gy)), 0,
                 ath, dd[-120:], 2016, encode(c, 2006, 11)])
    # velas semanales sintéticas de 5 años para Fibonacci y volumen por precio
    w = []
    for v in c[-60:]:
        for _ in range(4):
            o = v * math.exp(random.gauss(0, sig / 3)); cl = o * math.exp(random.gauss(0, sig / 3))
            h = max(o, cl) * (1 + abs(random.gauss(0, sig / 4))); l = min(o, cl) * (1 - abs(random.gauss(0, sig / 4)))
            w.append((o, h, l, cl, random.uniform(0.5, 1.5) * 1e6 / v))
    w[-1] = (w[-1][0], max(w[-1][1], c[-1]), min(w[-1][2], c[-1]), c[-1], w[-1][4])
    hi = max(x[1] for x in w); lo = min(x[2] for x in w)
    hiT = max(range(len(w)), key=lambda i: w[i][1]); loT = min(range(len(w)), key=lambda i: w[i][2])
    N, step = 24, (hi - lo) / 24; up = [0.0] * N; dn = [0.0] * N
    for o, h, l, cl, vol in w:
        for j in range(N):
            a, z = lo + j * step, lo + (j + 1) * step
            f = max(0, min(h, z) - max(l, a)) / (h - l) if h > l else 0
            (up if cl >= o else dn)[j] += vol * f
    mx = max(u + d for u, d in zip(up, dn))
    tv[tk] = {'hi': round(hi, 4), 'lo': round(lo, 4), 'last': round(c[-1], 4), 'hiT': hiT, 'loT': loT, 'n': len(w),
              'up': [round(u / mx * 61) for u in up], 'dn': [round(d / mx * 61) for d in dn]}

json.dump({'rows': rows, 'tv': tv}, open('datos_demo.json', 'w'), ensure_ascii=False)
print(len(rows), 'empresas ficticias generadas')
