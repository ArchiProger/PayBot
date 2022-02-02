from aiogram import types, Dispatcher
from bot import bot
from handlers.database import DataBase

import asyncio
import datetime
import config

db = DataBase("../DataBase.db")
loop = asyncio.get_event_loop()
delay = 60.0


def my_callback():
    asyncio.ensure_future(my_func())


async def my_func():

    users = db.getAllUsers()

    for el in users:
        date = db.userDate(el[0])
        user = await bot.get_chat_member(config.chat_id, el[0])

        if date < datetime.date.today():

            try:
                await bot.kick_chat_member(config.chat_id, el[0])
                await bot.unban_chat_member(config.chat_id, el[0])

            except:
                await bot.send_message(config.OWNER_ID,
                                       f"Не удалось исключить пользователя {el[0]} {user.username}\nВозможно его уже нет в группе")

            db.deleteUser(el[0])

        elif date == datetime.date.today() and user.status != "left":

            try:
                await bot.send_message(
                    el[0], "Привет!\nСегодня последний день подписки, если не продлишь, завтра удалю из группы(((")
            except:
                print("Чат не найден")

    when_to_call = loop.time() + delay
    loop.call_at(when_to_call, my_callback)


async def start(message: types.message):
    config.chat_id = message.chat.id
    my_callback()


async def on_user_joined(message: types.message):
    if not db.userExists(message.new_chat_members[0].id):
        await bot.send_message(config.OWNER_ID, f"Пользователя ({message.new_chat_members[0].id} {message.new_chat_members[0].first_name}) нет в базе данных")


def register_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], is_chat_admin=True)
    dp.register_message_handler(
        on_user_joined, content_types=["new_chat_members"])
