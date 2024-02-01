import dotenv

dotenv.load_dotenv()

import asyncio  # noqa: E402
import sys  # noqa: E402

from yuna.bot import Yuna  # noqa: E402


async def main():
    bot = Yuna()
    await bot.start()


if sys.argv[1].lower() == "start":
    asyncio.run(main())
