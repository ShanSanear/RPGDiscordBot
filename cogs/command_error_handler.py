import sys
import traceback

import discord
from discord.ext import commands

from loggers import general_logger


class CommandErrorHandler(commands.Cog):
    """
    Makes it easier to handle command errors.
    """

    def __init__(self, bot):
        """
        Constructor
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            general_logger.error('Exception type: %s', type(error))
            general_logger.error('Exception Value: %s', error)
            general_logger.error('Exception traceback: %s', traceback.extract_stack(error))