"""
ЛР17 — Telegram-бот (aiogram 3), вариант 19: инвестиционный портфель.
Установите BOT_TOKEN и запустите: python bot.py
Без токена работает демо-режим в консоли.
"""
from __future__ import annotations
import asyncio
import os
from portfolio import Portfolio, PRICES

portfolio = Portfolio()

def cmd_start() -> str:
    return (
        "Бот учебного портфеля\n"
        "/portfolio — портфель\n"
        "/buy TICKER QTY — купить\n"
        "/sell TICKER QTY — продать\n"
        "/history — история\n"
        "/yield — доходность"
    )

def cmd_portfolio() -> str:
    lines = [f"Cash: {portfolio.cash:,.2f}"]
    for t, p in portfolio.positions.items():
        price = PRICES.get(t, p.avg_price)
        lines.append(f"{t}: {p.quantity} x {price} (avg {p.avg_price})")
    lines.append(f"Итого: {portfolio.value(PRICES):,.2f}")
    return "\n".join(lines)

def cmd_buy(ticker: str, qty: float) -> str:
    ticker = ticker.upper()
    price = PRICES.get(ticker)
    if price is None:
        return f"Нет котировки для {ticker}"
    return portfolio.buy(ticker, qty, price)

def cmd_sell(ticker: str, qty: float) -> str:
    ticker = ticker.upper()
    price = PRICES.get(ticker)
    if price is None:
        return f"Нет котировки для {ticker}"
    return portfolio.sell(ticker, qty, price)

def cmd_history() -> str:
    return "\n".join(portfolio.history) or "Пусто"

def cmd_yield() -> str:
    invested = sum(p.quantity * p.avg_price for p in portfolio.positions.values())
    current = sum(p.quantity * PRICES.get(t, p.avg_price) for t, p in portfolio.positions.items())
    if invested == 0:
        return "Нет позиций"
    return f"Доходность: {(current / invested - 1) * 100:.2f}%"

async def run_aiogram():
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not set")
    bot = Bot(token)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start(m: types.Message):
        await m.answer(cmd_start())

    @dp.message(Command("portfolio"))
    async def port(m: types.Message):
        await m.answer(cmd_portfolio())

    @dp.message(Command("buy"))
    async def buy(m: types.Message):
        parts = (m.text or "").split()
        if len(parts) < 3:
            await m.answer("Формат: /buy SBER 10")
            return
        await m.answer(cmd_buy(parts[1], float(parts[2])))

    @dp.message(Command("sell"))
    async def sell(m: types.Message):
        parts = (m.text or "").split()
        if len(parts) < 3:
            await m.answer("Формат: /sell SBER 10")
            return
        await m.answer(cmd_sell(parts[1], float(parts[2])))

    @dp.message(Command("history"))
    async def hist(m: types.Message):
        await m.answer(cmd_history())

    @dp.message(Command("yield"))
    async def yld(m: types.Message):
        await m.answer(cmd_yield())

    await dp.start_polling(bot)

def demo():
    print(cmd_start())
    print(cmd_buy("SBER", 10))
    print(cmd_buy("GAZP", 20))
    print(cmd_portfolio())
    print(cmd_sell("SBER", 5))
    print(cmd_yield())
    print(cmd_history())

if __name__ == "__main__":
    if os.environ.get("BOT_TOKEN"):
        asyncio.run(run_aiogram())
    else:
        print("BOT_TOKEN не задан — демо-режим\n")
        demo()
