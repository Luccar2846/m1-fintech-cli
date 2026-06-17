# tests/unit/test_analyze_dataset.py
import pandas as pd
import pytest
from unittest.mock import MagicMock
from application.use_cases.analyze_dataset import AnalyzeDatasetUseCase
from application.ports.dataset_repository import DatasetRepositoryPort
from domain.value_objects import DataQualityReport


def make_mock_repository(df: pd.DataFrame) -> DatasetRepositoryPort:
    """Crea un repositorio mock que retorna el DataFrame dado."""
    mock = MagicMock(spec=DatasetRepositoryPort)
    mock.load.return_value = df
    return mock


def make_sample_df() -> pd.DataFrame:
    """DataFrame sintético — 5 clientes representativos."""
    return pd.DataFrame({
        'customerID':      ['C001', 'C002', 'C003', 'C004', 'C005'],
        'gender':          ['Male', 'Female', 'Male', 'Female', 'Male'],
        'SeniorCitizen':   [0, 0, 1, 0, 1],
        'Partner':         ['Yes', 'No', 'No', 'Yes', 'No'],
        'Dependents':      ['No', 'No', 'No', 'Yes', 'No'],
        'tenure':          [0, 12, 24, 36, 2],
        'PhoneService':    ['Yes', 'Yes', 'Yes', 'Yes', 'No'],
        'MultipleLines':   ['No', 'Yes', 'No', 'Yes', 'No phone service'],
        'InternetService': ['Fiber optic', 'DSL', 'Fiber optic', 'DSL', 'No'],
        'OnlineSecurity':  ['No', 'Yes', 'No', 'Yes', 'No internet service'],
        'OnlineBackup':    ['No', 'No', 'Yes', 'No', 'No internet service'],
        'DeviceProtection':['No', 'No', 'No', 'Yes', 'No internet service'],
        'TechSupport':     ['No', 'Yes', 'No', 'No', 'No internet service'],
        'StreamingTV':     ['No', 'No', 'Yes', 'No', 'No internet service'],
        'StreamingMovies': ['No', 'No', 'Yes', 'Yes', 'No internet service'],
        'Contract':        ['Month-to-month', 'One year', 'Month-to-month',
                           'Two year', 'Month-to-month'],
        'PaperlessBilling':['Yes', 'No', 'Yes', 'No', 'Yes'],
        'PaymentMethod':   ['Electronic check', 'Mailed check',
                           'Electronic check', 'Bank transfer (automatic)',
                           'Electronic check'],
        'MonthlyCharges':  [70.0, 50.0, 95.0, 45.0, 20.0],
        'TotalCharges':    [' ', '600.0', '2280.0', '1620.0', '40.0'],
        'Churn':           ['Yes', 'No', 'Yes', 'No', 'Yes'],
    })


class TestAnalyzeDatasetUseCase:

    def test_reporte_es_dataqualityreport(self):
        """El use case retorna un DataQualityReport."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        assert isinstance(report, DataQualityReport)

    def test_total_filas_correcto(self):
        """El reporte cuenta correctamente las filas."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        assert report.total_rows == 5

    def test_total_columnas_correcto(self):
        """El reporte cuenta correctamente las columnas."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        assert report.total_columns == 21

    def test_churn_rate_correcto(self):
        """3 de 5 clientes tienen churn — 60%."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        assert report.churn_rate == 0.6

    def test_totalcharges_nulo_imputado(self):
        """TotalCharges con espacio vacío se imputa a 0."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        # Si la imputación falló, has_quality_issues() sería True
        assert not report.has_quality_issues()

    def test_reporte_es_inmutable(self):
        """DataQualityReport no puede ser modificado."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        with pytest.raises(Exception):
            report.total_rows = 9999

    def test_high_churn_segments_filtra_correctamente(self):
        """high_churn_segments retorna solo segmentos con churn > 30%."""
        repo = make_mock_repository(make_sample_df())
        use_case = AnalyzeDatasetUseCase(repository=repo)
        report = use_case.execute()
        for insight in report.high_churn_segments():
            assert insight.churn_rate > 0.30