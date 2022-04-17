from typing import Iterator

from cogs.dnd5_api.resource.errors import ResourceNotFound
from cogs.dnd5_api.resource.spell import Spell
from loggers import general_logger


class DnD5Api:
    """
    Cog representing access to the DND5E API
    """
    _classes = {"spell": Spell}

    @classmethod
    async def dnd_search(cls, what_for: str, name: str, *fields_to_show: Iterator[str]):
        """Searches for spell (for now) using its name.
        :param what_for - what are you searching for (for now - only spell)
        :param name - name of the spell
        :param fields_to_show - space separated fields to show; Name, Description, Components, Range, Higher_level"""
        if what_for not in cls._classes:
            raise NotImplementedError
        if not fields_to_show:
            fields_to_show = None
        general_logger.debug("Searching for: %s using name: %s", what_for, name)
        try:
            search_instance = cls._classes[what_for](name)
            search_instance.fetch_by_name()
            return search_instance.get_formatted_message(fields_to_show)
        except ResourceNotFound:
            return f"Spell not found: {name}"
