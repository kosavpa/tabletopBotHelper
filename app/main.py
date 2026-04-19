import asyncio

from ClientHolder import start_up_client
from PeriodicTask import run_periodic_task
from Store import create_table
import MessageHandler


async def main():
    await create_table()

    await run_periodic_task()

    await start_up_client()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
