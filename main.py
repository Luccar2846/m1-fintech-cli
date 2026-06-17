from datetime import datetime
from domain.models import Transaction
from domain.exceptions import InvalidTransactionError
from infrastructure.transaction_validator_impl import TransactionValidatorImpl
from application.use_cases.validate_transaction import ValidateTransactionUseCase
from application.use_cases.analyze_dataset import AnalyzeDatasetUseCase
from infrastructure.persistence.csv_dataset_repository import CsvDatasetRepository


def main() -> None:
    """Composition root — cablea y ejecuta todo."""
    _run_transaction_validation()
    _run_eda_analysis()


def _run_transaction_validation() -> None:
    """Valida transacciones de ejemplo."""
    validator = TransactionValidatorImpl()
    use_case = ValidateTransactionUseCase(validator=validator)

    txn_ok = Transaction(
        id="TXN-001",
        amount=250.0,
        currency="USD",
        timestamp=datetime.now(),
        description="Transferencia internacional",
    )

    txn_bad = Transaction(
        id="TXN-002",
        amount=-100.0,
        currency="USD",
        timestamp=datetime.now(),
        description="Monto negativo",
    )

    try:
        result = use_case.execute(txn_ok)
        print(f"✓ TXN-001 válida: {result}")
    except InvalidTransactionError as e:
        print(f"✗ TXN-002 rechazada: {e}")

    try:
        result = use_case.execute(txn_bad)
        print(f"✓ TXN-002 válida: {result}")
    except InvalidTransactionError as e:
        print(f"✗ TXN-002 rechazada: {e}")


def _run_eda_analysis() -> None:
    """Ejecuta el análisis EDA del dataset de Telco."""
    repository = CsvDatasetRepository(
        file_path='data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    )
    use_case = AnalyzeDatasetUseCase(repository=repository)
    report = use_case.execute()

    print(f"\n{'='*50}")
    print(f"REPORTE DE CALIDAD — Telco Customer Churn")
    print(f"{'='*50}")
    print(f"Total filas:    {report.total_rows:,}")
    print(f"Total columnas: {report.total_columns}")
    print(f"Tasa de churn:  {report.churn_rate:.1%}")
    print(f"Problemas:      {'Sí' if report.has_quality_issues() else 'No'}")

    print(f"\n--- Segmentos críticos (churn > 30%) ---")
    for insight in report.high_churn_segments():
        print(f"  {insight.segment}")
        print(f"    Churn:    {insight.churn_rate:.1%}")
        print(f"    Clientes: {insight.client_count:,}")
        print(f"    Revenue:  ${insight.monthly_revenue:,.2f}/mes")


if __name__ == '__main__':
    main()
