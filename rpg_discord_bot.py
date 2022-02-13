import logging
from datetime import datetime, timedelta
from typing import Iterator

from discord import TextChannel
from discord.ext import commands

from config.config import config
from loggers import general_logger


class RPGDiscordBot(commands.Bot):
    def __init__(self, command_prefix: str):
        """
        Constructor for main bot class.
        :param command_prefix: prefix for commands
        """
        super(RPGDiscordBot, self).__init__(command_prefix)
        self._streaming_api_endpoint: str = config.STREAM.API_ENDPOINT
        self._text_channel_id: int = config.REMINDER.TEXT_CHANNEL_ID

    async def on_ready(self):
        """
        Logging information when on_ready event is being called
        """
        general_logger.info("Logged in as: %s [ID: %d]", self.user.name, self.user.id)

    @property
    def streaming_api_endpoint(self):
        return self._streaming_api_endpoint

    async def send_message_to_text_channel(self, message: str):
        """
        Send reminder to default text channel
        :param message: message to be send
        """
        text_channel: TextChannel = self.get_channel(self._text_channel_id)
        if text_channel is None:
            logging.warning("Couldn't find channel with configured id %s. Message to be sent: %s",
                            self._text_channel_id, message)
            return
        last_12_hours: datetime.date = datetime.utcnow() - timedelta(hours=12)
        last_messages: Iterator[str] = [message.content for message in
                                        await text_channel.history(after=last_12_hours).flatten()]
        if message in last_messages:
            general_logger.debug("Message %s appeared in the last 12 hours, skipping", message)
            return
        await text_channel.send(message)

