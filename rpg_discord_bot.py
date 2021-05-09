from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Iterator, Dict, Set

from discord import TextChannel, Member, VoiceState, VoiceChannel, Message
from discord.ext import commands

from loggers import general_logger


class RPGDiscordBot(commands.Bot):
    def __init__(self, command_prefix: str, config_data: dict):
        """
        Constructor for main bot class.
        :param command_prefix: prefix for commands
        :param config_data: configuration loaded from TOML file
        """
        super(RPGDiscordBot, self).__init__(command_prefix)
        self._config: dict = config_data
        self._gm_id: int = self._config["REMINDER"]["GM_ID"]
        self._blacklisted: List[int] = self._config["REMINDER"]["BLACKLISTED_IDS"]
        self._text_channel_id: int = self._config["REMINDER"]["TEXT_CHANNEL_ID"]
        self._voice_channel_id: int = self._config["REMINDER"]["VOICE_CHANNEL_ID"]
        self._gm_message: str = self._config["REMINDER"]["GM_MESSAGE"]
        self._others_message: str = self._config["REMINDER"]["OTHERS_MESSAGE"]
        self._following_mapping: Dict[Member, Set[Member]] = defaultdict(set)

    async def on_ready(self):
        """
        Logging information when on_ready event is being called
        """
        general_logger.info("Logged in as: %s [ID: %d]", self.user.name, self.user.id)

    async def send_reminder_to_text_channel(self, message: str):
        """
        Send reminder to default text channel
        :param message: message to be send
        """
        text_channel: TextChannel = self.get_channel(self._text_channel_id)
        last_12_hours: datetime.date = datetime.utcnow() - timedelta(hours=12)
        last_messages: Iterator[Message] = await text_channel.history(after=last_12_hours).flatten()
        last_messages: Iterator[Message] = (message.content for message in last_messages)
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
        await self.process_following(member, before, after)

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

        await self.send_reminder_to_text_channel(message)

    def add_user_to_be_followed(self, being_followed: Member, following: Member):
        """
        Makes user be followed by another user
        :param being_followed: User that is to be followed
        :param following: User that will be following
        """
        self._following_mapping[being_followed].add(following)

    async def process_following(self, member: Member, before: VoiceState, after: VoiceState):
        """
        Processes following mapping - in case user changes its voice channel
        :param member: User that voice change was happening for
        :param before: Before state of the user
        :param after: After state of the user
        """
        if member not in self._following_mapping:
            general_logger.debug("Member changed: %s is not in following mapping", member)
            return
        if before.channel == after.channel:
            return
        being_followed_voice_channel = after.channel
        for follower in self._following_mapping[member]:
            if follower.voice:
                follower_voice_channel = follower.voice.channel
            else:
                follower_voice_channel = None
            if follower_voice_channel != being_followed_voice_channel:
                general_logger.info("Moving %s to follow %s into channel '%s'",
                                    follower, member, being_followed_voice_channel)
                await follower.move_to(being_followed_voice_channel, reason="Following...")
