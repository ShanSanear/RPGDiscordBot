import asyncio
from urllib.parse import urljoin

from discord.ext import commands
from discord.ext.commands import Context

from dependencies.utils import call_endpoint_post
from loggers import general_logger
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
        self._obs_endpoint = urljoin(self.bot.streaming_api_endpoint, "obs/")
        self._obs_on = False
        self._stream_on = False
        self._recording_on = False
        self._obs_response = {}

    def _call_api_get(self, endpoint):
        pass

    @commands.group(pass_context=True)
    @commands.is_owner()
    async def obs(self, ctx: Context):
        """
        OBS related commands, check help for more info
        :param ctx:
        :return:
        """
        pass

    @obs.command(name='start', pass_context=True)
    @commands.is_owner()
    async def start_obs(self, ctx: Context):
        """
        Start OBS application on recording machine
        """
        await self.run_obs_if_turned_off(ctx)

    @commands.is_owner()
    @obs.command(name='stop', pass_context=True)
    async def stop_obs(self, ctx: Context):
        """
        Stop OBS application on recording machine
        """
        await self.turn_off_obs_if_turned_on(ctx)

    @commands.is_owner()
    @obs.group(pass_context=True, invoke_without_command=True)
    async def record(self, ctx: Context):
        """
        Manage OBS recording, check help for more info
        """

    @commands.is_owner()
    @record.command(name='start', pass_context=True)
    async def start_record(self, ctx: Context):
        """
        Start OBS recording
        """
        if not self._obs_on:
            general_logger.info("OBS is not turned on")
            await ctx.send("OBS is not turned on")
            return
        general_logger.info("Starting recording...")
        await self._start_obs_recording()
        self._recording_on = True
        await ctx.send("Starting OBS **recording**")

    @commands.is_owner()
    @record.command(name='stop', pass_context=True)
    async def stop_record(self, ctx: Context):
        """
        Stop OBS recording
        """
        general_logger.info("Stopping recording...")
        if not self._obs_on:
            general_logger.warning("Obs is not turned on")
            await ctx.send("OBS is not turned on")
            return
        if not self._recording_on:
            general_logger.warning("Recording is not turned on")
            await ctx.send("Recording is not turned on")
            return
        await self._stop_obs_recording()
        await ctx.send("Stopped OBS **recording**")

    @commands.is_owner()
    @obs.group(pass_context=True, invoke_without_command=True)
    async def stream(self, ctx: Context):
        """
        Manage OBS stream, check help for more info
        """
        pass

    @commands.is_owner()
    @stream.command(name='start', pass_context=True)
    async def start_stream(self, ctx: Context):
        """
        Start OBS stream
        """
        if not self._obs_on:
            general_logger.info("OBS is not turned on")
            await ctx.send("OBS is not turned on")
            return
        await self._start_obs_stream()
        self._stream_on = True
        await ctx.send("Starting OBS **stream**")

    async def run_obs_if_turned_off(self, ctx):
        if not self._obs_on:
            self._obs_response = await self._turn_on_obs()
            await ctx.send("Waiting for OBS to be turned on...")
            await asyncio.sleep(5)

    async def turn_off_obs_if_turned_on(self, ctx):
        if self._obs_on:
            self._obs_response = await self._turn_off_obs()

    @commands.is_owner()
    @stream.command(name='stop', pass_context=True)
    async def stop_stream(self, ctx: Context):
        """
        Stop OBS stream
        """
        if not self._obs_on:
            general_logger.warning("Obs is not turned on")
            await ctx.send("OBS is not turned on")
            return
        if not self._stream_on:
            general_logger.warning("Stream is not turned on")
            await ctx.send("Stream is not turned on")
            return
        general_logger.info("Stopping OBS stream...")
        await self._stop_obs_stream()
        await ctx.send("Stopped OBS **stream**")

    async def _turn_on_obs(self) -> dict:
        """
        Turns on OBS
        :return: API response
        """
        general_logger.info("Turning on obs...")
        response = call_endpoint_post(urljoin(self._obs_endpoint, "run"))
        self._obs_on = True
        return response.json()

    async def _turn_off_obs(self):
        """
        Turns off OBS
        :return: API response
        """
        general_logger.info("Turning off obs...")
        response = call_endpoint_post(urljoin(self._obs_endpoint, "stop"), json=self._obs_response)
        self._obs_on = False
        self._obs_response = {}
        general_logger.info("Turn off OBS response: %s", response.json())
        return response.json()

    async def _start_obs_stream(self):
        general_logger.info("Starting stream...")
        call_endpoint_post(endpoint=urljoin(self._obs_endpoint, "stream/start"), )

    async def _stop_obs_stream(self):
        general_logger.info("Stopping stream...")
        call_endpoint_post(endpoint=urljoin(self._obs_endpoint, "stream/stop"), )

    async def _start_obs_recording(self):
        general_logger.info("Starting recording...")
        call_endpoint_post(endpoint=urljoin(self._obs_endpoint, "recording/start"))

    async def _stop_obs_recording(self):
        general_logger.info("Stopping recording...")
        call_endpoint_post(endpoint=urljoin(self._obs_endpoint, "recording/start"))
