import discord
from discord.ext import commands
from discord.ext.commands import Context

from dependencies.ytdl_source import YTDLSource
from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Music(commands.Cog):
    """
    Simple Cog which lets bot play music.
    """

    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor.
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

    @commands.group(pass_context=True)
    async def music(self, ctx):
        """
        Music playing/streaming functionality, check help to find out more
        :param ctx:
        :return:
        """
        pass

    @music.command(pass_context=True)
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(
            source,
            after=lambda e: general_logger.error("Player error: %s", e) if e else None,
        )

        await ctx.send("Now playing: {}".format(query))

    @music.command(pass_context=True)
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player,
                after=lambda e: general_logger.error("Player error: %s", e)
                if e
                else None,
            )

        await ctx.send("Now playing: {} from: {}".format(player.title, player.url))

    @music.command(pass_context=True)
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player,
                after=lambda e: general_logger.error("Player error: %s", e)
                if e
                else None,
            )

        await ctx.send("Now playing: {} from: {}".format(player.title, player.url))

    @music.command(pass_context=True)
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @music.command(pass_context=True)
    async def stop(self, ctx: Context):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client is None:
            await ctx.channel.send("Nothing is being played right now")
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        else:
            await ctx.channel.send("Nothing is being played right now")

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx: Context):
        """
        Check to make sure bot is in some voice channel before playing anything.
        :param ctx: Context.
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                general_logger.debug("Joining authors voice channel")
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
