# Backend Architecture

## Runtime

- `app.main` creates the FastAPI application.
- FastAPI lifespan initializes Postgres engine, Redis, aiogram bot, dispatcher, plugins, default seed data, and KIE task tracker.
- Telegram webhook updates are parsed as aiogram `Update` objects and fed into the dispatcher.

## Plugins

- `core`: start, menu, help, balance
- `generation`: KIE flows and file uploads
- `gallery`: public gallery
- `partners`: partner links and click tracking
- `payments`: packages and T-Bank init payment
- `admin`: in-bot admin panel

## Storage

- Postgres via SQLAlchemy async ORM.
- Redis via aiogram `RedisStorage`.

## Background Work

`TaskTracker` polls active KIE tasks and also accepts KIE callback payloads. It updates task status, stores result URLs, creates private gallery drafts, refunds credits on failures, and notifies users.

