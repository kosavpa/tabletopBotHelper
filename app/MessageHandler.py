from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import MessageMediaPoll, PollResults

from ClientHolder import client
from MessagesUtil import create_info, create_message, create_batches_game_list, get_poll
from Store import save_info, update_info, info_is_exist, select_by_chat_and_forum, Info


@client.on(events.NewMessage(incoming=True, pattern='^(/init).*'))
async def init_info(event: NewMessage.Event):
    message: Message = await client.get_messages(event.chat, ids=event.message.id)

    if message.text and len(message.text) != 0:
        created_info: Info = create_info(message)

        if created_info:
            if await info_is_exist(created_info):
                await update_info(created_info)
            else:
                await save_info(created_info)

            if message.reply_to and message.reply_to.forum_topic:
                await client.send_message(
                    message.chat.id,
                    reply_to=message.reply_to.reply_to_msg_id,
                    message='Инициализация успешна'
                )
            else:
                await client.send_message(
                    message.chat.id,
                    message='Инициализация успешна'
                )


@client.on(events.NewMessage(incoming=True, pattern='^(/list).*'))
async def game_list(event: NewMessage.Event):
    message: Message = await client.get_messages(event.chat, ids=event.message.id)

    info: Info

    if message.reply_to and message.reply_to.forum_topic:
        info = await select_by_chat_and_forum(message.chat.id, message.reply_to.reply_to_msg_id)
    else:
        info = await select_by_chat_and_forum(message.chat.id)

    await client.send_message(info.chat_id, reply_to=info.forum_id, message=create_message(info))


@client.on(events.NewMessage(incoming=True, pattern='^(/poll).*'))
async def create_poll(event: NewMessage.Event):
    message: Message = await client.get_messages(event.chat, ids=event.message.id)

    info: Info

    if message.reply_to and message.reply_to.forum_topic:
        info = await select_by_chat_and_forum(message.chat.id, message.reply_to.reply_to_msg_id)
    else:
        info = await select_by_chat_and_forum(message.chat.id)

    for batch in create_batches_game_list(info):
        await client.send_message(
            info.chat_id,
            file=MessageMediaPoll(get_poll(batch, info), PollResults()),
            reply_to=info.forum_id
        )

@client.on(events.NewMessage(incoming=True, pattern='^(/info).*'))
async def game_list(event: NewMessage.Event):
    message: Message = await client.get_messages(event.chat, ids=event.message.id)

    info: Info

    if message.reply_to and message.reply_to.forum_topic:
        info = await select_by_chat_and_forum(message.chat.id, message.reply_to.reply_to_msg_id)
    else:
        info = await select_by_chat_and_forum(message.chat.id)

    await client.send_message(info.chat_id, reply_to=info.forum_id, message=info.get_info())