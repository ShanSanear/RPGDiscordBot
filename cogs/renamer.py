from typing import Optional, Dict, List

from discord import Member, User
from discord.ext import commands
from discord.ext.commands import Context


class Renamer(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        # TODO - make it database based
        self.renaming_mapping: Dict[str, Dict[int, str]] = {}
        self._current_profile = None

    @commands.group(pass_context=True)
    async def profile(self, ctx: Context):
        return

    @profile.command(name='show', pass_context=True)
    async def show_profile(self, ctx):
        await ctx.send(f"Current profile: {self._current_profile}")
        message = ""
        for user_id, name_to_set in self.renaming_mapping[self._current_profile].items():
            members: List[Member] = await ctx.message.guild.query_members(user_ids=[user_id])
            member = members[0]
            message += f"{member} has name set for this profile to '{name_to_set}'\n"
        await ctx.send(message)
        await ctx.send(f"All profiles: {','.join(self.renaming_mapping.keys())}")

    @profile.command(name='delete', pass_context=True)
    async def delete_profile(self, ctx, profile_to_delete: str):
        if profile_to_delete in self.renaming_mapping:
            del self.renaming_mapping[profile_to_delete]
            await ctx.send(f"Deleted profile '{profile_to_delete}' from renaming mapping")
        else:
            await ctx.send(f"Profile '{profile_to_delete}' has not been created")

    @profile.command(name='set', pass_context=True)
    async def set_profile(self, ctx, profile_name):
        """
        Sets the profile and if it's not available - creates it
        :param ctx: Context
        :param profile_name: Profile name
        """
        self._current_profile = profile_name
        if profile_name in self.renaming_mapping:
            await ctx.send(f"Profile has been set to '{profile_name}'")
        else:
            self.renaming_mapping[profile_name] = {}
            await ctx.send(f"Profile '{profile_name}' has been created")

    @profile.command(name='rename', pass_context=True)
    async def rename_profile(self, ctx, rename_to_profile):
        """
        Renames current profile
        :param ctx: Context
        :param rename_to_profile: To what rename the profile
        """
        if not self._current_profile:
            await ctx.send("No profile currently selected")
            return
        self.renaming_mapping[rename_to_profile] = self.renaming_mapping[self._current_profile]
        del self.renaming_mapping[self._current_profile]
        await ctx.send(f"Renamed profile from {self._current_profile} to {rename_to_profile}")
        self._current_profile = rename_to_profile

    @profile.command(name='add', pass_context=True)
    async def add_to_profile(self, ctx, member: User, name_to_be_set: str):
        """
        Adds given user to profile with name for given profile
        :param ctx: Context
        :param member: Member (user) that is being added to profile
        :param name_to_be_set: Which name to set for member
        """
        if not self._current_profile:
            await ctx.send("No profile is being set")
            return
        self.renaming_mapping[self._current_profile][member.id] = name_to_be_set
        await ctx.send(f"Set name {name_to_be_set} for {member} in profile {self._current_profile}")

    @profile.command(name='apply', pass_context=True)
    async def apply_profile(self, ctx: Context, profile_to_apply: Optional[str] = None):
        """
        Applies given profile
        :param ctx: Context
        :param profile_to_apply: Optional, profile that needs to be applied, by default uses current profile
        """
        if not profile_to_apply:
            profile_to_apply = self._current_profile
        await ctx.send(f"Applying profile {profile_to_apply}")
        for user_id, name_to_set in self.renaming_mapping[profile_to_apply].items():
            members = await ctx.message.guild.query_members(user_ids=[user_id])
            member = members[0]
            await member.edit(nick=name_to_set, reason=f'Setting name for profile: {profile_to_apply}')
