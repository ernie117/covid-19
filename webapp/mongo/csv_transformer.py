from csv import DictReader

from webapp.mongo.CountryTransformer import CountryTransformer


class CSVTransformer:
    COUNTRY_REGION: str = "Country/Region"
    COUNTRY_REGION_LC: str = "country/region"
    list_of_custom_dicts = []

    def __init__(self, dict_reader: DictReader, date: str):
        self.dict_reader = dict_reader
        self.date = date.split(".")[0]

    def transform_csv_data(self):
        pass

    def create_custom_dicts(self):
        """
        Alter the structure of dictionaries slightly by adding the date
        to each one. Also transforms some country names as they are
        inconsistently-named in the source data.
        """
        new_dicts = []
        for dictionary in self.dict_reader:
            dictionary["date"] = self.date

            country = dictionary[self.COUNTRY_REGION]
            country_transformer = CountryTransformer(country)
            dictionary[self.COUNTRY_REGION] = country_transformer.transform()

            new_dicts.append({
                "date": dictionary["date"],
                self.COUNTRY_REGION.lower(): dictionary[self.COUNTRY_REGION],
                "province/state": dictionary["Province/State"],
                "confirmed": dictionary["Confirmed"],
                "recovered": dictionary["Recovered"],
                "deaths": dictionary["Deaths"]
            })

        self.list_of_custom_dicts = new_dicts

    def reduce_dicts(self):
        """
        Create a dict for each date with summed values for each country on
        that date.
        """
        confirmed = 0
        recovered = 0
        deaths = 0

        countries = {d[self.COUNTRY_REGION_LC]
                     for d in self.list_of_custom_dicts}

        # Sum the confirmed, recovered and deaths for each region of a country
        # to have a total confirmed, recovered and deaths for each country
        building_dictionary = {
            "date": self.date,
            "countries": []
        }
        for country in countries:
            for dictionary in self.list_of_custom_dicts:
                if dictionary[self.COUNTRY_REGION_LC].lower() == country.lower():
                    dictionary = self.replace_empty_values(dictionary)
                    confirmed += int(dictionary["confirmed"])
                    recovered += int(dictionary["recovered"])
                    deaths += int(dictionary["deaths"])
                else:
                    continue

            building_dictionary["countries"].append({
                "country/region": country,
                "confirmed": confirmed,
                "recovered": recovered,
                "deaths": deaths
            })

            confirmed = 0
            recovered = 0
            deaths = 0

        return building_dictionary

    @staticmethod
    def replace_empty_values(dictionary):
        """
        Some values in the raw csv are blank, this replaces them with zeroes.

        :param dictionary:
        :return:
        """
        for case in ("confirmed", "recovered", "deaths"):
            if not dictionary[case]:
                dictionary[case] = 0

        return dictionary
