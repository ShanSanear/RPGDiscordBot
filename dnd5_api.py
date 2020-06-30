import logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from loggers import general_logger



class DnD5Api(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, what_for, query):
        general_logger.debug("Searching for: %s using query: %s", what_for, query)
