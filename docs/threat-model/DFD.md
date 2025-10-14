# DFD — Data Flow Diagram (Study Planner)

## Диаграмма
```mermaid
flowchart LR
    %% External actor
    U["Student / External User"]

    %% Trust Boundary: Client
    subgraph Client["Trust Boundary: Client"]
        SPA["Web / SPA (Frontend)"]
    end

    %% Trust Boundary: Edge
    subgraph Edge["Trust Boundary: Edge"]
        GW["FastAPI Gateway / App"]
    end

    %% Trust Boundary: Core
    subgraph Core["Trust Boundary: Core"]
        SVC["Planner Service"]
        DB["PostgreSQL Database"]
        SCH["Scheduler / Worker"]
        LOG["Logs / Tracing"]
    end

    %% Trust Boundary: Third-Party
    subgraph ThirdParty["Trust Boundary: Third-Party"]
        MAIL["Email / SMS Provider"]
        CAL["External Calendar API"]
    end

    %% Flows (F1..F10)
    U --> |"F1: HTTPS login/signup"| SPA
    SPA --> |"F2: HTTPS /auth (creds)"| GW
    GW --> |"F3: internal /auth"| SVC
    SVC --> |"F4: read/write"| DB
    SPA --> |"F5: HTTPS /plan (CRUD)"| GW
    GW --> |"F6: internal /plan"| SVC
    SVC --> |"F7: enqueue reminder"| SCH
    SCH --> |"F8: send notification"| MAIL
    SVC --> |"F9: sync events"| CAL
    GW --> |"F10: logs/metrics"| LOG

    %% Styling emphasis
    style GW stroke-width:2px
    style DB stroke-width:2px
```

## Потоки данных

| ID  | Откуда → Куда | Протокол / Канал | Данные / PII | Комментарий |
|-----|----------------|------------------|---------------|--------------|
| F1  | User → SPA | HTTPS | email, пароль | Первичный вход / регистрация |
| F2  | SPA → Gateway (/auth) | HTTPS | creds / session | Передача учётных данных |
| F3  | Gateway → Planner Service (/auth) | mTLS / internal API | session claims | Проверка логина |
| F4  | Planner Service → DB | TCP (TLS) | расписание, PII | CRUD над задачами |
| F5  | SPA → Gateway (/plan) | HTTPS | расписание | Основное API |
| F6  | Gateway → Planner Service (/plan) | internal RPC | расписание | Вызов бизнес-логики |
| F7  | Planner Service → Scheduler | Queue / AMQP | job payload | Постановка напоминания |
| F8  | Scheduler → Mail Provider | HTTPS (API key) | email / phone | Отправка уведомления |
| F9  | Planner Service → Calendar API | HTTPS (API key) | события | Синхронизация календаря |
| F10 | Gateway → Logs / Tracing | HTTPS / TCP | correlation_id, метаданные | Централизованные логи |
