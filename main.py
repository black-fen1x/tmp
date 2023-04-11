from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import config
import db
import logging
import asyncio
import os
import numpy as np

COMMANDS = """
    /help
"""

bot = Bot(token = config.tbot) #os.getenv("API_TOKEN")
dbs = db.DataBase(config.host, config.user, config.password, config.db_name)

logging.basicConfig(level = logging.INFO)

dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
keyboard.add(KeyboardButton('/help'))

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    if(not dbs.user_exists(message.from_user.id)):
        dbs.add_user(message.from_user.id, message.from_user.first_name)
        await message.delete()
        await bot.send_message(message.from_user.id, "Укажите вашу группу")
        @dp.message_handler()
        async def bot_message(message: types.Message):
            if message.chat.type == "private":
                if message.text == "text":
                    pass
                else:
                    if dbs.get_signup(message.from_user.id) == "group" :
                        dbs.set_group(message.from_user.id, message.text)
                        dbs.set_signup(message.from_user.id, "true")
                        await bot.send_message(message.from_user.id, "Успешная авторизация")
    else:
        await bot.send_message(message.from_user.id, "Регистрация была произведена ранее!")
        await message.delete()

@dp.message_handler(commands = ['change_group'])
async def change_group(message: types.Message):
    if message.chat.type == "private":
        await message.delete()
        await bot.send_message(message.from_user.id, "Введите новое значение")
        @dp.message_handler()
        async def change_group(message: types.Message):
            dbs.set_group(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Группа успешно изменена!")

@dp.message_handler(commands = ['mailing'])
async def mailing_command(message: types.Message):
    if message.chat.type == "private" and np.array(dbs.get_role(message.from_user.id))[0][0] == True:
        await message.delete()
        await bot.send_message(message.from_user.id, "Введите группу для рассылки")
        @dp.message_handler()
        async def mailing_command(message: types.Message):
            mass = np.array(dbs.all_chat(message.text))
            for i in range (len(mass)):
                await bot.send_message(mass[i][0], text='hello')
                #mass = np.delete(mass, [i][0])

        await bot.send_message(message.from_user.id, "Отправлено!")


#print(np.array(dbs.get_role(1163496657))[0][0])

if __name__ == '__main__':
    executor.start_polling(dp)
