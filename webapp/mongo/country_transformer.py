"""
todo
"""
class CountryTransformer:
    """
    todo
    """

    CONGO_ALIASES = [
        "congo (brazzaville)",
        "congo (kinshasa)",
        "republic of the congo"
    ]

    def __init__(self, country: str):
        self.country = country.lower()

    def transform(self):
        """
        todo
        :return:
        """
        if self.country == "mainland china":
            return "china"
        elif self.country == "uk":
            return "united kingdom"
        elif self.country == "us":
            return "united states"
        elif self.country in self.CONGO_ALIASES:
            return "congo"
        elif self.country == "viet nam":
            return "vietnam"
        else:
            return self.country
