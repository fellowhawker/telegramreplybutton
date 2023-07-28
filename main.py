
import os
import psutil
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

import gvars

async def commonmessage(client, message):

    if message.from_user is None:
        return

    if message.text is None:
        return

    textMessage = message.text
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Stats",
                    callback_data="stats_callback"
                )
            ],
        ]
    )

    ReplyButton = [
        [
            "ReplyButton"
        ]
    ]

    if "ReplyButton" in textMessage:
        await message.reply("This is reply",
                            reply_markup=key)

    if "/start" in textMessage:

        replymarkup = ReplyKeyboardMarkup(ReplyButton, one_time_keyboard=True, resize_keyboard=True)
        await message.reply(
            f"Click on the below button to get help about",
            reply_markup=replymarkup,
        )

app = Client(
    name="botbutton",
    app_version="Telegram Desktop 4.5.3 x64",
    device_model="Windows 10",
    api_id=gvars.api_id,
    api_hash=gvars.api_hash,
    bot_token=gvars.bot_token

)
app.add_handler(MessageHandler(commonmessage, None))

@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()

    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="End",
                    callback_data="second_end"
                )
            ],
        ]
    )
    await app.send_message(CallbackQuery.from_user.id, text, reply_markup=key)


@app.on_callback_query(filters.regex("second_end"))
async def second_end(_, CallbackQuery):
    await app.send_message(CallbackQuery.from_user.id, "second end")



async def bot_sys_stats():

    # bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
------------------
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""
    return stats

app.run()