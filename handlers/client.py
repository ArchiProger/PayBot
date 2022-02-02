from aiogram import types, Dispatcher
from handlers.database import DataBase
from handlers.buttons import toPayMenu, buyMeny
from pyqiwip2p import QiwiP2P
from bot import bot

import config
import random
import datetime

db = DataBase("../DataBase.db")
p2p = QiwiP2P(auth_key=config.QIWI_TOKEN)


async def start(message: types.Message):

    if message.chat.type == 'private':

        print(message.from_user.id)

        if not db.userExists(message.from_user.id):
            await message.answer(f"Привет! Для вывода списка команд введите /help\nНа данный у вас нет подписки на группу.\nЖелаете её приобрести за {config.COST}₽?", reply_markup=toPayMenu)

        else:
            await message.answer(f"Привет!\nВаша подписка действительна до {db.userDate(message.from_user.id)}.\nЖелаете продлить?", reply_markup=toPayMenu)


async def id(message: types.Message):
    await message.answer(message.from_user.id)


async def toPayFunc(callback: types.CallbackQuery):
    if not db.userExists(callback.from_user.id):
        db.addUser(callback.from_user.id, datetime.date.today())

    await callback.message.delete()

    comment = str(callback.from_user.id) + \
        ':' + str(random.randint(1000, 99999))
    bill = p2p.bill(amount=config.COST, lifetime=15, comment=comment)

    db.addCheck(callback.from_user.id, bill.bill_id)

    await callback.message.answer(
        f"Стоимость составит {config.COST}₽.\nСсылка на оплату QIWI: {bill.pay_url}",
        reply_markup=buyMeny(url=bill.pay_url, bill=bill.bill_id)
    )


async def checkPayment(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = db.getCheck(bill)

    if info:
        if str(p2p.check(bill_id=bill).status) == "PAID":

            usrDate = db.userDate(callback.from_user.id)

            newDate = usrDate + datetime.timedelta(days=+ config.TIME)
            db.setNewDate(callback.from_user.id, newDate)
            # db.deleteCheck(bill)

            usr = await bot.get_chat_member(config.chat_id, callback.from_user.id)

            if usr.status == "left":
                expire_date = datetime.datetime.now() + datetime.timedelta(days=+1)
                link = await bot.create_chat_invite_link(config.chat_id, expire_date.timestamp, 1)
                await callback.message.answer(f"Счет оплачен 🥳\nОдноразовая ссылка-приглашение в группу: {link.invite_link}")

            else:
                await callback.message.answer("Операция прошла успешно! 🥳")

        else:
            await callback.message.answer("Вы не оплатили счет", reply_markup=buyMeny(False, bill=bill))

    else:
        await callback.message.answer("Счет не найден")


async def help(message: types.message):
    await message.answer("/pay - оплатить подписку\n/id - узнать свой id\n/status - дата исключения из группы")


async def status(message: types.message):

    if db.userExists(message.from_user.id):
        await message.answer(f"{db.userDate(message.from_user.id)}")

    else:
        await message.answer("У вас нет подписки на группу 😥")


def register_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'pay'])
    dp.register_message_handler(id, commands=['id'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(status, commands=['status'])
    dp.register_callback_query_handler(toPayFunc, text="top_up")
    dp.register_callback_query_handler(checkPayment, text_contains="check_")
