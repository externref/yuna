from __future__ import annotations


import disnake
from disnake.ext import commands

from yuna.core import YunaCog

class MemberInfoButtons(disnake.ui.View):
    @disnake.ui.button(label="User Avatar")
    async def view_user_avatar(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction,) -> None:
        ...

    @disnake.ui.button(label="Server Avatar")
    async def view_server_avatar(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction, ) -> None:
        ...

    @disnake.ui.button(label="Banner")
    async def view_banner(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction, ) -> None:
        ...


class Info(YunaCog):
    qualified_name = "info"

    @commands.slash_command(name="memberinfo")
    async def member_info(self, inter: disnake.CmdInter, member: disnake.Member ) -> None:
        ...

    @commands.slash_command(name="serverinfo")
    async def server_info(self, inter: disnake.CmdInter) -> None:
        ...

setup = Info.setup