# ADR-001: RFC 7807 для ошибок API
Дата: 2025-10-20
Статус: Accepted

## Context
Нужно единообразно возвращать ошибки, маскировать детали и включать correlation_id. Сейчас разные эндпойнты могут отвечать по-разному.

## Decision
Вводим единый helper `problem(status, title, detail, type_, extras)` и глобальные обработчики ошибок FastAPI (404/422/500 и доменные). Формат — RFC 7807 JSON: `type,title,status,detail,correlation_id`.

## Consequences
+ Маскирование деталей исключений, меньше утечек PII.
+ Трассировка инцидентов через `correlation_id`.
+ Небольшая просадка DX из-за стандартизации, но выигрываем в безопасной поддержке.

## Links
- NFR-02 (ошибки RFC7807), NFR-04 (маскирование PII)
- TM: F5, R4
- Tests: `tests/test_errors.py::test_rfc7807_contract`
