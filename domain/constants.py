# domain/constants.py

# Umbrales de calidad de datos
NULL_THRESHOLD_PCT = 0.01        # más del 1% de nulos es problema de calidad

# Umbrales de riesgo de churn
CHURN_RATE_HIGH_THRESHOLD = 0.30  # segmento con churn > 30% es crítico

# Umbrales de facturación
MONTHLY_CHARGES_Q3 = 89.85       # umbral cliente premium
DSL_CHARGES_Q75 = 69.90          # referencia precio DSL
TENURE_NUEVO_CLIENTE = 6         # meses para considerar cliente nuevo
TENURE_RIESGO_ALTO = 12          # meses umbral riesgo alto