from aiogram.utils import executor
from bot import dp
from handlers import client, admin


async def on_start_up(_):
    print("Online")

admin.register_handler(dp)
client.register_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
