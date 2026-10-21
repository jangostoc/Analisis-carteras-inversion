# Formato de datos del Radar de Valoración

`construir.py` recibe un JSON con estas claves (sólo `rows` es obligatoria):

```json
{ "asof": "21 oct 2026", "rows": [ ... ], "s5": { "TICKER": { ... } },
  "ohlc": { ... }, "wk": { ... }, "earn": { ... }, "ersess": { ... }, "mcap": { ... } }
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

## `s5` — datos de 5 años (velas semanales) por ticker

| Campo | Descripción |
|---|---|
| `hi`, `lo`, `last` | Máximo, mínimo y último cierre de 5 años |
| `hiT`, `loT` | Posición temporal del máximo y del mínimo (sólo importa cuál es anterior) |
| `n` | Número de velas |
| `up`, `dn` | 24 valores (escala relativa, p. ej. 0–1000) con el volumen alcista y bajista por fila de precio, de abajo arriba |

## Otras claves por ticker

| Clave | Formato | Uso |
|---|---|---|
| `ohlc` | `AAAA-M|` + 3 caracteres por mes (alfabeto `A–Z a–z 0–9`, 62 símbolos): `ln(apertura/cierre)·100+30`, `ln(máximo/máx(apertura,cierre))·100`, `ln(mín(apertura,cierre)/mínimo)·100` | Velas mensuales |
| `wk` | `t0|L0:deltas|ohl`: `t0` en segundos Unix de la primera semana, cierres semanales consecutivos codificados como `cz` y 3 caracteres por semana como en `ohlc` | Vista semanal, Fibonacci y volumen ampliados |
| `earn` | `AAAA-MM-DD` | Próxima publicación de resultados |
| `ersess` | `"pre"`, `"after"` o `null` | Antes de la apertura / tras el cierre |
| `mcap` | número (millones de USD) | Capitalización bursátil |

Los indicadores derivados (PEG, media de PER, RSI, SMA 50, rentabilidad YTD, niveles de Fibonacci, POC/VAH/VAL, nodo de volumen y soporte fuerte) se calculan en el navegador.
