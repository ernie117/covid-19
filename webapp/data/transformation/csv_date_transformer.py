"""
Contains the class for transforming covid-19 CSV data from github into a
document structure suitable for MongoDB.
"""
import datetime
from typing import List, Dict

from webapp.data.transformation.country_transformer import CountryTransformer
from webapp.utils.loggers import build_logger


class CSVDateTransformer:
    """
    Class containing all logic required to transform CSV data from GitHub into
    custom dictionary objects representing documents to be persisted in Mongo.
    """

    COUNTRY_REGION: str = "Country_Region"
    COUNTRY_REGION_OLD: str = "Country/Region"
    PROVINCE_STATE: str = "Province_State"
    PROVINCE_STATE_OLD: str = "Province/State"
    CONFIRMED: str = "Confirmed"
    RECOVERED: str = "Recovered"
    DEATHS: str = "Deaths"
    COUNTRY_REGION_LC: str = "country/region"

    def __init__(self):
        self.logger = build_logger("CSVDateTransformer")

    def transform_csv_data(self, data) -> List[Dict]:
        """
        Entry point for transforming CSV data requested from the Johns Hopkins
        GitHub repo.

        :return: list of transformed dictionaries
        """
        transformed_data = []
        for date, dictreader in data.items():
            custom_dicts = self._create_custom_dicts(dictreader)
            transformed_data.append(self._create_documents(date, custom_dicts))

        return transformed_data

    def _create_custom_dicts(self, dictreader) -> List[Dict]:
        """
        Create an intermediate structure for transformation. The structure of
        dicts in the DictReader is altered to dicts with custom keys, removing
        latitude, longitude, last-updated and others. Also transforms country
        names to preferred/consistent names. Dicts are returned in a list sorted
        alphabetically by country.

        Example resulting dict:
        {
            "country/region": italy,
            "province/state": "",
            "confirmed": "10",
            "recovered": "",
            "deaths": ""
        }

        :param dictreader: DictReader object of data retrieved from GitHub
        :return: list of custom dicts sorted alphabetically by country
        """
        new_dicts = []
        for row in dictreader:
            try:
                country = row[self.COUNTRY_REGION]
                province = row[self.PROVINCE_STATE]
            except KeyError:
                # Older documents have different keys
                country = row[self.COUNTRY_REGION_OLD]
                province = row[self.PROVINCE_STATE_OLD]

            country_transformer = CountryTransformer(country)
            custom_country = country_transformer.transform()

            new_dicts.append(
                {
                    self.COUNTRY_REGION_LC: custom_country,
                    "province/state": province,
                    "confirmed": row["Confirmed"],
                    "recovered": row["Recovered"],
                    "deaths": row["Deaths"],
                }
            )

        return sorted(new_dicts, key=lambda d: d[self.COUNTRY_REGION_LC])

    def _create_documents(
        self, date: str, list_of_custom_dicts: List[Dict]
    ) -> Dict[str, any]:
        """
        Given a list of custom dicts provided by _create_custom_dicts, cases of
        each country's provinces/states are summed to provide totals for
        confirmed, recovered and deaths for each country. Dicts are built
        representing Mongo documents that will be persisted containing a date
        key and an array of objects for each country with data for that date.

        Example resulting dict:
        {
        "date": 01-22-2020 00:00:00",
        "countries": [
                {
                    "country/region": "italy",
                    "confirmed": 10,
                    "recovered": 0,
                    "deaths": 0
                },
                ...
            ]
        }

        :param date: String of date for requested data.
        :param list_of_custom_dicts: Dicts produced by _create_custom_dicts
        :return: Final transformed Dict representing a Document to be persisted
        """
        countries = sorted({d[self.COUNTRY_REGION_LC] for d in list_of_custom_dicts})

        # Sum the confirmed, recovered and deaths for each region of a country
        # to have a total confirmed, recovered and deaths for each country
        building_dictionary = {
            "date": datetime.datetime.strptime(date, "%m-%d-%Y"),
            "countries": [],
        }

        confirmed = 0
        recovered = 0
        deaths = 0

        self.logger.info("Building new document for date '%s'", date)
        for country in countries:
            for dictionary in list_of_custom_dicts:
                if dictionary[self.COUNTRY_REGION_LC] == country.lower():
                    dictionary = self._replace_empty_values(dictionary)
                    confirmed += int(dictionary["confirmed"])
                    recovered += int(dictionary["recovered"])
                    deaths += int(dictionary["deaths"])
                else:
                    continue

            building_dictionary["countries"].append(
                {
                    self.COUNTRY_REGION_LC: country,
                    "confirmed": confirmed,
                    "recovered": recovered,
                    "deaths": deaths,
                }
            )

            confirmed = 0
            recovered = 0
            deaths = 0

        return building_dictionary

    @staticmethod
    def _replace_empty_values(dictionary: Dict) -> Dict:
        """
        Some values in the raw csv are blank, this replaces them with zeroes.

        :param dictionary: Custom dict produced by _create_custom_dicts
        :return: Input dictionary with blank values converted to int 0
        """
        for case in ("confirmed", "recovered", "deaths"):
            if not dictionary[case]:
                dictionary[case] = 0

        return dictionary
