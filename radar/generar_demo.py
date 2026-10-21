"""Genera un conjunto de datos FICTICIO para la demo pública del Radar de Valoración.

Las compañías, precios y estimaciones son inventados (paseos aleatorios con semilla fija);
sólo sirven para mostrar el funcionamiento de la herramienta.
"""
import datetime, json, math, random

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

A62 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
def q(x):
    return A62[max(0, min(61, round(x)))]
def ohl(o, h, l, c):
    return q(math.log(o / c) * 100 + 30) + q(math.log(h / max(o, c)) * 100) + q(math.log(min(o, c) / l) * 100)

def semanas(c, sig):
    """4 velas semanales por mes que terminan exactamente en el cierre mensual."""
    w = []
    for k in range(1, len(c)):
        a, b = math.log(c[k - 1]), math.log(c[k])
        prev = c[k - 1]
        for s in range(1, 5):
            tgt = math.exp(a + (b - a) * s / 4 + (random.gauss(0, sig / 4) if s < 4 else 0))
            o = prev * math.exp(random.gauss(0, sig / 12))
            h = max(o, tgt) * (1 + abs(random.gauss(0, sig / 5)))
            l = min(o, tgt) * (1 - abs(random.gauss(0, sig / 5)))
            w.append((o, h, l, tgt, random.uniform(0.5, 1.5) * 1e6 / tgt))
            prev = tgt
    return w

HOY = datetime.date(2026, 10, 21)
rows, s5, ohlc, wk, earn, ersess, mcap = [], {}, {}, {}, {}, {}, {}
for tk, name, ex, pe, fc, g, mu, sig in EMPRESAS:
    n = 240  # 20 años de cierres mensuales (2006-11 .. 2026-10)
    c = serie_mensual(n, mu, sig, random.uniform(5, 40))
    run, dd = 0, []
    for v in c:
        run = max(run, v); dd.append(round((v / run - 1) * 100))
    ath = round((c[-1] / max(c) - 1) * 100, 2)
    ann = [round(max(1.0, pe * random.uniform(0.7, 1.5)), 2) if pe > 0 else None for _ in range(10)]
    gy = [round(g * random.uniform(0.6, 1.4), 1) for _ in range(5)]
    gmed = sorted(gy)[2]
    rows.append([tk, tk, ex, name, pe, fc, gmed, '31/12', 2025, ann, '|'.join(map(str, gy)), 0,
                 ath, dd[-120:], 2016, encode(c, 2006, 11)])
    w = semanas(c, sig)  # semana 4·(k-1)..4·k-1 pertenece al mes k
    # velas mensuales de los últimos 10 años
    m0 = n - 120
    ohlc[tk] = '2016-11|' + ''.join(
        ohl(w[4 * (k - 1)][0], max(x[1] for x in w[4 * (k - 1):4 * k]), min(x[2] for x in w[4 * (k - 1):4 * k]), c[k])
        for k in range(m0, n))
    # velas semanales de los últimos 5 años
    ws = w[-261:]
    t0 = int(datetime.datetime(2021, 10, 25, tzinfo=datetime.timezone.utc).timestamp())
    Ls = [round(math.log(x[3]) * 200) for x in ws]
    body = f'{Ls[0]}:' + ''.join(CZA[d + 31] if -31 <= d <= 31 else f'~{d},' for d in (b - a for a, b in zip(Ls, Ls[1:])))
    wk[tk] = f'{t0}|{body}|' + ''.join(ohl(o, h, l, cl) for o, h, l, cl, _ in ws)
    hi = max(x[1] for x in ws); lo = min(x[2] for x in ws)
    hiT = max(range(len(ws)), key=lambda i: ws[i][1]); loT = min(range(len(ws)), key=lambda i: ws[i][2])
    N, step = 24, (hi - lo) / 24; up = [0.0] * N; dn = [0.0] * N
    for o, h, l, cl, vol in ws:
        for j in range(N):
            a, z = lo + j * step, lo + (j + 1) * step
            f = max(0, min(h, z) - max(l, a)) / (h - l) if h > l else 0
            (up if cl >= o else dn)[j] += vol * f
    mx = max(u + d for u, d in zip(up, dn))
    s5[tk] = {'hi': round(hi, 4), 'lo': round(lo, 4), 'last': round(c[-1], 4), 'hiT': hiT, 'loT': loT, 'n': len(ws),
              'up': [round(u / mx * 1000) for u in up], 'dn': [round(d / mx * 1000) for d in dn]}
    earn[tk] = (HOY + datetime.timedelta(days=random.randint(1, 45))).isoformat()
    ersess[tk] = random.choice(['pre', 'after', 'pre', 'after', None])
    mcap[tk] = round(10 ** random.uniform(3, 6.3))  # millones de USD

json.dump({'asof': '21 oct 2026', 'rows': rows, 's5': s5, 'ohlc': ohlc, 'wk': wk, 'earn': earn,
           'ersess': ersess, 'mcap': mcap}, open('datos_demo.json', 'w'), ensure_ascii=False)
print(len(rows), 'empresas ficticias generadas')
