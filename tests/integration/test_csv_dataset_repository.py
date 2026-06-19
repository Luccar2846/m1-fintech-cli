# tests/integration/test_csv_dataset_repository.py
import pandas as pd
import pytest
from pathlib import Path
from infrastructure.persistence.csv_dataset_repository import CsvDatasetRepository


class TestCsvDatasetRepository:

    def test_carga_csv_real_retorna_dataframe(self, tmp_path):
        """Prueba la implementación REAL — sin mock."""
        # Creamos un CSV temporal — no usamos el de producción
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text("customerID,Churn\nC001,Yes\nC002,No\n")

        repo = CsvDatasetRepository(file_path=csv_file)
        df = repo.load()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ['customerID', 'Churn']

    def test_archivo_inexistente_lanza_error(self):
        """Verifica el manejo de error cuando el archivo no existe."""
        repo = CsvDatasetRepository(file_path="ruta/que/no/existe.csv")

        with pytest.raises(FileNotFoundError):
            repo.load()