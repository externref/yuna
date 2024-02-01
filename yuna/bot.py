import os

import asyncpg
import disnake
from disnake.ext import commands


class Yuna(commands.Bot):
    def __init__(self) -> None:

        super().__init__("y!", intents=disnake.Intents.all())
        self.load_extension("jishaku")

    async def setup(self) -> None:
        for file in os.listdir("yuna/cogs"):
            if (not file.startswith("__")) and file.endswith(".py"):
                self.load_extension(f"yuna.cogs.{}")
        pool = asyncpg.create_pool(os.environ["PGSQL_URL"])
        with open("setup_pg.sql", "r") as file:
            await pool.execute(file.read())

    async def start(self) -> None:  # type: ignore
        await super().start(os.environ["TOKEN"])
