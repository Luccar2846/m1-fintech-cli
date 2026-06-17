# application/ports/dataset_repository.py
from abc import ABC, abstractmethod
import pandas as pd


class DatasetRepositoryPort(ABC):
    """
    Puerto de entrada para obtener datasets.
    El use case no sabe si los datos vienen de CSV,
    base de datos, API o cualquier otra fuente.
    """

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Carga el dataset y lo retorna como DataFrame."""
        ...