from pathlib import Path

import toml
from discord import TextChannel, VoiceState, VoiceChannel, Member
from discord.ext import commands

from dnd5_api import DnD5Api
from loggers import create_loggers, general_logger
from music import Music


class MyBot(commands.Bot):

    def __init__(self, command_prefix, config_data):
        super(MyBot, self).__init__(command_prefix)
        self._config = config_data

    async def on_ready(self):
        general_logger.info("Logged in as: %s [ID: %d]", self.user.name, self.user.id)

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.id in self._config['REMINDER']['BLACKLISTED_IDS']:
            general_logger.debug("User %s is in black list for reminder", member)
            return
        voice_channel: VoiceChannel = self.get_channel(self._config['REMINDER']['VOICE_CHANNEL_ID'])
        if voice_channel != after.channel:
            return
        if before.channel == after.channel:
            general_logger.debug("User %s is in the same channel still, skipping", member)
            return
        mg = self.get_user(self._config['REMINDER']['GM_ID'])
        text_channel: TextChannel = self.get_channel(self._config['REMINDER']['TEXT_CHANNEL_ID'])
        if mg == member:
            await text_channel.send(f'Nie zapomnij o nagrywaniu, {member.mention}!')
        else:
            await text_channel.send(f"Nie zapomnij o celu krótkoterminowym, {member.mention}!")

    async def send_message_to_text_channel(self, message):
        text_channel: TextChannel = self.get_channel(self._config['REMINDER']['TEXT_CHANNEL_ID'])
        await text_channel.send(message)


config = toml.loads(Path("config.toml").read_text())
bot = MyBot('!', config_data=config)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.send_message_to_text_channel("Turning off")
    await ctx.bot.logout()
    await ctx.bot.close()


def main():
    create_loggers()
    bot.add_cog(Music(bot))
    bot.add_cog(DnD5Api(bot))
    bot.run(config['APP']['TOKEN'])


if __name__ == '__main__':
    main()
