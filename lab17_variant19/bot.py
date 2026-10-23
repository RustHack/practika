"""
ЛР17 — Telegram-бот (aiogram 3), вариант 19: инвестиционный портфель.
Установите BOT_TOKEN и запустите: python bot.py
Без токена работает демо-режим в консоли.
"""
from __future__ import annotations

import asyncio
import os
import logging
from typing import Optional

from portfolio import PortfolioManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальный менеджер портфелей (user_id -> PortfolioManager)
portfolios: dict[int, PortfolioManager] = {}


def get_portfolio(user_id: int) -> PortfolioManager:
    if user_id not in portfolios:
        pm = PortfolioManager()
        # демо-данные
        pm.add("SBER", 100, 270.0)
        pm.add("GAZP", 200, 158.0)
        pm.update_price("SBER", 285.4)
        pm.update_price("GAZP", 158.2)
        portfolios[user_id] = pm
    return portfolios[user_id]


async def cmd_start(message) -> None:
    text = (
        "Привет! Я бот портфеля (вариант 19).\n"
        "Команды:\n"
        "/portfolio — показать портфель\n"
        "/add TICKER QTY PRICE — добавить позицию\n"
        "/price TICKER PRICE — обновить цену\n"
        "/value — стоимость портфеля\n"
    )
    await message.answer(text)


async def cmd_portfolio(message) -> None:
    pm = get_portfolio(message.from_user.id)
    lines = [str(p) for p in pm.positions] or ["Пусто"]
    await message.answer("Портфель:\n" + "\n".join(lines))


async def cmd_value(message) -> None:
    pm = get_portfolio(message.from_user.id)
    await message.answer(f"Стоимость: {pm.total_value():,.2f}\nPnL: {pm.total_pnl():+,.2f}")


async def cmd_add(message) -> None:
    parts = message.text.split()
    if len(parts) != 4:
        await message.answer("Формат: /add TICKER QTY PRICE")
        return
    _, ticker, qty_s, price_s = parts
    try:
        qty, price = float(qty_s), float(price_s)
    except ValueError:
        await message.answer("QTY и PRICE должны быть числами")
        return
    pm = get_portfolio(message.from_user.id)
    pm.add(ticker.upper(), qty, price)
    await message.answer(f"Добавлено: {ticker.upper()} x {qty} @ {price}")


async def cmd_price(message) -> None:
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Формат: /price TICKER PRICE")
        return
    _, ticker, price_s = parts
    try:
        price = float(price_s)
    except ValueError:
        await message.answer("PRICE должно быть числом")
        return
    pm = get_portfolio(message.from_user.id)
    pm.update_price(ticker.upper(), price)
    await message.answer(f"Цена {ticker.upper()} = {price}")


def run_console_demo() -> None:
    """Демо без Telegram."""
    print("=== Демо Telegram-бота (консоль) ===")
    class FakeUser:
        id = 1
    class FakeMessage:
        from_user = FakeUser()
        text = ""
        async def answer(self, text):
            print("[bot]", text)

    async def demo():
        msg = FakeMessage()
        await cmd_start(msg)
        await cmd_portfolio(msg)
        await cmd_value(msg)
        msg.text = "/add LKOH 5 7100"
        await cmd_add(msg)
        msg.text = "/price SBER 290"
        await cmd_price(msg)
        await cmd_portfolio(msg)
        await cmd_value(msg)

    asyncio.run(demo())


def main() -> None:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        print("BOT_TOKEN не задан — запуск демо-режима")
        run_console_demo()
        return

    try:
        from aiogram import Bot, Dispatcher
        from aiogram.filters import Command
        from aiogram.types import Message
    except ImportError:
        print("aiogram не установлен. pip install aiogram")
        run_console_demo()
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_portfolio, Command("portfolio"))
    dp.message.register(cmd_value, Command("value"))
    dp.message.register(cmd_add, Command("add"))
    dp.message.register(cmd_price, Command("price"))

    async def runner():
        logger.info("Бот запущен")
        await dp.start_polling(bot)

    asyncio.run(runner())


if __name__ == "__main__":
    main()
