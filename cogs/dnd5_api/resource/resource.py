from urllib.parse import urljoin

import requests

from cogs.dnd5_api.resource.errors import ResourceNotFound
from loggers import general_logger


class Resource:
    """
    Class which represents possible resource at dnd5eapi endpoint
    """
    _base_api = "https://www.dnd5eapi.co/api/"

    def __init__(self, name: str, api_subpath: str):
        """
        Constructor
        :param name: name of the resource
        :param api_subpath: subpath for the api calls
        """
        self.name = name
        self._full_api_path = urljoin(self._base_api, api_subpath)
        self.response_data = {}

    def _get_by_index(self, index: str):
        """
        Get resource by provided index.
        :param index: Index of item that has been requested
        :return: Json response containing resource
        """
        url = urljoin(self._full_api_path, index)
        general_logger.debug("Url: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_by_name(self):
        """
        Fetches object, using provided name - saves this state in the class itself.
        """
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
        """
        Was this data already fetched
        :return: True if that data was already fetched, false otherwise
        """
        return True if self.response_data else False