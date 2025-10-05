import logging
from aiogram import Bot , Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart , Command
from app.handlers import router
import app.handlers as a
import asyncio
import config as c 
import app.fuctions as f                                
from aiogram.types import FSInputFile
from app.database.models import asyn_main
from app.database.request import save_user, all_user
from setting import bot, dp, scheduler




async def main():
    # вторника (1)
    scheduler.add_job(f.get_lesson, "cron", day_of_week="tue", hour=10, minute=15, args=[1, 2])
    scheduler.add_job(f.get_lesson, "cron", day_of_week="tue", hour=11, minute=35, args=[1, 3])

    # субботы (5)
    scheduler.add_job(f.get_lesson, "cron", day_of_week="sat", hour=9, minute=10, args=[5, 2])
    scheduler.add_job(f.get_lesson, "cron", day_of_week="sat", hour=10, minute=25, args=[5, 3])

    # (понедельник, среда, четверг, пятница)
    scheduler.add_job(f.get_lesson, "cron", day_of_week="mon,wed,thu,fri", hour=9, minute=40, args=[0, 2])
    scheduler.add_job(f.get_lesson, "cron", day_of_week="mon,wed,thu,fri", hour=11, minute=15, args=[0, 3])

    scheduler.start()
    await asyn_main()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('EXIT')

