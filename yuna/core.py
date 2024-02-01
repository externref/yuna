from __future__ import annotations

from disnake.ext import commands

from yuna.bot import Yuna


class YunaCog(commands.Cog):
    bot: Yuna

    def __init__(self, bot: Yuna):
        self.bot = bot
        super().__init__()

    @classmethod
    def setup(cls, bot: Yuna) -> None:
        bot.add_cog(cls(bot))
