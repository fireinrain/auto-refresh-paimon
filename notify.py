from datetime import datetime
import time

import pytz
from telegram import Bot
import os
import asyncio
import utils

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
BOT_TOKEN = None
CHAT_ID = None
bot_token = os.getenv('TG_BOT_TOKEN')
chat_id = os.getenv('TG_CHAT_ID')
if bot_token:
    BOT_TOKEN = bot_token
else:
    print(f"you must provide a bot token!")
if chat_id:
    CHAT_ID = chat_id
else:
    print(f"you must provide a chat_id!")


async def send_message2bot(message: str):
    bot = Bot(BOT_TOKEN)
    async with bot:
        # print(await bot.get_me())
        print(message)
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="MarkdownV2")


def pretty_telegram_notify(message_header: str, message_from: str, message_info: str) -> str:
    # 设置时区为东八区
    tz = pytz.timezone("Asia/Shanghai")
    formatted_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    # 替换字符串中的字符
    froms = message_from.split(" ")
    tg_tag1 = froms[0].replace("-", "_")
    tag_tag2 = froms[1].replace("-", "_")

    # 构建消息字符串
    message = f"{message_header}\n\n- 消息来源: {message_from}\n- 当前时间：{formatted_time}\n- 提示消息：\n    {message_info}\n#{tg_tag1} #{tag_tag2}"
    return message
