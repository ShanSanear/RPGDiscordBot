from pathlib import Path

import toml

from loggers import create_loggers
from rpg_discord_bot import RPGDiscordBot
from dnd5_api import DnD5Api
from music import Music
from maintain import Maintain


def main():
    create_loggers()
    config = toml.loads(Path("config.toml").read_text())
    bot = RPGDiscordBot('!', config_data=config)
    bot.add_cog(Music(bot))
    bot.add_cog(DnD5Api(bot))
    bot.add_cog(Maintain(bot))
    bot.run(config['APP']['TOKEN'])


if __name__ == '__main__':
    main()
