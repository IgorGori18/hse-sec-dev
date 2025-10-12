# SecDev Course Template

Стартовый шаблон для студенческого репозитория (HSE SecDev 2025).

## Требования
- Python 3.11
- Git, pip, venv
- (Опционально) Make, Docker

## Быстрый старт
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
