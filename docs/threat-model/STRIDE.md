# STRIDE — Study Planner

> Для каждой угрозы указаны: элемент/поток, тип STRIDE, описание, контроль (мера защиты), ссылка на NFR из P03 и как проверяется.

| Поток/Элемент | Угроза (S/T/R/I/D/E) | Описание угрозы | Контроль | Ссылка на NFR | Проверка/Артефакт |
|---|---|---|---|---|---|
| F2 /auth (creds) | S | Подбор или кража учётных данных пользователя | MFA, блокировка после 5 попыток, rate-limit /login | NFR-01, NFR-09 | e2e негативные тесты логина |
| F2 /auth (creds) | T | Подмена запроса клиента | HTTPS, HSTS, CSRF-токены | NFR-03 | Интеграционный тест security headers |
| F3 internal /auth→SVC | R | Нет трассировки входов (repudiation) | correlation_id + аудит логинов | NFR-09 | Лог-тест на наличие correlation_id |
| F5 /plan CRUD | I | Утечка PII в ответах и логах | Маскирование PII, RFC7807 для ошибок | NFR-04, NFR-02 | Контракт-тесты ошибок |
| F6 internal /plan→SVC | D | Перегрузка /plan (DoS) | Rate-limit, p95 ≤ 300мс @50RPS | NFR-02 | Нагрузочный тест (k6/locust) |
| DB | I | Хранение PII без шифрования | Шифрование at-rest, роли с минимальными правами | NFR-08 | Проверка конфигов |
| F8 SCH→MAIL | S/I | Подмена или утечка уведомлений | Scoped API-keys, подпись webhook, retry | NFR-07 | Интеграционный тест провайдера |
| F9 SVC→CAL | E | Эскалация прав через API-key внешнего календаря | Secret rotation policy, least privilege | NFR-09 | Политика ротации + аудит |
| GW | T/I | Отсутствуют security headers | `X-CTO:nosniff`, `X-Frame-Options:DENY`, CSP | NFR-03 | e2e тест заголовков |
| F10 logs | R/I | Логи содержат PII и не нормализованы | Нормализация, запрет PII, retention policy | NFR-04, NFR-09 | Линтер PII в CI |
| SCH | D | Массовые задания вызывают задержку уведомлений | Очередь с backpressure, SLA ≥99% ≤1мин | NFR-07 | Метрики SLA |
| SPA | S | Кража сессии (фиксация) | HttpOnly/SameSite cookie, короткий TTL токена | NFR-01, NFR-03 | e2e cookie-тест |
