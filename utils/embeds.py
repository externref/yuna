from __future__ import annotations

import typing

import disnake
from disnake.ext import commands

from utils.emojis import Emojis

InvocationT = typing.Union[commands.Context, disnake.CmdInter]


class BaseEmbed(disnake.Embed):
    def __init__(
        self, ctx_or_inter: InvocationT, *, footer: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.set_footer(
            text=footer or ctx_or_inter.bot.user.name,
            icon_url=ctx_or_inter.bot.user.display_avatar,
        )


def success_embed(ctx_or_inter: InvocationT, text: str) -> BaseEmbed:
    return BaseEmbed(
        ctx_or_inter,
        description=f"{Emojis.SUCCESS} | {text}",
        color=disnake.Color.green(),
    )


def fail_embed(ctx_or_inter: InvocationT, text: str) -> BaseEmbed:
    return BaseEmbed(
        ctx_or_inter, description=f"{Emojis.FAIL} | {text}", color=disnake.Color.red()
    )
