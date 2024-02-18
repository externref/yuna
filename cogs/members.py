from __future__ import annotations


import disnake
from disnake.ext import commands

from yuna.core import YunaCog

class Info(YunaCog):
    qualified_name = "info"

    @commands.slash_command(name="memberinfo")
    async def member_info(self, inter: disnake.CmdInter, member: disnake.Member ) -> None:
        ...

    @commands.slash_command(name="serverinfo")
    async def server_info(self, inter: disnake.CmdInter) -> None:
        ...