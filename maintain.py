import sys
import traceback
from datetime import datetime, timedelta

import discord
from discord import Member, TextChannel, Message
from discord.ext import commands
from discord.ext.commands import Context

from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Maintain(commands.Cog):
    """
    Cog which handles simple maintain tasks (such as joining channel, disconnecting etc)
    """
    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot
        self._users_to_be_followed = {}

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a specified voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def disconnect(self, ctx: Context):
        """Disconnects from currently connected voice channel"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to any voice channel at the moment")

        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down bot"""
        await self.bot.send_reminder_to_text_channel("Turning off")
        await ctx.bot.logout()
        await ctx.bot.close()

    @commands.command()
    @commands.is_owner()
    async def clear_today_messages(self, ctx: Context, number: str):
        """
        Clears messages created by bot today. Requires number of messages
        :param ctx: Message context
        :param number: number of messages
        """
        number = int(number)
        last_24_hours = datetime.utcnow() - timedelta(days=1)
        general_logger.info("Clearing messages from channel: %s since: %s", ctx.channel, last_24_hours)
        await ctx.channel.purge(limit=number, check=self.check_if_bot_is_author_of_message,
                                after=last_24_hours)

    def check_if_bot_is_author_of_message(self, message: Message):
        """
        Checks if bot is author of the message.
        :param message: Message being checked
        :return: True in case message has been created by bot or not
        """
        general_logger.debug("Message: %s, author: %s", message, message.author)
        return message.author == self.bot.user

    @commands.command()
    async def follow_another_user(self, ctx, user_to_be_followed: Member, user_following: Member):
        """
        TODO:
        Command which saves information about which user should follow who in voice channels
        :param ctx: Message context
        :param user_to_be_followed: Who should be followed
        :param user_following: Who should be following
        :return:
        """
        general_logger.debug("User to be followed: %s, User following: %s", user_to_be_followed, user_following)
        await ctx.send("Following...")


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
