from __future__ import annotations

from disnake.ext import commands

from src.bot import Yuna


class YunaCog(commands.Cog):
    bot: Yuna

    def __init__(self, bot: Yuna):
        self.bot = bot
        super().__init__()
