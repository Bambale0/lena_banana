# QA Report

## Checks Run

- `python3 -m compileall app scripts`
- `python3 -m ruff check app scripts`
- Imported FastAPI app and verified routes:
  - `/health`
  - `/telegram/webhook`
  - `/kie/callback`
  - `/payments/tbank/callback`
- Built aiogram dispatcher and confirmed 6 plugins load.

## Not Run

- End-to-end Telegram webhook test, because it requires a real bot token and public HTTPS URL.
- Postgres migration/init test, because no local Postgres instance was started in this workspace.
- Real KIE/T-Bank calls, because they require live API credentials.

