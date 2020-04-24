from .country_map import country_map


class CountryTransformer:

    @staticmethod
    def transform(country: str):
        return country_map.get(country.lower(), country.title())
