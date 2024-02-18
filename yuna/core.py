from __future__ import annotations

import typing

from disnake.ext import commands

if typing.TYPE_CHECKING:
    from yuna.bot import Yuna


class YunaCog(commands.Cog):
    bot: Yuna
    is_group: bool = False

    def __init__(self, bot: Yuna):
        self.bot = bot
        super().__init__()

    @classmethod
    def setup(cls, bot: Yuna) -> None:
        bot.add_cog(cls(bot))
