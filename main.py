from pathlib import Path

import toml
from discord import TextChannel, VoiceState, VoiceChannel, Member
from discord.ext import commands


class MyBot(commands.Bot):

    def __init__(self, command_prefix, config):
        super(MyBot, self).__init__(command_prefix)
        self.config = config

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def remind_gm_about_recording(self, after, member):
        text_channel: TextChannel = self.get_channel(self.config['REMINDER']['TEXT_CHANNEL_ID'])
        voice_channel: VoiceChannel = self.get_channel(self.config['REMINDER']['VOICE_CHANNEL_ID'])
        if voice_channel == after.channel:
            await text_channel.send(f'Nie zapomnij o nagrywaniu, {member.mention}!')

    async def remind_about_short_term_tasks(self, after, member):
        text_channel: TextChannel = self.get_channel(self.config['REMINDER']['TEXT_CHANNEL_ID'])
        voice_channel: VoiceChannel = self.get_channel(self.config['REMINDER']['VOICE_CHANNEL_ID'])
        if voice_channel == after.channel:
            await text_channel.send(f"Nie zapomnij o celu krótkoterminowym, {member.mention}!")

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        mg = self.get_user(self.config['REMINDER']['GM_ID'])
        if mg == member:
            await self.remind_gm_about_recording(after, member)
        else:
            await self.remind_about_short_term_tasks(after, member)

    async def send_message_to_text_channel(self, message):
        text_channel: TextChannel = self.get_channel(self.config['REMINDER']['TEXT_CHANNEL_ID'])
        await text_channel.send(message)


config = toml.loads(Path("config.toml").read_text())
bot = MyBot('!', config=config)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.send_message_to_text_channel("Turning off")
    await ctx.bot.logout()
    await ctx.bot.close()


bot.run(config['APP']['TOKEN'])
