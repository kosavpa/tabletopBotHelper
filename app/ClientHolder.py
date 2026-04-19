import os

from telethon import TelegramClient

bot_token: str = os.environ['BOT_TOKEN']
bot_api_hash: str = os.environ['BOT_API_HASH']
bot_api_id: int = int(os.environ['BOT_API_ID'])

client: TelegramClient = TelegramClient('bot', bot_api_id, bot_api_hash).start(bot_token=bot_token)


async def start_up_client():
    await client.start()

    print("Bot success start")

    await client.run_until_disconnected()
