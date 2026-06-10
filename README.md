# m1-fintech-cli

CLI de validación de transacciones financieras construido con arquitectura hexagonal y Python 3.12.

## Arquitectura

Este proyecto implementa arquitectura hexagonal (ports & adapters) desde el mes 1:
m1-fintech-cli/
├── domain/                    # Entidades y reglas de negocio puras
│   ├── models.py              # Transaction — entidad central
│   └── exceptions.py         # InvalidTransactionError
├── application/               # Casos de uso y puertos
│   ├── ports/                 # Contratos abstractos (ABCs)
│   └── use_cases/             # Orquestación de lógica
├── infrastructure/            # Adaptadores concretos
│   └── transaction_validator_impl.py
├── tests/
│   ├── conftest.py            # Fixtures compartidos
│   ├── unit/                  # Tests unitarios con mocks
│   └── integration/           # Tests de integración
└── main.py                    # Composition root

## Reglas de dependencia

- `domain` no importa nada externo — solo Python stdlib
- `application` importa `domain`, nunca `infrastructure`
- `infrastructure` implementa puertos definidos en `application`
- `main.py` es el único punto que conoce todas las capas

## Setup

```bash
# Requiere uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar dependencias
uv sync

# Ejecutar
uv run python main.py
```

## Tests

```bash
# Correr tests con coverage
uv run pytest tests/unit/ --cov=. --cov-report=term-missing
```

Coverage actual: **99%** — umbral mínimo: 80%

## Stack

| Herramienta | Versión | Rol |
|-------------|---------|-----|
| Python | 3.12.3 | Lenguaje base |
| uv | 0.11.19 | Gestión de entorno y deps |
| pytest | 9.0.3 | Testing |
| pytest-cov | 7.1.0 | Coverage |
| ruff | 0.15.16 | Linter y formatter |
| mypy | 2.1.0 | Type checking |

## Principios aplicados

- **Hexagonal architecture** — dominio desacoplado de infraestructura
- **Dependency injection** — use cases reciben puertos, no implementaciones
- **TDD** — tests escritos junto al código, no después
- **Clean Code** — nombres descriptivos, funciones con una responsabilidad
- **Secrets seguros** — variables de entorno via `python-dotenv`, nunca en código