from datetime import datetime, timedelta

import discord
from discord import Message, Member
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

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a specified voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        else:
            await ctx.send(f"Couldn't find channel: {channel}")

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
        await self.bot.send_message_to_text_channel("Turning off")
        await ctx.bot.close()

    @commands.command()
    @commands.is_owner()
    async def clear_today_messages(self, ctx: Context, number: int):
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
    async def change_nick(self, ctx: Context, member_to_change: Member, name: str, reason=None):
        """
        Changes nick of given Member
        :param ctx: Context
        :param member_to_change: Member which name is being changed
        :param name: Name to be changed to
        :param reason: Optional, reason for the change
        """
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send(f"User {ctx.message.author} is not an administrator")
            return
        await ctx.send(f"Changing name of {member_to_change} to {name}")
        await member_to_change.edit(nick=name, reason=reason)
