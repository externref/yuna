from __future__ import annotations

import datetime
import typing

import disnake
from disnake.ext import commands

from utils import emojis
from yuna.core import YunaCog


class AFKData(typing.TypedDict):
    user_id: int
    guild_id: int
    is_global: bool
    message: str
    created_on: datetime.datetime


class AFKMessageData(typing.TypedDict):
    user_id: int
    guild_id: int
    mention_msg: str
    mention_url: str
    created_on: datetime.datetime


class AFK(YunaCog):
    async def add_afk_to_user(
        self, user: disnake.Member, message, _global: bool = False
    ) -> None:
        if _global:
            await self.bot.pool.execute(
                "DELETE FROM afk_data WHERE user_id=$1", user.id
            )
        await self.bot.pool.execute(
            "INSERT INTO afk_data VALUES ($1, $2, $3, $4);",
            user.id,
            user.guild.id,
            _global,
            message,
        )

    @commands.Cog.listener(disnake.Event.message)
    async def remove_afk(self, message: disnake.Message) -> None:
        data: None | AFKData = await self.bot.pool.fetchrow(
            "SELECT * FROM afk_data WHERE user_id=$1 OR is_global=$2",
            message.author.id,
            True,
        )
        if not data:
            return
        mentions = ""
        if data["is_global"]:
            mentions_d: list[AFKMessageData] = await self.bot.pool.fetch(
                "SELECT * FROM afk_mentions WHERE user_id=$1", message.author.id
            )
        else:
            mentions_d: list[AFKMessageData] = await self.bot.pool.fetch(
                "SELECT * FROM afk_mentions WHERE user_id=$1 AND guild_id=$2",
                message.author.id,
                message.guild.id,
            )
        print(mentions_d)
        for mention in sorted(mentions_d, key=lambda x: x["created_on"])[:10]:
            mentions += f"{disnake.utils.format_dt(mention['created_on'], 'R')} [{mention['mention_msg']}]({mention['mention_url']})\n"
        await self.bot.pool.execute(
            "DELETE FROM afk_data WHERE user_id=$1", message.author.id
        )
        await self.bot.pool.execute(
            "DELETE FROM afk_mentions WHERE user_id=$1", message.author.id
        )
        await message.reply(
            embed=disnake.Embed(
                description=f"Your AFK has been removed\n\n{emojis.Emojis.MENTION} **Recent Mentions**\{mentions or None}n"
            )
        )

    @commands.Cog.listener(disnake.Event.message)
    async def message_sent(self, message: disnake.Message) -> None:
        for mention in message.mentions:
            await self.add_mention(mention, message)

    async def add_mention(self, user: disnake.Member, message: disnake.Message) -> None:
        data: None | AFKData = await self.bot.pool.fetchrow(
            "SELECT * FROM afk_data WHERE user_id=$1 AND (guild_id=$2 OR is_global=$3)",
            user.id,
            user.guild.id,
            True,
        )
        if data:
            await self.bot.pool.execute(
                "INSERT INTO afk_mentions VALUES ($1, $2, $3, $4);",
                user.id,
                user.guild.id,
                message.clean_content[:30],
                message.jump_url,
            )

    @commands.slash_command(name="afk")
    async def _afk(self, _: disnake.CmdInter) -> None: ...

    @_afk.sub_command("set")
    async def set_afk(self, inter: disnake.CmdInter, message: str = "AFK") -> None:
        await inter.response.defer()
        await self.add_afk_to_user(inter.author, message, False)
        await inter.edit_original_response(
            content="You're now AFK, beware of the real world"
        )


setup = AFK.setup
