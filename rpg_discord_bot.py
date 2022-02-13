import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Iterator, Dict, Set

from discord import TextChannel, Member, VoiceState, VoiceChannel, Status
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
        self._gm_id: int = config.REMINDER.GM_ID
        self._blacklisted: List[int] = config.REMINDER.BLACKLISTED_IDS
        self._text_channel_id: int = config.REMINDER.TEXT_CHANNEL_ID
        self._voice_channel_id: int = config.REMINDER.VOICE_CHANNEL_ID
        self._gm_message: str = config.REMINDER.GM_MESSAGE
        self._others_message: str = config.REMINDER.OTHERS_MESSAGE
        self._streaming_api_endpoint: str = config.STREAM.API_ENDPOINT
        self._following_mapping: Dict[Member, Set[Member]] = defaultdict(set)

    async def on_ready(self):
        """
        Logging information when on_ready event is being called
        """
        general_logger.info("Logged in as: %s [ID: %d]", self.user.name, self.user.id)

    @property
    def following_mapping(self):
        return self._following_mapping

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

    async def on_voice_state_update(
            self, member: Member, before: VoiceState, after: VoiceState
    ):
        """
        Being run on voice state update being detected
        :param member: member which is being affected by voice state change
        :param before: state before update
        :param after: state after update
        """
        await self.send_reminder(member, before, after)

    async def send_reminder(self, member: Member, before: VoiceState, after: VoiceState):
        """
        Send reminder about message provided earlier.
        :param member: member which is being affected by voice state change
        :param before: state before update
        :param after: state after update
        """
        voice_channel: VoiceChannel = self.get_channel(self._voice_channel_id)
        if voice_channel != after.channel:
            return
        if before.channel == after.channel:
            general_logger.debug(
                "User %s is in the same channel still, skipping", member
            )
            return
        if member.id in self._blacklisted:
            general_logger.debug("User %s is in black list for reminder", member)
            return

        gm = self.get_user(self._gm_id)
        if gm == member:
            message = self._gm_message.format(mention=member.mention)
        else:
            message = self._others_message.format(mention=member.mention)

        await self.send_message_to_text_channel(message)