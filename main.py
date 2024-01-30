import dotenv

dotenv.load_dotenv()

import asyncio

from src.bot import Yuna


async def main():
    bot = Yuna()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
