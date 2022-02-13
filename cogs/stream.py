import asyncio
import json
from urllib.parse import urljoin

import requests
from discord.ext import commands
from discord.ext.commands import Context

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
        self._obs_response = {}

    @commands.group(pass_context=True)
    async def stream(self, ctx: Context):
        pass

    @stream.command(pass_context=True)
    async def start(self, ctx: Context):
        """
        Start stream
        :param ctx:
        :return:
        """
        general_logger.info("Starting OBS stream...")
        if not self._obs_on:
            self._obs_response = await self._turn_on_obs()
            await ctx.send("Waiting for OBS to be turned on...")
            await asyncio.sleep(5)
        await self._start_obs_stream()
        self._stream_on = True
        await ctx.send("Starting **recording** (DEBUG)")

    @stream.command(pass_context=True)
    async def stop(self, ctx: Context):
        if not self._obs_on:
            general_logger.warning("Obs is not turned on")
            return
        if not self._stream_on:
            general_logger.warning("Stream is not turned on")
            return
        general_logger.info("Stopping OBS stream...")
        await ctx.send("Stopping **recording** (DEBUG)")
        await self._stop_obs_stream()
        await self._turn_off_obs()

    async def _turn_on_obs(self):
        general_logger.info("Turning on obs...")
        response = requests.post(urljoin(self._obs_endpoint, "run"))
        response.raise_for_status()
        self._obs_on = True
        return response.json()

    async def _turn_off_obs(self):
        general_logger.info("Turning on obs...")
        response = requests.post(urljoin(self._obs_endpoint, "stop"), json=self._obs_response)
        response.raise_for_status()
        self._obs_on = False
        self._obs_response = {}
        general_logger.info("Turn off OBS response: %s", response.json())

    async def _start_obs_stream(self):
        general_logger.info("Starting recording...")
        requests.post(urljoin(self._obs_endpoint, "recording/start"))

    async def _stop_obs_stream(self):
        general_logger.info("Stopping recording...")
        requests.post(urljoin(self._obs_endpoint, "recording/stop"))
