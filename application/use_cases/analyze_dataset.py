# application/use_cases/analyze_dataset.py
import pandas as pd
from application.ports.dataset_repository import DatasetRepositoryPort
from domain.value_objects import (
    DataQualityReport,
    ColumnQuality,
    ChurnInsight,
)
from domain.constants import MONTHLY_CHARGES_Q3


class AnalyzeDatasetUseCase:
    """
    Caso de uso: analizar calidad y generar insights de churn.
    Orquesta el dominio — no sabe de dónde vienen los datos
    ni cómo se van a mostrar.
    """

    def __init__(self, repository: DatasetRepositoryPort) -> None:
        self._repository = repository

    def execute(self) -> DataQualityReport:
        df = self._repository.load()
        df = self._clean(df)

        columns = self._analyze_columns(df)
        churn_rate = self._calculate_churn_rate(df)
        insights = self._generate_insights(df)

        return DataQualityReport(
            total_rows=len(df),
            total_columns=len(df.columns),
            columns=tuple(columns),
            churn_rate=churn_rate,
            insights=tuple(insights),
        )

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpieza con criterio de negocio — tenure=0 → TotalCharges=0."""
        df = df.copy()
        df['TotalCharges'] = pd.to_numeric(
            df['TotalCharges'], errors='coerce'
        ).fillna(0)
        return df

    def _analyze_columns(self, df: pd.DataFrame) -> list[ColumnQuality]:
        """Calidad por columna."""
        result = []
        for col in df.columns:
            null_count = df[col].isnull().sum()
            result.append(ColumnQuality(
                name=col,
                dtype=str(df[col].dtype),
                null_count=int(null_count),
                null_pct=round(null_count / len(df), 4),
                unique_count=int(df[col].nunique()),
            ))
        return result

    def _calculate_churn_rate(self, df: pd.DataFrame) -> float:
        """Tasa global de churn."""
        return round((df['Churn'] == 'Yes').mean(), 4)

    def _generate_insights(self, df: pd.DataFrame) -> list[ChurnInsight]:
        """Insights de negocio validados en el EDA."""
        insights = []

        # Insight 1 — Churn por tipo de contrato
        for contrato in df['Contract'].unique():
            segmento = df[df['Contract'] == contrato]
            insights.append(ChurnInsight(
                segment=f"Contrato: {contrato}",
                churn_rate=round(
                    (segmento['Churn'] == 'Yes').mean(), 4
                ),
                client_count=len(segmento),
                monthly_revenue=round(
                    segmento['MonthlyCharges'].sum(), 2
                ),
            ))

        # Insight 2 — Churn por método de pago
        for metodo in df['PaymentMethod'].unique():
            segmento = df[df['PaymentMethod'] == metodo]
            insights.append(ChurnInsight(
                segment=f"Pago: {metodo}",
                churn_rate=round(
                    (segmento['Churn'] == 'Yes').mean(), 4
                ),
                client_count=len(segmento),
                monthly_revenue=round(
                    segmento['MonthlyCharges'].sum(), 2
                ),
            ))

        # Insight 3 — Segmento premium en riesgo
        premium_riesgo = df[
            (df['MonthlyCharges'] > MONTHLY_CHARGES_Q3) &
            (df['Contract'] == 'Month-to-month')
        ]
        insights.append(ChurnInsight(
            segment="Premium sin contrato (riesgo alto)",
            churn_rate=round(
                (premium_riesgo['Churn'] == 'Yes').mean(), 4
            ),
            client_count=len(premium_riesgo),
            monthly_revenue=round(
                premium_riesgo['MonthlyCharges'].sum(), 2
            ),
        ))

        return insights