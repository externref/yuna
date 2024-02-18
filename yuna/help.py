from __future__ import annotations

import typing

import attrs
import disnake
from disnake.ext import commands

from yuna.core import YunaCog

if typing.TYPE_CHECKING:
    from yuna.bot import Yuna


class YunaInter(disnake.CmdInter):
    bot: Yuna


@attrs.define
class HelpImpl:
    inter: YunaInter

    async def send_help(self, item: str | None = None) -> None:
        if item is None:
            return await self.send_bot_help()
        item = item.strip().lower()
        if cog := self.inter.bot.get_cog(item):
            return await self.send_cog_help(cog)
        elif cmd := self.inter.bot.get_slash_command(item):
            await self.send_command_help(cmd)

    async def send_bot_help(self) -> None:
        bot: Yuna = self.inter.bot
        embed = disnake.Embed(color=disnake.Color.purple()).set_footer(
            icon_url=bot.user.display_avatar.url, text=f"yuna | {bot.version}"
        )
        for cog in bot.cogs.values():
            if cog.qualified_name == "Jishaku": continue
            cog: YunaCog
            if cog.is_group:
                cmds = [
                    f"`{cog.qualified_name.lower()} {child}`"
                    for child in cog.get_slash_commands()[0].children
                ]
            else:
                cmds = []
                for command in cog.get_slash_commands():
                    if command.children:
                        cmds.extend(
                            [f"`{command.name.lower()} {child}`" for child in command.children]
                        )
                    else:
                        cmds.append(f"`{command.name.lower()}`")
            embed.add_field(f"{cog.qualified_name.title()}", ", ".join(cmds), inline=False)
        await self.inter.edit_original_response(embed=embed)

        await self.inter.edit_original_response(embed=embed)

    async def send_command_help(self, cmd: commands.InvokableSlashCommand) -> None: ...

    async def send_group_help(self, grp: commands.InvokableSlashCommand) -> None: ...

    async def send_cog_help(self, cog: commands.Cog) -> None: ...


@commands.slash_command(name="help", description="Get help for commands and groups")
async def _help(inter: YunaInter, query: str | None = None) -> None:
    await inter.response.defer()
    await HelpImpl(inter).send_help(query)
