import json
from typing import Union, Tuple, List

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from loggers import general_logger
from urllib.parse import urljoin

import requests


class SpellNotFound(Exception):
    pass


class Spell:
    _base_api = "https://www.dnd5eapi.co/api/"
    _spells_api = urljoin(_base_api, "spells/")

    @classmethod
    def get_spell_by_index(cls, index):
        url = urljoin(cls._spells_api, index)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_spell(cls, name):
        name_query = f"?name={name}"
        url = urljoin(cls._spells_api, name_query)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        returned = response.json()
        if returned['count'] == 1:
            return cls.get_spell_by_index(returned['results'][0]['index'])
        elif returned['count'] > 1:
            names = {result['name']: result['index'] for result in returned['results']}
            if name not in names:
                raise SpellNotFound
            return cls.get_spell_by_index(names[name])
        raise SpellNotFound


class DnD5Api(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def format_spell_message(data, required_fields: Union[None, Tuple, List] = None):
        fields = {'Name': data['name'],
                  'Description': '\n'.join(data['desc']),
                  "Components": ' '.join(data['components']),
                  "Range": data['range']}
        if "higher_level" in data:
            fields["Higher level"] = '\n'.join(data['higher_level'])
        message = "\n".join((f"**{key}** : {value}" for key, value in fields.items()
                             if required_fields is None or key in required_fields)
                            )

        return f"Found spell:\n{message}"

    @commands.command()
    async def search(self, ctx, what_for, name, *required_fields):
        if not required_fields:
            required_fields = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        async with ctx.typing():
            try:
                data = Spell.get_spell(name)
                await ctx.send(self.format_spell_message(data, required_fields=required_fields))
                # await ctx.send(json.dumps(data, indent=4))
            except SpellNotFound:
                await ctx.send(f"Spell not found: {name}")
