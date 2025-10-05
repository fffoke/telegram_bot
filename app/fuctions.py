import asyncio
import config as c
import requests
from setting import bot, scheduler
from app.database.request import get_user, all_user
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError


def getToday(today):
    msg = []
    index = 0
    for lesson in c.schedule[today]:
        index += 1
        num = c.numbers[index]
        msg.append(f'\n{num}{lesson['subject']}'
                f'|{lesson['teacher']}' 
                f'|{lesson['room']}\n')
            
    lastmg = ''.join(msg)

    return lastmg


async def getCurrentTemp():
    response = requests.get(c.url)
    data = response.json()
    temp = f'{data['current']['temp_c']}°'
    city = f'📍{data['location']['name']}'
    text = f'{data['current']['condition']['text']}'
    return f'Погода: {city} {temp} {text}'

#  для отцентровки текста
def text(text):
    curren_text = text.center(20, '-')
    return curren_text

async def daylyMessage(tg_id):
    user = await get_user(tg_id)
    weather = await getCurrentTemp()
    today = getToday(c.weekday_index)
    final_msg = f'{c.days[c.weekday_index]}\n{weather}\n{today}'
    gif = FSInputFile('media/lol.mp4')
    try:
        await bot.send_video(user.tg_id, video=gif, caption=final_msg)
    except Exception as e:
        print(f'ошибка отправки {user}: {e}')
    
async def get_lesson(day, pair):
    users = await all_user() 
    pair -= 1
    lesson = c.schedule[day][pair]
    message = (f'\n{c.numbers[pair+1]} {lesson['subject']}\n'
                f'|{lesson['teacher']}\n '
                f'|{lesson['room']}\n')
    for user in users:
        try:
            await bot.send_message(user.tg_id, text=message)
        except Exception as e:
            print(f'ошибка отправки {user}, {e}')



async def set_job(tg_id):
    user = await get_user(tg_id=tg_id)
    job_id = f'dayly_{user.id}'
    try:
        scheduler.remove_job(job_id=job_id)
    except JobLookupError:
        pass

    scheduler.add_job(
    daylyMessage,          
    "cron",
    args=[user.tg_id],    
    hour=user.hour,
    minute=user.min,
    id=job_id,
    misfire_grace_time=60
)