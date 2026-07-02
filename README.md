# StupidBot

Telegram webhook bot on FastAPI and aiogram for Comet API image and video generation:

- Banana through Comet image models
- Banana Pro through Comet image models
- Banana 2 through Comet image models
- Kling 2.6 and Kling 3.0 Motion Control through KIE, using an image plus a
  motion-reference video
- Seedance 2 image-to-video through Comet `/v1/videos`, with KIE fallback
- Postgres for durable data
- Redis for aiogram FSM state
- In-bot admin panel
- Local watchdog runner without Docker

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip setuptools wheel
python3 -m pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env`:

- `TELEGRAM_BOT_TOKEN`
- `ADMIN_IDS`
- `DATABASE_URL`
- `REDIS_URL`
- `COMET_API_KEY`
- optional `TELEGRAM_BOT_USERNAME` for payment return buttons
- `PUBLIC_BASE_URL`
- optional `MINI_APP_PATH` for BANANA, defaults to `/miniapp`
- optional `COMET_CALLBACK_SECRET` for provider callback protection
- optional `TBANK_TERMINAL_KEY` and `TBANK_PASSWORD`

Create the Postgres database and start Redis, then run migrations and seed defaults:

```bash
python3 -m scripts.init_db
```

Run the bot:

```bash
python3 -m app.main
```

Run with automatic restart on file changes:

```bash
python3 -m app.watchdog
```

## Webhook

FastAPI exposes:

- `POST /telegram/webhook` for Telegram
- `POST /comet/callback` for Comet video task callbacks
- `POST /payments/tbank/callback` for T-Bank notifications
- `GET /miniapp` for the BANANA Telegram Mini App
- `GET /health` for health checks

If `TELEGRAM_SET_WEBHOOK=true`, the app sets Telegram webhook on startup using:

```text
{PUBLIC_BASE_URL}{TELEGRAM_WEBHOOK_PATH}
```

Set `TELEGRAM_SECRET_TOKEN` and use HTTPS in production.
Set `COMET_CALLBACK_SECRET` in production so provider callbacks use a signed URL:

```text
{PUBLIC_BASE_URL}/comet/callback?token={COMET_CALLBACK_SECRET}
```

## Bot Menu

User menu:

- `BANANA`: Telegram Mini App prompt builder with a pink visual brief UI
- `Banana`: image generation through Comet image models
- `AI Video`: Seedance 2 image-to-video plus Kling 2.6 and Kling 3.0 Motion Control
- `Галерея`: public gallery with prompts
- `Партнеры`: partner links with click tracking
- `Баланс`: pink banana balance and unlimited status
- `Пакеты`: T-Bank pink banana package payment or manual pending payment

Admin menu:

- `Статистика`
- `Пользователи`
- `Модели`
- `Пакеты`
- `Платежи`
- `Галерея`
- `Партнеры`
- `Настройки`
- `Рассылка`

Open it with `/admin` or the `Админка` button.

## Telegram Mini App

BANANA is served from:

```text
{PUBLIC_BASE_URL}{MINI_APP_PATH}
```

Default path:

```text
MINI_APP_PATH=/miniapp
```

Open it with `/app` or the `BANANA` button in the main menu. The Mini App sends a
prompt brief back to the bot with Telegram `WebApp.sendData`; the generation plugin
then starts the matching image or video flow.

## Plugin System

Plugins live in `app/plugins/<name>/plugin.py` and expose:

```python
def setup(dispatcher, context) -> None:
    dispatcher.include_router(router)
```

Enabled plugins are configured with `ENABLED_PLUGINS`:

```text
ENABLED_PLUGINS=core,generation,gallery,partners,payments,admin
```

## Operations Without Docker

Use `systemd/stupidbot.service` as a template. Copy the project to `/opt/stupidbot`,
create `/opt/stupidbot/.venv`, place `.env` there, then install and enable the unit.

For development or small local deployments, `python3 -m app.watchdog` runs `uvicorn`
and restarts it when files under `app`, `scripts`, `.env`, or `pyproject.toml` change.
Run `python3 -m scripts.init_db` before starting the service; the systemd template
does this automatically through `ExecStartPre`.

The nginx site configured on this server proxies `https://stupid.chillcreative.ru`
to `127.0.0.1:8092`, so set `PORT=8092` in `.env`.

Optional Comet model settings:

```text
COMET_BASE_URL=https://api.cometapi.com
COMET_IMAGE_SIMPLE_MODEL=gemini-3.1-flash-image-preview
COMET_IMAGE_PRO_MODEL=gemini-3-pro-image-preview
COMET_IMAGE_2_MODEL=gemini-3.1-flash-image-preview
COMET_KLING_2_6_MODEL=kling-v2-6
COMET_KLING_3_0_MODEL=kling-v2-master
COMET_SEEDANCE_2_MODEL=doubao-seedance-2-0
KIE_KLING_2_6_MOTION_CONTROL_MODEL=kling-2.6/motion-control
KIE_KLING_3_0_MOTION_CONTROL_MODEL=kling-3.0/motion-control
KIE_SEEDANCE_2_MODEL=bytedance/seedance-2
```
