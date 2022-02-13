from typing import Iterator

from discord.ext import commands
from discord.ext.commands import Context

from cogs.dnd5_api.resource.errors import ResourceNotFound
from cogs.dnd5_api.resource.spell import Spell
from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class DnD5Api(commands.Cog):
    """
    Cog representing access to the DND5E API
    """
    _classes = {"spell": Spell}

    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

    @commands.command()
    async def search(self, ctx: Context, what_for: str, name: str, *fields_to_show: Iterator[str]):
        """Searches for spell (for now) using its name.
        :param ctx - message context
        :param what_for - what are you searching for (for now - only spell)
        :param name - name of the spell
        :param fields_to_show - space separated fields to show; Name, Description, Components, Range, Higher_level"""
        if what_for not in self._classes:
            raise NotImplementedError
        if not fields_to_show:
            fields_to_show = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        async with ctx.typing():
            cls = self._classes[what_for]
            try:
                search_instance = cls(name)
                search_instance.fetch_by_name()
                message = search_instance.get_formatted_message(fields_to_show)
                await ctx.send(message)
            except ResourceNotFound:
                await ctx.send(f"Spell not found: {name}")
