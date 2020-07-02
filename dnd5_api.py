import json
from typing import Union, Tuple, List

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from loggers import general_logger
from urllib.parse import urljoin

import requests


class ResourceNotFound(Exception):
    pass


class SpellNotFound(ResourceNotFound):
    pass


class Resource:
    _base_api = "https://www.dnd5eapi.co/api/"

    def __init__(self, name, api_subpath):
        self.name = name
        self._full_api_path = urljoin(self._base_api, api_subpath)

    def _get_by_index(self, index):
        url = urljoin(self._full_api_path, index)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_by_name(self):
        name_query = f"?name={self.name}"
        url = urljoin(self._full_api_path, name_query)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        returned = response.json()
        if returned['count'] == 1:
            return self._get_by_index(returned['results'][0]['index'])
        elif returned['count'] > 1:
            names = {result['name']: result['index'] for result in returned['results']}
            if self.name not in names:
                raise ResourceNotFound
            return self._get_by_index(names[self.name])
        raise ResourceNotFound


class Spell(Resource):

    def __init__(self, name):
        super().__init__(name, api_subpath="spells/")


class DnD5Api(commands.Cog):
    _classes = {
        "spell": Spell
    }
    _message = {
        "spell": "Found spell:"
    }

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def format_message(start_of_the_message, data, fields_to_show: Union[None, Tuple, List] = None):
        fields = {'Name': data['name'],
                  'Description': '\n'.join(data['desc']),
                  "Components": ' '.join(data['components']),
                  "Range": data['range']}
        if "higher_level" in data:
            fields["Higher_level"] = '\n'.join(data['higher_level'])
        message = "\n".join((f"**{key}** : {value}" for key, value in fields.items()
                             if fields_to_show is None or key in fields_to_show)
                            )

        return f"{start_of_the_message}\n{message}"

    @commands.command()
    async def search(self, ctx, what_for, name, *fields_to_show):
        """Searches for spell (for now) using it's name.
        :param what_for - what are you searching for (for now - only spell)
        :param name - name of the spell
        :param fields_to_show - space separated fields to show: Name, Description, Components, Range, Higher_level"""
        if what_for not in self._classes or what_for not in self._message:
            raise NotImplementedError
        if not fields_to_show:
            fields_to_show = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        async with ctx.typing():
            cls = self._classes[what_for]
            msg = self._message[what_for]
            try:
                data = cls(name).get_by_name()
                await ctx.send(self.format_message(msg, data, fields_to_show=fields_to_show))
                # await ctx.send(json.dumps(data, indent=4))
            except ResourceNotFound:
                await ctx.send(f"Spell not found: {name}")
