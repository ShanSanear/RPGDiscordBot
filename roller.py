import random
import re
import discord
from discord.ext import commands

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
        roll_results = {}
        for to_roll in rolls_to_roll:
            if to_be_rolled := ROLL_RE.match(to_roll):
                number_of_dices = int(to_be_rolled.group('NumberOfDices'))
                dice_size = int(to_be_rolled.group('DiceSize'))
                current_roll = []
                for dice_number in range(1, number_of_dices + 1):
                    current_roll.append(random.randint(1, dice_size))
                roll_results[to_be_rolled.group(0)] = current_roll


        # await ctx.send(f"Your roll results: {' + '.join(roll_results.values())}")
        # await ctx.send(f"Combined roll result: {sum((int(val) for val in roll_results.values()))}")

