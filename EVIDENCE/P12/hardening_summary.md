# P12 Hardening Summary

## Dockerfile
Было:
- root user
- потенциально latest base image

Стало:
- python:3.12-slim
- запуск под non-root (appuser)
- уменьшена поверхность атаки

## IaC (docker-compose)
Было:
- сервис доступен извне без ограничений

Стало:
- bind на 127.0.0.1
- no-new-privileges
- read-only filesystem

## Вывод
Базовый контейнер и инфраструктура приведены к безопасному минимуму
для production-like окружения.
