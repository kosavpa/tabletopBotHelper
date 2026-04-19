import sys
from datetime import datetime
from random import randint

import pytz
from croniter import croniter
from telethon.tl.custom import Message
from telethon.tl.types import Poll, PollAnswer, TypeTextWithEntities

from GoogleSheetsVisitor import get_games_list
from Store import Info


def create_info(message: Message) -> Info | None:
    init_str: str = message.text.replace('/init@SimpleTableTopHelperBot', '').strip()

    info_params: list[str] = init_str.split(',')

    info = Info()

    info_params = list(filter(lambda param_str: param_str.find('=') != -1, info_params))

    for param in info_params:
        match param.split('=')[0]:
            case 'sheet_id':
                info.sheet_id = param.split('=')[1].strip()
            case 'cron_question_about_game':
                info.cron_question_about_game = param.split('=')[1].strip()
            case 'cron_game':
                info.cron_game = param.split('=')[1].strip()
            case 'range':
                info.range = param.split('=')[1].strip()
            case 'time_zone':
                info.time_zone = param.split('=')[1].strip()

    if (not info.range or len(info.range) == 0
            or not info.sheet_id or len(info.sheet_id) == 0
            or not info.cron_game or len(info.cron_game) == 0
            or not info.cron_question_about_game or len(info.cron_question_about_game) == 0):
        return None
    else:
        if message.reply_to and message.reply_to.forum_topic:
            info.forum_id = message.reply_to.reply_to_msg_id

        info.chat_id = message.chat.id

        if not info.time_zone or len(info.time_zone) == 0:
            info.time_zone = 'Europe/Samara'

        return info


def get_answers(game_info: list[str]) -> list:
    count = 0
    answers = []

    if len(game_info) == 1:
        game_info.append('Mock answer')

    for game_name in game_info:
        answers.append(PollAnswer(text=TypeTextWithEntities(game_name, []), option=hex(count).encode()))
        count += 1

    return answers


def get_poll(game_info: list[str], info: Info) -> Poll:
    game_date: datetime = croniter(info.cron_game, datetime.now()).get_next(datetime)

    game_date = game_date.astimezone(pytz.timezone(info.time_zone))

    return Poll(
        id=randint(0, sys.maxsize),
        question=TypeTextWithEntities(f'Во что играем {game_date.strftime('%d.%m')}?', []),
        answers=get_answers(game_info),
        closed=False,
        public_voters=True,
        multiple_choice=True,
        quiz=False
    )


def create_batches_game_list(info: Info) -> list[list[str]]:
    result: list[list[str]] = []

    game_list: list[str] = get_games_list(info.sheet_id, info.range)

    for _ in range(int(len(game_list) / 10) + 1):
        result.append([])

    for index, game_info in enumerate(game_list):
        result[int(index / 10)].append(game_info)

    return result


def create_message(info: Info) -> str:
   games:list[str] = get_games_list(info.sheet_id, info.range)

   return '\n'.join(games)