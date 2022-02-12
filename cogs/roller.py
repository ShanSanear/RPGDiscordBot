from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import List

from discord.ext import commands

import loggers
from rpg_discord_bot import RPGDiscordBot

ROLL_RE = re.compile(r"(?P<NumberOfDices>\d+)?[dkDK](?P<DiceSize>\d+)")


@dataclass
class RollResult:
    entry: str
    results: list[int]

    @property
    def complete_result(self):
        return sum(self.results)

    def __str__(self):
        if len(self.results) > 1:
            return f"**{self.complete_result}** ({'+'.join([str(value) for value in self.results])}) [{self.entry}]"
        else:
            return f"**{self.complete_result}** [{self.entry}]"

    def __repr__(self):
        return str(self)

    def __radd__(self, other: int):
        return other + self.complete_result


def get_roll_result(roll_entry: re.Match):
    try:
        number_of_dices = int(roll_entry['NumberOfDices'])
    except TypeError:
        number_of_dices = 1
    dice_size: int = int(roll_entry['DiceSize'])
    return RollResult(
        entry=f"{number_of_dices}d{dice_size}",
        results=[random.randint(1, dice_size) for _ in range(number_of_dices)]
    )


class Roller(commands.Cog):
    """
    Simple roller Cog
    """

    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, *rolls_to_roll):
        """
        Roll specified rolls
        :param ctx: Context
        :param rolls_to_roll Rolls to roll in format of NumberOfDices[dk]DiceSize, can provide multiple rolls split using spaces
        """
        roll_results: List[RollResult] = []

        for to_roll in rolls_to_roll:
            to_be_rolled = ROLL_RE.match(to_roll)
            if not to_be_rolled:
                await ctx.send(f"'{to_be_rolled}' has not been detected as roll")
                continue
            roll_results.append(get_roll_result(to_be_rolled))

        loggers.general_logger.debug("Roll results: %s", roll_results)

        await ctx.send(
            f"Your roll results: {' + '.join(str(result) for result in roll_results)} = **{sum(roll_results)}**")
