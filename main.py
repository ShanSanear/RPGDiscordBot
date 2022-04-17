from cogs.command_error_handler import CommandErrorHandler
from cogs.finder import Finder
from cogs.follower import Follower
from cogs.maintain import Maintain
from cogs.music import Music
from cogs.reminder import Reminder
from cogs.roller import Roller
from cogs.stream import Stream
from config.config import config
from loggers import create_loggers
from rpg_discord_bot import RPGDiscordBot


def main():
    create_loggers()
    bot = RPGDiscordBot(command_prefix="!")
    bot.add_cog(Music(bot))
    bot.add_cog(Maintain(bot))
    bot.add_cog(CommandErrorHandler(bot))
    bot.add_cog(Roller(bot))
    bot.add_cog(Stream(bot))
    bot.add_cog(Follower(bot))
    bot.add_cog(Reminder(bot))
    bot.add_cog(Finder(bot))
    bot.run(config.APP.TOKEN)


if __name__ == "__main__":
    main()
