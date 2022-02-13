from cogs.stream import Stream
from config.config import config
from loggers import create_loggers
from cogs.roller import Roller
from rpg_discord_bot import RPGDiscordBot
from cogs.dnd5_api import DnD5Api
from cogs.music import Music
from cogs.maintain import Maintain
from cogs.command_error_handler import CommandErrorHandler


def main():
    create_loggers()
    bot = RPGDiscordBot(command_prefix="!")
    bot.add_cog(Music(bot))
    bot.add_cog(DnD5Api(bot))
    bot.add_cog(Maintain(bot))
    bot.add_cog(CommandErrorHandler(bot))
    bot.add_cog(Roller(bot))
    bot.add_cog(Stream(bot))
    bot.run(config.APP.TOKEN)


if __name__ == "__main__":
    main()
