from collections import defaultdict
from typing import Set, Dict

from discord import Member, VoiceState, Status
from discord.ext import commands
from discord.ext.commands import Context

from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Follower(commands.Cog):
    def __init__(self, bot: RPGDiscordBot):
        self.bot = bot
        self._following_mapping: Dict[Member, Set[Member]] = defaultdict(set)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        await self._process_following(member, before, after)

    async def _process_following(self, being_followed: Member, before: VoiceState, after: VoiceState):
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
                await self.bot.send_message_to_text_channel(f"{being_followed} disconnected, won't move {follower}")
            if follower.voice.channel != being_followed_voice_channel:
                await self.bot.send_message_to_text_channel(
                    f"Moving {follower} to follow {being_followed} into channel {being_followed_voice_channel}")
                general_logger.info("Moving %s to follow %s into channel '%s'",
                                    follower, being_followed, being_followed_voice_channel)
                await follower.move_to(being_followed_voice_channel, reason="Following...")

    @commands.command()
    async def follow_another_user(self, ctx: Context, user_to_be_followed: Member, user_following: Member):
        """
        Command which saves information about which user should follow who in voice channels
        :param ctx: Message context
        :param user_to_be_followed: Who should be followed
        :param user_following: Who should be following
        """
        general_logger.debug("User to be followed: %s, User following: %s", user_to_be_followed, user_following)
        await ctx.send(f"User to be followed: {user_to_be_followed}, User following: {user_following}")
        self._following_mapping[user_to_be_followed].add(user_following)

    @commands.command()
    async def stop_follow_another_user(self, ctx: Context, user_being_followed: Member, user_following: Member):
        """
        Stops user from being followed
        :param ctx: Message context
        :param user_being_followed: Who is being currently followed
        :param user_following: Who is following
        """
        general_logger.debug("User being followed: %s, User that will no longer follow: %s", user_being_followed,
                             user_following)
        await ctx.send(f"User {user_being_followed} will no longer be followed by {user_following}")
        self._following_mapping[user_being_followed].remove(user_following)

    @commands.command()
    async def show_current_followers(self, ctx: Context):
        """
        Shows who is followed by who.
        :param ctx: Message context
        """
        for being_followed, followers in self.bot.following_mapping.items():
            await ctx.send(f"{being_followed} is being followed by {','.join(str(follower) for follower in followers)}")



