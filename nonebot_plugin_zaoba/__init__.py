import asyncio
import random
from datetime import datetime
from pathlib import Path
import nonebot
from nonebot import get_bot
from nonebot import require
from .config import Config

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

morning_greetings_file = "morning_greetings.txt"
evening_greetings_file = "evening_greetings.txt"

global_config = nonebot.get_driver().config
zaoba_config = Config.parse_obj(global_config.dict())
morning_hour = zaoba_config.morning_hour
morning_minute = zaoba_config.morning_minute
evening_hour = zaoba_config.evening_hour
evening_minute = zaoba_config.evening_minute
morning_send = zaoba_config.morning_send
evening_send = zaoba_config.evening_send


def read_greetings(file_name):
    greetings = []
    file_path = Path(__file__).parent / file_name
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            greetings.append(line.strip())
    return greetings


morning_greetings = read_greetings(morning_greetings_file)
evening_greetings = read_greetings(evening_greetings_file)


@scheduler.scheduled_job("cron", hour=morning_hour, minute=morning_minute)  # 周日至周五的早上 7 点执行
async def send_morning_greeting():
    if morning_send:
        today = datetime.today()
        # 检查是否是周五晚上、周六或周日的早上
        if today.weekday() == 5:  # 周六
            return
        if today.weekday() == 6 and today.hour >= 7:  # 周日的早上
            return
        bot = get_bot()
        group_list = await bot.get_group_list()
        group_list = [g['group_id'] for g in group_list]
        greeting = random.choice(morning_greetings)
        send_groups = group_list
        for group in send_groups:
            await bot.send_group_msg(group_id=group, message=greeting)
            await asyncio.sleep(random.randint(5, 10))
    else:
        return


@scheduler.scheduled_job("cron", hour=evening_hour, minute=evening_minute)  # 周日至周五的晚上 11 点执行
async def send_evening_greeting():
    if evening_send:
        today = datetime.today()
        # 检查是否是周五晚上、周六或周日的早上
        if today.weekday() == 4 and today.hour >= 23:  # 周五晚上
            return
        if today.weekday() == 5:  # 周六
            return
        bot = get_bot()
        group_list = await bot.get_group_list()
        group_list = [g['group_id'] for g in group_list]
        greeting = random.choice(evening_greetings)
        send_groups = group_list
        for group in send_groups:
            await bot.send_group_msg(group_id=group, message=greeting)
            await asyncio.sleep(random.randint(10, 15))
    else:
        return
