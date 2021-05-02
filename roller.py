import random
import re
from collections import defaultdict
from typing import List

import discord
from discord.ext import commands

import loggers
from rpg_discord_bot import RPGDiscordBot

ROLL_RE = re.compile("(?P<NumberOfDices>\d+)[dkDK](?P<DiceSize>\d+)")


class Roller(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, *rolls_to_roll):
        """Roll specified rolls
        :param ctx: Context
        :param rolls_to_roll Rolls to roll in format of NumberOfDices[dk]DiceSize, can provide multiple rolls split using spaces
        """
        roll_results: List[tuple[str, int]] = []

        for to_roll in rolls_to_roll:
            to_be_rolled = ROLL_RE.match(to_roll)
            if not to_be_rolled:
                await ctx.send(f"'{to_be_rolled}' has not been detected as roll")
                continue
            number_of_dices = int(to_be_rolled.group('NumberOfDices'))
            dice_size = int(to_be_rolled.group('DiceSize'))
            current_roll_results = random.randint(number_of_dices, dice_size * number_of_dices + 1)
            roll_results.append((to_be_rolled.group(0), current_roll_results))

        rolls_with_values = []
        final_value = 0
        for roll_name, roll_result in roll_results:
            rolls_with_values.append(f"{roll_result} ({roll_name})")
            final_value += roll_result
        await ctx.send(f"Your roll results: {' + '.join(rolls_with_values)} = {final_value}")
