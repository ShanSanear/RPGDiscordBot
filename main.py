import os

from discord import TextChannel, VoiceState, VoiceChannel, Member
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
text_channel_id = int(os.getenv("TEXT_CHANNEL_ID"))
voice_channel_id = int(os.getenv("VOICE_CHANNEL_ID"))
gm_id = int(os.getenv("GM_ID"))


class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


bot = MyBot('!')


async def remind_gm_about_recording(after, member):
    text_channel: TextChannel = bot.get_channel(text_channel_id)
    voice_channel: VoiceChannel = bot.get_channel(voice_channel_id)
    if voice_channel == after.channel:
        await text_channel.send(f'Nie zapomnij o nagrywaniu, {member.mention}!')


async def remind_about_short_term_tasks(after, member):
    text_channel: TextChannel = bot.get_channel(text_channel_id)
    voice_channel: VoiceChannel = bot.get_channel(voice_channel_id)
    if voice_channel == after.channel:
        await text_channel.send(f"Nie zapomnij o celu krótkoterminowym, {member.mention}!")


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    mg = bot.get_user(gm_id)
    if mg == member:
        await remind_gm_about_recording(after, member)
    else:
        await remind_about_short_term_tasks(after, member)


bot.run(TOKEN)
