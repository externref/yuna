from __future__ import annotations

import datetime
import typing

import disnake
from disnake.ext import commands

from utils import embeds
from yuna.core import YunaCog


class ConfessionData(typing.TypedDict):
    id: int
    user_id: int
    guild_id: int
    message_content: str
    created_on: datetime.datetime


class Confessions(YunaCog):
    @commands.slash_command(name="confession")
    async def _confess(self, _: disnake.CmdInter) -> None:
        """Write your confession message here."""

    async def guild_channel(
        self, guild_id: int, *, set_id: int | None = None
    ) -> int | None:
        result: int | None = await self.bot.pool.fetchval(
            "SELECT channel_id FROM confession_configs WHERE guild_id=$1", guild_id
        )
        if not set_id:
            return result
        if not result:
            await self.bot.pool.execute(
                """
                INSERT INTO confession_configs
                VALUES ($1, $2);
                """,
                guild_id,
                set_id,
            )
            return
        await self.bot.pool.execute(
            """
            UPDATE confession_configs
            SET channel_id = $1 WHERE guild_id = $2;
            """,
            set_id,
            guild_id,
        )

    async def member_ban(
        self, guild_id: int, member_id: int, *, ban: bool = False, reason: str = ""
    ) -> None:
        is_banned = await self.bot.pool.fetch(
            "SELECT user_id FROM confession_bans WHERE guild_id=$1 AND user_id=$2",
            guild_id,
            member_id,
        )
        print(is_banned)
        if not ban:
            return is_banned
        if not is_banned:
            await self.bot.pool.execute(
                "INSERT INTO confession_bans VALUES ($1, $2, $3)",
                member_id,
                guild_id,
                reason,
            )

    @commands.has_guild_permissions(ban_members=True)
    @_confess.sub_command("channel", "Setup the slash command channel.")
    async def set_channel(
        self, inter: disnake.CmdInter, channel: disnake.TextChannel
    ) -> None:
        """Set the channel where message will be sent

        Parameters
        ----------
        channel: The channel to set.
        """
        await self.guild_channel(inter.guild_id, set_id=channel.id)
        await inter.send(
            embed=embeds.success_embed(
                inter, f"Confession channel has been set to {channel.mention}!"
            )
        )

    @commands.has_guild_permissions(ban_members=True)
    @_confess.sub_command(
        "ban", "Ban the member who created the confession using the confession ID"
    )
    async def ban_member(
        self, inter: disnake.CmdInter, c_id: int, reason: str | None = None
    ) -> None:
        """Bans the member who is spreading hatred

        Parameters
        ----------
        ban: Banned the members.
        """
        await inter.response.defer(ephemeral=True)
        data: ConfessionData | None = await self.bot.pool.fetchrow(
            "SELECT * FROM confession_messages WHERE guild_id=$1 AND id=$2",
            inter.guild_id,
            c_id,
        )
        if data is None:
            await inter.edit_original_response(
                embed=embeds.fail_embed(inter, "Confession not found")
            )
            return
        await self.member_ban(
            data["guild_id"],
            data["user_id"],
            ban=True,
            reason=reason or "No reason provided",
        )
        await inter.edit_original_response(
            embed=embeds.success_embed(
                inter, "The user who posted the confession was banned from confessions."
            )
        )

    @_confess.sub_command("create", "Create a confession")
    async def create_confession(self, inter: disnake.CmdInter, message: str) -> None:
        """set your confession message."""
        await inter.response.defer(ephemeral=True)
        if (channel := await self.guild_channel(inter.guild_id)) is None:
            await inter.edit_original_response(
                embed=embeds.fail_embed(
                    inter, "No confession channel set for this server."
                )
            )
            return
        if await self.member_ban(inter.guild_id, inter.user.id):
            await inter.edit_original_response(
                embed=embeds.fail_embed(
                    inter,
                    "You have been banned from making confessions in this server.",
                ),
            )
            return
        num_confessions = await self.bot.pool.fetchval(
            "SELECT COUNT(*) FROM confession_messages WHERE guild_id=$1", inter.guild_id
        )
        embed = (
            embeds.BaseEmbed(
                inter,
                color=disnake.Color.purple(),
                description=message,
                title=f"#{num_confessions+1}",
                timestamp=datetime.datetime.now(),
            )
            .remove_footer()
            .set_thumbnail((inter.guild.icon or inter.author.display_avatar).url)
        )

        try:
            await self.bot.get_partial_messageable(
                channel, type=disnake.ChannelType.text
            ).send(embed=embed)
        except disnake.HTTPException:
            await inter.edit_original_response(
                embed=embeds.fail_embed(
                    "Sending confession failed, please contact a server admin/manager to update confession channel access for bot."
                )
            )
        await inter.edit_original_response(
            embed=embeds.success_embed(
                inter, text=f"Your confession has been sent in <#{channel}>!"
            )
        )
        await self.bot.pool.execute(
            """
            INSERT INTO confession_messages
            VALUES ($1, $2, $3, $4)
            """,
            num_confessions + 1,
            message,
            inter.guild_id,
            inter.user.id,
        )


setup = Confessions.setup
