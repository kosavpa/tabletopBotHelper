import asyncio
from datetime import datetime
from typing import Sequence

import pytz
from croniter import croniter

from telethon.tl.types import MessageMediaPoll, PollResults

from ClientHolder import client
from MessagesUtil import create_batches_game_list, get_poll
from Store import Info, select_all


async def run_periodic_task():
    asyncio.create_task(periodic_loop())


async def periodic_loop():
    while True:
        await ask_about_game()
        await asyncio.sleep(10)


async def ask_about_game():
    infos: Sequence[Info] = await select_all()

    for info in infos:
        now = datetime.now(pytz.timezone(info.time_zone))

        if croniter.match(info.cron_question_about_game, now):
            for batch in create_batches_game_list(info):
                await client.send_message(
                    info.chat_id,
                    file=MessageMediaPoll(get_poll(batch, info), PollResults()),
                    reply_to=info.forum_id
                )