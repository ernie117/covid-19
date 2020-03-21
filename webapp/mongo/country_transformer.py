"""
todo
"""
from .country_mapper import country_map


class CountryTransformer:
    """
    todo
    """
    country_map = country_map

    def __init__(self, country: str):
        self.country = country.lower()

    def transform(self):
        """
        todo
        :return:
        """
        return self.country_map.get(self.country, self.country)
