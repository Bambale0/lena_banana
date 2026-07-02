from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from redis.asyncio import Redis

from app.config import Settings
from app.context import AppContext
from app.plugins.loader import load_plugins


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher(context: AppContext, redis: Redis) -> Dispatcher:
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))
    dispatcher["context"] = context
    load_plugins(dispatcher, context)
    return dispatcher


async def register_bot_commands(bot: Bot, settings: Settings) -> None:
    default_commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Главное меню"),
        BotCommand(command="app", description="Открыть BANANA"),
        BotCommand(command="image", description="Banana: фото по референсу"),
        BotCommand(command="motion", description="AI Video: видео по референсу"),
        BotCommand(command="balance", description="Баланс, лимиты и партнерка"),
        BotCommand(command="packages", description="Пополнить кредиты"),
        BotCommand(command="gallery", description="Галерея работ"),
        BotCommand(command="feed", description="Публичная лента"),
        BotCommand(command="partners", description="Партнерская программа"),
        BotCommand(command="help", description="Помощь"),
    ]
    admin_commands = [
        *default_commands,
        BotCommand(command="admin", description="Админка"),
    ]
    await bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())
    for admin_id in settings.admin_ids:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
