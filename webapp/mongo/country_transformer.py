class CountryTransformer:

    CONGO_ALIASES = [
        "congo (brazzaville)",
        "congo (kinshasa)",
        "republic of the congo"
    ]

    def __init__(self, country: str):
        self.country = country.lower()

    def transform(self):
        if self.country == "mainland china":
            return "China"
        elif self.country == "uk":
            return "United Kingdom"
        elif self.country == "us":
            return "United States"
        elif self.country in self.CONGO_ALIASES:
            return "Congo"
        else:
            return self.country
