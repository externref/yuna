import dotenv

dotenv.load_dotenv()

import asyncio  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402

from yuna.bot import Yuna  # noqa: E402

bot = Yuna()


async def main():
    await bot.start()


command = sys.argv[1].lower()
if command == "start":
    asyncio.run(main())
elif command in ["format", "fmt"]:
    res = os.system("black .; isort .")
    if res == 0:
        bot.logger.info("Formatted files and imports")
    else:
        bot.logger.error("Unexpected error occured")
