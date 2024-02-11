from __future__ import annotations

import datetime
import typing

import disnake
from disnake.ext import commands

from utils import embeds
from yuna.core import YunaCog


class NoDatabaseEntry(Exception): ...


class EntryData(typing.TypedDict):
    action: str
    guild_id: int
    channel_id: int
    message: str
    image_url: str | None


def parser(message: str, member: disnake.Member) -> str:
    return message.format(
        **{
            "member_name": str(member),
            "member_id": str(member.id),
            "member_created_on": str(member.created_at),
            "member_avatar": member.display_avatar.url,
            "member": str(member),
            "server_name": member.guild.name,
            "server_id": str(member.guild.id),
            "server_icon": member.guild.icon.url if member.guild.icon.url else "",
            "server_member_count": str(len(member.guild.members)),
        }
    )


class MemberLogging(YunaCog):
    async def log_channel(
        self,
        action: typing.Literal["join", "leave"],
        guild_id: int,
        *,
        add: int | None = None,
    ) -> int | None:
        channel_id = await self.bot.pool.fetchval(
            "SELECT channel_id FROM member_logs WHERE action=$1 AND guild_id=$2",
            action,
            guild_id,
        )
        if not add:
            return channel_id
        if not channel_id:
            msg = (
                "Hey {member_mention}! welcome to {server_name}."
                if action == "join"
                else "{member_name} left the server."
            )
            await self.bot.pool.execute(
                "INSERT INTO member_logs VALUES ($1, $2, $3, $4)",
                action,
                guild_id,
                add,
                msg,
            )
            return
        await self.bot.pool.execute(
            "UPDATE member_logs SET channel_id=$1 WHERE guild_id=$2 AND action=$3",
            add,
            guild_id,
            action,
        )

    async def update_message(
        self, guild_id: int, action: typing.Literal["join", "leave"], message: str
    ) -> None:
        channel = await self.log_channel(action, guild_id)
        if not channel:
            raise NoDatabaseEntry()
        await self.bot.pool.execute(
            "UPDATE member_logs SET message=$1 WHERE guild_id=$2 AND action=$3",
            message,
            guild_id,
            action,
        )

    async def send_message(
        self, action: typing.Literal["join", "leave"], member: disnake.Member
    ) -> None:
        data: EntryData | None = await self.bot.pool.fetchrow(
            "SELECT * FROM member_logs WHERE guild_id=$1 AND action=$2",
            member.guild.id,
            action,
        )
        if not data.get("channel_id"):
            return
        try:
            await self.bot.get_partial_messageable(
                data["channel_id"], type=disnake.ChannelType.text
            ).send(
                embed=disnake.Embed(
                    color=member.accent_color or disnake.Color.random(),
                    description=parser(data["message"], member),
                    timestamp=datetime.datetime.now(),
                ).set_author(name=member.name, url=member.display_avatar.url)
            )

        except disnake.HTTPException:
            ...

    async def set_channel(
        self, action: str, inter: disnake.CmdInter, channel: disnake.TextChannel
    ) -> None:
        action = (
            "join"
            if inter.application_command.qualified_name == "welcome channel"
            else "leave"
        )
        await inter.response.defer()
        await self.log_channel(action, inter.guild_id, add=channel.id)
        await inter.edit_original_response(
            embed=embeds.success_embed(
                inter, f"{action.title()} has been set to {channel.mention}"
            )
        )

    @commands.Cog.listener(disnake.Event.member_join)
    async def new_member(self, member: disnake.Member) -> None:
        await self.send_message("join", member)

    @commands.Cog.listener(disnake.Event.member_remove)
    async def left_member(self, member: disnake.Member) -> None:
        await self.send_message("leave", member)

    @commands.has_permissions(manage_guild=True)
    @commands.slash_command(name="welcome")
    async def welcome(self, _: disnake.CmdInter) -> None: ...

    @commands.has_permissions(manage_guild=True)
    @commands.slash_command(name="goodbye")
    async def goodbye(self, _: disnake.CmdInter) -> None: ...

    @commands.has_permissions(manage_guild=True)
    @welcome.sub_command(name="channel", description="Edit the channel to send logs in")
    async def welcome_channel(
        self, inter: disnake.CmdInter, channel: disnake.TextChannel
    ) -> None:
        await self.set_channel("join", inter, channel)

    @commands.has_permissions(manage_guild=True)
    @goodbye.sub_command(name="channel", description="Edit the channel to send logs in")
    async def goodbye_channel(
        self, inter: disnake.CmdInter, channel: disnake.TextChannel
    ) -> None:
        await self.set_channel("leave", inter, channel)

    @commands.has_permissions(manage_guild=True)
    @welcome.sub_command(
        name="message", description="Edit the message to send in the logs"
    )
    async def welcome_message(self, inter: disnake.CmdInter, message: str) -> None:
        await inter.response.defer()
        await self.update_message(inter.guild_id, "join", message)
        await inter.edit_original_response(
            embed=embeds.success_embed(inter, "Message has been updated")
        )

    @commands.has_permissions(manage_guild=True)
    @goodbye.sub_command(
        name="message", description="Edit the message to send in the logs"
    )
    async def goodbye_message(self, inter: disnake.CmdInter, message: str) -> None:
        await inter.response.defer()
        await self.update_message(inter.guild_id, "leave", message)
        await inter.edit_original_response(
            embed=embeds.success_embed(inter, "Message has been updated")
        )


setup = MemberLogging.setup
