from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnToPay = InlineKeyboardButton(text="Купить", callback_data="top_up")
toPayMenu = InlineKeyboardMarkup(row_width=1)
toPayMenu.insert(btnToPay)


def buyMeny(is_url=True, url="", bill=""):

    payMenu = InlineKeyboardMarkup(row_width=1)

    if is_url:
        btnPayQiwi = InlineKeyboardButton(
            text="Оплатить", url=url)
        payMenu.insert(btnPayQiwi)

    btnCheckQiwi = InlineKeyboardButton(
        text="Проверить оплату", callback_data="check_" + bill)
    payMenu.insert(btnCheckQiwi)

    return payMenu
