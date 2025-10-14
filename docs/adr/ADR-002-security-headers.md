# ADR-002: Security Headers middleware
Дата: 2025-10-20
Статус: Accepted

## Context
Нужно гарантировать базовые security-заголовки на всех ответах: `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`.

## Decision
Добавляем middleware, которое проставляет:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy: default-src 'self'`

## Consequences
+ Митигируем clickjacking, MIME sniffing, уменьшаем поверхность XSS.
+ Единая точка контроля.
+ Нужно поддерживать CSP под реальные ассеты.

## Links
- NFR-03 (заголовки безопасности)
- TM: GW, R9
- Tests: `tests/test_security_headers.py`
