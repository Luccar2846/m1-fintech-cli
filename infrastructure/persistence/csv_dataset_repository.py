# infrastructure/persistence/csv_dataset_repository.py
import pandas as pd
from pathlib import Path
from application.ports.dataset_repository import DatasetRepositoryPort


class CsvDatasetRepository(DatasetRepositoryPort):
    """
    Adaptador concreto — lee datos desde un archivo CSV.
    Implementa el puerto — el use case no sabe que existe esto.
    """

    def __init__(self, file_path: str | Path) -> None:
        self._file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        if not self._file_path.exists():
            raise FileNotFoundError(
                f"Dataset no encontrado: {self._file_path}"
            )
        return pd.read_csv(self._file_path)