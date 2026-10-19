# Formato de datos del Radar de Valoración

`construir.py` recibe un JSON con dos claves:

```json
{ "rows": [ ... ], "tv": { "TICKER": { ... } } }
```

## `rows` — una lista por compañía (16 campos, en este orden)

| # | Campo | Tipo | Descripción |
|---|---|---|---|
| 0 | `lab` | texto | Ticker mostrado |
| 1 | `tk` | texto | Ticker en la fuente de datos |
| 2 | `ex` | texto | Mercado |
| 3 | `name` | texto | Nombre de la compañía |
| 4 | `pe` | número | PER NTM (precio / beneficio normalizado a 12 meses) |
| 5 | `fc` | número o `null` | MC / FCF NTM |
| 6 | `g` | número | % Growth Rate Forward (mediana del crecimiento de ingresos estimado) |
| 7 | `fy` | texto | Cierre fiscal (`dd/mm`) |
| 8 | `lastFY` | entero | Último ejercicio fiscal cerrado |
| 9 | `ann` | lista[10] | PER NTM al cierre de los 10 últimos ejercicios (`null` si no hay dato) |
| 10 | `gy` | texto | Crecimientos anuales estimados separados por `|` |
| 11 | — | entero | Reservado (0) |
| 12 | `ath` | número | % de distancia al máximo histórico |
| 13 | `dd` | lista | Caída mensual desde máximos de los últimos 10 años (enteros, %) |
| 14 | `y0` | entero | Año inicial de `dd` |
| 15 | `cz` | texto | Cierres mensuales codificados: `AAAA-M|L0:deltas`, con `L = round(ln(cierre)·200)` y cada delta en un carácter (`ABC…_`, índice − 31) o `~d,` si excede ±31 |

## `tv` — datos de 5 años (velas semanales) por ticker

| Campo | Descripción |
|---|---|
| `hi`, `lo`, `last` | Máximo, mínimo y último cierre de 5 años |
| `hiT`, `loT` | Posición temporal del máximo y del mínimo (sólo importa cuál es anterior) |
| `n` | Número de velas |
| `up`, `dn` | 24 valores (0–61) con el volumen alcista y bajista por fila de precio, de abajo arriba |

Los indicadores derivados (PEG, media de PER, RSI, SMA 50, niveles de Fibonacci, POC/VAH/VAL, nodo de volumen y soporte fuerte) se calculan en el navegador.
