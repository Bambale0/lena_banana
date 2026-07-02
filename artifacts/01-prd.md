# PRD

## Goal

Build a Telegram webhook bot that lets users generate images and videos through KIE AI and lets admins manage the business entirely inside Telegram.

## Scope

- FastAPI receives Telegram webhooks.
- aiogram handles bot routing and FSM.
- Postgres stores users, models, tasks, packages, payments, gallery items, partners, settings, and broadcasts.
- Redis stores bot dialog state.
- KIE integration supports Nano Banana 2, Nano Banana Pro, and Kling 2.6 Motion Control.
- T-Bank payment plugin supports credit packages and a separate unlimited package.
- Admin panel is implemented as Telegram inline menus, not as a web admin.
- Project runs without Docker.
- Watchdog runner restarts uvicorn on file changes.

## Non-Goals

- No public web frontend.
- No container orchestration.
- No image/video hosting beyond KIE result URLs and Telegram sending.

