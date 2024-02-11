import os

import asyncpg
import disnake
from disnake.ext import commands

from yuna.logger import main_logger


class Yuna(commands.Bot):
    pool: asyncpg.Pool
    logger = main_logger

    def __init__(self) -> None:
        super().__init__("y!", intents=disnake.Intents.all())
        self.owner_ids.add(1134016724132446208)
        self.load_extension("jishaku")

    async def on_ready(self) -> None:
        main_logger.info(f"Ready with latency of: {self.latency*1000:.2f}ms")

    async def setup(self) -> None:
        main_logger.debug("Loading cogs ...")
        for file in os.listdir("cogs"):
            if (not file.startswith("__")) and file.endswith(".py"):
                main_logger.debug(f"🛑 Loading {file}")
                self.load_extension(f"cogs.{file[:-3]}")
                main_logger.debug(f"☑️  {file} loaded")
        main_logger.debug("Establishing connection with the database ...")
        self.pool = await asyncpg.create_pool(os.environ["PGSQL_URL"])
        main_logger.debug("☑️  Connected to the database.")

        with open("setup_pg.sql", "r") as file:
            await self.pool.execute(file.read())
        main_logger.debug("☑️  Database setup complete.")

    async def start(self) -> None:  # type: ignore
        await self.setup()
        await super().start(os.environ["TOKEN"])
