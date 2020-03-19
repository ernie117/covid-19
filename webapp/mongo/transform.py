"""
Here we'll transform the data retrieved by the request module.
"""
import json
from csv import DictReader

from webapp.mongo import request_csv

COUNTRY_REGION = "Country/Region"
COUNTRY_REGION_LC = "country/region"


def create_custom_dicts(dictreader: DictReader, date: str):
    """
    Alter the structure of dictionaries slightly by adding the date
    to each one. Also transform some country names as they are
    inconsistently-named in the source data.

    :param dictreader: DictReader holding our source csv data
    :param date: string representing date of case data
    :return:
    """
    new_dicts = []
    for dictionary in dictreader:
        dictionary["date"] = date.split(".")[0]

        # There are more of these that need to be checked and changed.
        country = dictionary[COUNTRY_REGION]
        dictionary[COUNTRY_REGION] = transform_country(country)

        new_dicts.append({
            "date": dictionary["date"],
            COUNTRY_REGION_LC: dictionary[COUNTRY_REGION],
            "province/state": dictionary["Province/State"],
            "confirmed": dictionary["Confirmed"],
            "recovered": dictionary["Recovered"],
            "deaths": dictionary["Deaths"]
        })

    return new_dicts


def reduce_dicts(list_of_custom_dicts, date):
    """
    Create a dict for each date with summed values for each country on
    that date.

    :param date: String representing date
    :param list_of_custom_dicts: Custom dicts created previously
    :return: list of dicts with case totals for country by date
    """
    confirmed = 0
    recovered = 0
    deaths = 0

    countries = {d[COUNTRY_REGION_LC] for d in list_of_custom_dicts}

    # Sum the confirmed, recovered and deaths for each region of a country
    # to have a total confirmed, recovered and deaths for each country
    building_dictionary = {
        "date": date,
        "countries": []
    }
    for country in countries:
        for dictionary in list_of_custom_dicts:
            if dictionary[COUNTRY_REGION_LC].lower() == country.lower():
                dictionary = replace_empty_values(dictionary)
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


def transform_country(country: str):
    if country.lower() == "mainland china":
        return "China"
    elif country.lower() == "uk":
        return "United Kingdom"
    elif country.lower() == "us":
        return "United States"


def main():
    csv_list, dates = request_csv.main()
    reduced_dicts = []
    for csv, date in zip(csv_list, dates):
        dicts = create_custom_dicts(csv, date)
        reduced_dicts.append(reduce_dicts(dicts, date))

    with open("dates.json", "w") as f:
        f.write(json.dumps(reduced_dicts, indent=2))


if __name__ == "__main__":
    main()
