from pathlib import Path

import toml

from loggers import create_loggers
from cogs.roller import Roller
from rpg_discord_bot import RPGDiscordBot
from cogs.dnd5_api import DnD5Api
from cogs.music import Music
from cogs.maintain import Maintain, CommandErrorHandler


def main():
    create_loggers()
    config = toml.loads(Path("config.toml").read_text(encoding="utf-8"))
    bot = RPGDiscordBot("!", config_data=config)
    bot.add_cog(Music(bot))
    bot.add_cog(DnD5Api(bot))
    bot.add_cog(Maintain(bot))
    bot.add_cog(CommandErrorHandler(bot))
    bot.add_cog(Roller(bot))
    bot.run(config["APP"]["TOKEN"])


if __name__ == "__main__":
    main()
