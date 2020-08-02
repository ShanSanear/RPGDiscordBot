from datetime import datetime, timedelta

import discord
from discord import VoiceClient
from discord.ext import commands
from discord.ext.commands import Context

from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Maintain(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self.bot = bot

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
            return await ctx.send("Not connected to any voice channel at the momend")

        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down bot"""
        await self.bot.send_message_to_text_channel("Turning off")
        await ctx.bot.logout()
        await ctx.bot.close()

    @commands.command()
    @commands.is_owner()
    async def clear_today_messages(self, ctx: Context, number):
        number = int(number)
        last_24_hours = datetime.utcnow() - timedelta(days=1)
        general_logger.info("Clearing messages from channel: %s since: %s", ctx.channel, last_24_hours)
        await ctx.channel.purge(limit=number, check=lambda message: message.author == self.bot.user,
                                before=last_24_hours)
