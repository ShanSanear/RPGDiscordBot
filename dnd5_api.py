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

    def __init__(self, name: str, api_subpath: str, fields_to_show: Tuple):
        self.name = name
        self._full_api_path = urljoin(self._base_api, api_subpath)
        self.data = {}
        self.fields_to_show = fields_to_show

    def _get_by_index(self, index):
        url = urljoin(self._full_api_path, index)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_by_name(self):
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

    def __init__(self, name: str, fields_to_show: Tuple):
        super().__init__(name, api_subpath="spells/", fields_to_show=fields_to_show)
        self.start_of_the_message = "Found spell:"

    def get_formatted_message(self):
        fields = {'Name': self.data['name'],
                  'Description': '\n'.join(self.data['desc']),
                  "Components": ' '.join(self.data['components']),
                  "Range": data['range']}
        if "higher_level" in self.data:
            fields["Higher_level"] = '\n'.join(self.data['higher_level'])
        message = "\n".join((f"**{key}** : {value}" for key, value in fields.items()
                             if self.fields_to_show is None or key in self.fields_to_show)
                            )

        return f"{self.start_of_the_message}\n{message}"


class DnD5Api(commands.Cog):
    _classes = {
        "spell": Spell
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
        if what_for not in self._classes:
            raise NotImplementedError
        if not fields_to_show:
            fields_to_show = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        async with ctx.typing():
            cls = self._classes[what_for]
            try:
                search_instance = cls(name, fields_to_show)
                await search_instance.fetch_by_name()
                message = search_instance.get_formatted_message()
                await ctx.send(message)
            except ResourceNotFound:
                await ctx.send(f"Spell not found: {name}")
