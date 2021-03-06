from urllib.parse import urljoin

import requests
from discord.ext import commands
from discord.ext.commands import Bot

from loggers import general_logger
from utils import flyweight, ResourceNotFound


class Resource:
    _base_api = "https://www.dnd5eapi.co/api/"

    def __init__(self, name: str, api_subpath: str):
        self.name = name
        self._full_api_path = urljoin(self._base_api, api_subpath)
        self.response_data = {}

    def _get_by_index(self, index):
        url = urljoin(self._full_api_path, index)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_by_name(self):
        if self.already_fetched:
            general_logger.debug("Using cached data for: %r", self)
            return
        name_query = f"?name={self.name}"
        url = urljoin(self._full_api_path, name_query)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        returned = response.json()
        if returned["count"] == 1:
            self.response_data = self._get_by_index(returned["results"][0]["index"])
        elif returned["count"] > 1:
            names = {result["name"]: result["index"] for result in returned["results"]}
            if self.name not in names:
                raise ResourceNotFound
            self.response_data = self._get_by_index(names[self.name])
        else:
            raise ResourceNotFound
        general_logger.debug("Response data: %s", self.response_data)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    @property
    def already_fetched(self):
        return True if self.response_data else False


@flyweight
class Spell(Resource):
    def __init__(self, name: str):
        super().__init__(name, api_subpath="spells/")
        self.start_of_the_message = "Found spell:"

    def get_formatted_message(self, fields_to_show):
        fields = {
            "Name": self.response_data["name"],
            "Description": "\n".join(self.response_data["desc"]),
            "Level": self.response_data["level"],
            "Components": " ".join(self.response_data["components"]),
            "Range": self.response_data["range"],
            "Ritual": self.response_data["ritual"],
            "Duration": self.response_data["duration"],
            "Casting time": self.response_data["casting_time"],
            "School": self.response_data["school"]["name"],
            "Classes": ",".join((cls["name"] for cls in self.response_data["classes"])),
        }
        if "higher_level" in self.response_data:
            fields["Higher_level"] = "\n".join(self.response_data["higher_level"])
        message = "\n".join(
            (
                f"**{key}** : {value}"
                for key, value in fields.items()
                if fields_to_show is None or key in fields_to_show
            )
        )

        return f"{self.start_of_the_message}\n{message}"


class DnD5Api(commands.Cog):
    _classes = {"spell": Spell}

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, what_for, name, *fields_to_show):
        """Searches for spell (for now) using it's name.
        :param what_for - what are you searching for (for now - only spell)
        :param name - name of the spell
        :param fields_to_show - space separated fields to show; Name, Description, Components, Range, Higher_level"""
        if what_for not in self._classes:
            raise NotImplementedError
        if not fields_to_show:
            fields_to_show = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        async with ctx.typing():
            cls = self._classes[what_for]
            try:
                search_instance = cls(name)
                search_instance.fetch_by_name()
                message = search_instance.get_formatted_message(fields_to_show)
                await ctx.send(message)
            except ResourceNotFound:
                await ctx.send(f"Spell not found: {name}")
