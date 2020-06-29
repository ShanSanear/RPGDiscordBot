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

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        voice_channel: VoiceChannel = self.get_channel(self.config['REMINDER']['VOICE_CHANNEL_ID'])
        if voice_channel != after.channel:
            return
        mg = self.get_user(self.config['REMINDER']['GM_ID'])
        text_channel: TextChannel = self.get_channel(self.config['REMINDER']['TEXT_CHANNEL_ID'])
        if mg == member:
            await text_channel.send(f'Nie zapomnij o nagrywaniu, {member.mention}!')
        else:
            await text_channel.send(f"Nie zapomnij o celu krótkoterminowym, {member.mention}!")

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
