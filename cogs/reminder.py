from typing import List

from discord import Member, VoiceState, VoiceChannel
from discord.ext import commands

from config.config import config
from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Reminder(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self._bot = bot
        self._gm_id: int = config.REMINDER.GM_ID
        self._blacklisted: List[int] = config.REMINDER.BLACKLISTED_IDS
        self._voice_channel_id: int = config.REMINDER.VOICE_CHANNEL_ID
        self._gm_message: str = config.REMINDER.GM_MESSAGE
        self._others_message: str = config.REMINDER.OTHERS_MESSAGE

    @commands.Cog.listener()
    async def on_voice_state_update(
            self, member: Member, before: VoiceState, after: VoiceState
    ):
        await self.send_reminder(member, before, after)

    async def send_reminder(self, member: Member, before: VoiceState, after: VoiceState):
        voice_channel: VoiceChannel = self._bot.get_channel(self._voice_channel_id)
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

        gm = self._bot.get_user(self._gm_id)
        if gm == member:
            message = self._gm_message.format(mention=member.mention)
        else:
            message = self._others_message.format(mention=member.mention)

        await self._bot.send_message_to_text_channel(message)
