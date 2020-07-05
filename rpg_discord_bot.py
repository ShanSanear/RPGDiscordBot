from typing import List

from discord import TextChannel, Member, VoiceState, VoiceChannel
from discord.ext import commands

from loggers import general_logger


class RPGDiscordBot(commands.Bot):

    def __init__(self, command_prefix, config_data):
        super(RPGDiscordBot, self).__init__(command_prefix)
        self._config = config_data
        self._gm_id: int = self._config['REMINDER']['GM_ID']
        self._blacklisted: List[int] = self._config['REMINDER']['BLACKLISTED_IDS']
        self._text_channel_id: int = self._config['REMINDER']['TEXT_CHANNEL_ID']
        self._voice_channel_id: int = self._config['REMINDER']['VOICE_CHANNEL_ID']
        self._gm_message: str = self._config['REMINDER']['GM_MESSAGE']
        self._others_message: str = self._config['REMINDER']['OTHERS_MESSAGE']

    async def on_ready(self):
        general_logger.info("Logged in as: %s [ID: %d]", self.user.name, self.user.id)

    async def send_message_to_text_channel(self, message):
        text_channel: TextChannel = self.get_channel(self._text_channel_id)
        await text_channel.send(message)

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.id in self._blacklisted:
            general_logger.debug("User %s is in black list for reminder", member)
            return
        voice_channel: VoiceChannel = self.get_channel(self._voice_channel_id)
        if voice_channel != after.channel:
            return
        if before.channel == after.channel:
            general_logger.debug("User %s is in the same channel still, skipping", member)
            return

        gm = self.get_user(self._gm_id)
        if gm == member:
            message = self._gm_message.format(mention=member.mention)
        else:
            message = self._others_message.format(mention=member.mention)

        await self.send_message_to_text_channel(message)
