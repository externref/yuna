import dotenv

dotenv.load_dotenv()

import asyncio

from yuna.bot import Yuna


async def main():
    bot = Yuna()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
