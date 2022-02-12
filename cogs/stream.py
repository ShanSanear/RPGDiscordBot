from discord.ext import commands

from rpg_discord_bot import RPGDiscordBot


class Stream(commands.Cog):
    """
    Cog which connects to streaming API on different machine
    """

    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor.
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

