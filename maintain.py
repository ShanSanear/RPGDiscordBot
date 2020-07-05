import discord
from discord.ext import commands

from rpg_discord_bot import RPGDiscordBot


class Maintain(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.send_message_to_text_channel("Turning off")
        await ctx.bot.logout()
        await ctx.bot.close()
