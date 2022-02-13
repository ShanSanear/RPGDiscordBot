from collections import defaultdict
from typing import Set, Dict

from discord import Member, VoiceState, Status
from discord.ext import commands

from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Follower(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self._bot = bot
        self._following_mapping: Dict[Member, Set[Member]] = defaultdict(set)

    @commands.Cog.listener()
    def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        self._process_following(member, before, after)

    def _process_following(self, being_followed: Member, before: VoiceState, after: VoiceState):
        """
        Processes following mapping - in case user changes its voice channel
        :param being_followed: User that voice change was happening for
        :param before: Before state of the user
        :param after: After state of the user
        """
        if being_followed not in self._following_mapping:
            general_logger.debug("Member changed: %s is not in following mapping", being_followed)
            return
        if before.channel == after.channel:
            return
        being_followed_voice_channel = after.channel
        for follower in self._following_mapping[being_followed]:
            if follower.status == Status.offline:
                continue
            if not follower.voice:
                continue
            if not being_followed_voice_channel:
                await self._bot.send_message_to_text_channel(f"{being_followed} disconnected, won't move {follower}")
            if follower.voice.channel != being_followed_voice_channel:
                await self._bot.send_message_to_text_channel(
                    f"Moving {follower} to follow {being_followed} into channel {being_followed_voice_channel}")
                general_logger.info("Moving %s to follow %s into channel '%s'",
                                    follower, being_followed, being_followed_voice_channel)
                await follower.move_to(being_followed_voice_channel, reason="Following...")



