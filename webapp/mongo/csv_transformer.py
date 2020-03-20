"""
todo
"""
from csv import DictReader

from webapp.mongo.country_transformer import CountryTransformer


class CSVTransformer:
    """
    todo
    """
    COUNTRY_REGION: str = "Country/Region"
    COUNTRY_REGION_LC: str = "country/region"

    def __init__(self, date: str, dict_reader: DictReader):
        self.date = date
        self.dict_reader = dict_reader

    def transform_csv_data(self):
        """
        todo
        :return:
        """
        return self._reduce_dicts(self._create_custom_dicts())

    def _create_custom_dicts(self):
        """
        Alter the structure of dictionaries slightly by adding the date
        to each one, transforms some country names as they are
        inconsistently-named in the source data, and returns them sorted
        alphabetically by country.
        """
        new_dicts = []
        for dictionary in self.dict_reader:
            country = dictionary[self.COUNTRY_REGION]
            country_transformer = CountryTransformer(country)
            dictionary[self.COUNTRY_REGION] = country_transformer.transform()

            new_dicts.append({
                "date": self.date,
                self.COUNTRY_REGION_LC: dictionary[self.COUNTRY_REGION],
                "province/state": dictionary["Province/State"],
                "confirmed": dictionary["Confirmed"],
                "recovered": dictionary["Recovered"],
                "deaths": dictionary["Deaths"]
            })

        return sorted(new_dicts, key=lambda d: d[self.COUNTRY_REGION_LC])

    def _reduce_dicts(self, list_of_custom_dicts):
        """
        Create a dict for each date with summed values for each country on
        that date.
        """
        confirmed = 0
        recovered = 0
        deaths = 0

        countries = sorted({d[self.COUNTRY_REGION_LC]
                            for d in list_of_custom_dicts})

        # Sum the confirmed, recovered and deaths for each region of a country
        # to have a total confirmed, recovered and deaths for each country
        building_dictionary = {
            "date": self.date,
            "countries": []
        }
        for country in countries:
            for dictionary in list_of_custom_dicts:
                if dictionary[self.COUNTRY_REGION_LC] == country.lower():
                    dictionary = self._replace_empty_values(dictionary)
                    confirmed += int(dictionary["confirmed"])
                    recovered += int(dictionary["recovered"])
                    deaths += int(dictionary["deaths"])
                else:
                    continue

            building_dictionary["countries"].append({
                self.COUNTRY_REGION_LC: country,
                "confirmed": confirmed,
                "recovered": recovered,
                "deaths": deaths
            })

            confirmed = 0
            recovered = 0
            deaths = 0

        return building_dictionary

    @staticmethod
    def _replace_empty_values(dictionary):
        """
        Some values in the raw csv are blank, this replaces them with zeroes.

        :param dictionary:
        :return:
        """
        for case in ("confirmed", "recovered", "deaths"):
            if not dictionary[case]:
                dictionary[case] = 0

        return dictionary
