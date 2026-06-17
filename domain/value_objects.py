# domain/value_objects.py
from dataclasses import dataclass
from domain.constants import NULL_THRESHOLD_PCT, CHURN_RATE_HIGH_THRESHOLD


@dataclass(frozen=True)
class ColumnQuality:
    """Calidad de una columna individual."""
    name: str
    dtype: str
    null_count: int
    null_pct: float
    unique_count: int


@dataclass(frozen=True)
class ChurnInsight:
    """Insight de negocio sobre churn."""
    segment: str
    churn_rate: float
    client_count: int
    monthly_revenue: float


@dataclass(frozen=True)
class DataQualityReport:
    """
    Reporte de calidad de datos — value object inmutable.
    Vive en domain porque representa conocimiento de negocio puro.
    No sabe de dónde vienen los datos ni cómo se calculó.
    """
    total_rows: int
    total_columns: int
    columns: tuple[ColumnQuality, ...]
    churn_rate: float
    insights: tuple[ChurnInsight, ...]

    def has_quality_issues(self) -> bool:
        """¿Hay columnas con nulos significativos?"""
        return any(
            col.null_pct > NULL_THRESHOLD_PCT
            for col in self.columns
        )

    def high_churn_segments(self) -> tuple[ChurnInsight, ...]:
        """Segmentos con churn mayor al umbral crítico."""
        return tuple(
            i for i in self.insights
            if i.churn_rate > CHURN_RATE_HIGH_THRESHOLD
        )