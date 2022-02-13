from typing import Optional, Iterator

from cogs.dnd5_api.resource.resource import Resource
from utils import flyweight


@flyweight
class Spell(Resource):
    """
    Spell resource from api
    """

    def __init__(self, name: str):
        """
        Constructor.
        :param name: Name of the spell to check
        """
        super().__init__(name, api_subpath="spells/")
        self.start_of_the_message = "Found spell:"

    def get_formatted_message(self, fields_to_show: Optional[Iterator[str]]):
        """
        Creates already formatted message based on the fields to be shown requested by the user
        :param fields_to_show: Fields to be shown
        :return: Formatted text, ready to be placed as message in Discord
        """
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