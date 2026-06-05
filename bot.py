# -*- coding: utf-8 -*-
import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = "8397372232:AAFkaASb2tRiT95Hsxlw5ReUkWN-IEm-tAk"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_error_code(code):
    conn = sqlite3.connect('autodiag.db')
    cursor = conn.cursor()
    query = "SELECT code, brand, model, engine, description, cause, solution FROM obd_codes WHERE code LIKE ?"
    cursor.execute(query, ('%' + code.upper() + '%',))
    result = cursor.fetchone()
    conn.close()
    return result

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Search by error code", callback_data="search_code")], [types.InlineKeyboardButton(text="Check by VIN", callback_data="vin_check")], [types.InlineKeyboardButton(text="My cars", callback_data="my_cars")], [types.InlineKeyboardButton(text="Help", callback_data="help")]])
    await message.answer("Hello! I am Renault Diagnostic Bot. Choose an action:", reply_markup=keyboard)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Commands: /start main menu | /code DF030 search error | /vin VIN check | /help this help")

@dp.message(F.text)
async def search_code_df(message: types.Message):
    text = message.text.strip().upper()
    code = ''.join(c for c in text if c.isalnum())
    
    if len(code) < 4:
        await message.answer("Please enter a valid error code")
        return
    
    result = get_error_code(code)
    
    if result:
        await message.answer("Error Code: " + result[0] + " | Brand: " + result[1] + " | Model: " + result[2] + " | Engine: " + result[3] + " | Description: " + result[4] + " | Causes: " + result[5] + " | Solution: " + result[6])
    else:
        await message.answer("Error code " + code + " not found. Try: DF000, DF030, DF050, DF203, DF233")

@dp.callback_query(F.data == "help")
async def callback_help(call: types.CallbackQuery):
    await call.message.answer("Commands: /start | /code DF030 | /vin VIN | /help")

@dp.callback_query(F.data == "search_code")
async def callback_search_code(call: types.CallbackQuery):
    await call.message.answer("Enter error code (e.g., DF030):")

@dp.callback_query(F.data == "vin_check")
async def callback_vin(call: types.CallbackQuery):
    await call.message.answer("Enter VIN number:")

@dp.callback_query(F.data == "my_cars")
async def callback_my_cars(call: types.CallbackQuery):
    await call.message.answer("You have no cars added yet.")

async def main():
    print("Bot started! Press Ctrl+C to stop.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
