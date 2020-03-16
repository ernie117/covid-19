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

    :param dictreader: DictReader holding our source data
    :param date: string representing date of case data
    :return:
    """
    new_dicts = []
    for dictionary in dictreader:
        dictionary["date"] = date.split(".")[0]

        country = dictionary[COUNTRY_REGION]
        # There are more of these that need to be checked and changed.
        # TODO move to own function
        if country.lower() == "mainland china":
            dictionary[COUNTRY_REGION] = "China"
        elif country.lower() == "uk":
            dictionary[COUNTRY_REGION] = "United Kingdom"

        new_dicts.append({
            "date": dictionary["date"],
            COUNTRY_REGION_LC: dictionary[COUNTRY_REGION],
            "province/state": dictionary["Province/State"],
            "confirmed": dictionary["Confirmed"],
            "recovered": dictionary["Recovered"],
            "deaths": dictionary["Deaths"]
        })

    return new_dicts


def reduce_dicts(list_of_custom_dicts):
    """
    Sum all cases for each occurrence of a country by date, build new
    dict of results.
    
    :param list_of_custom_dicts: Custom dicts created previously
    :return: list of dicts with case totals for country by date
    """
    confirmed = 0
    recovered = 0
    deaths = 0

    countries = {d[COUNTRY_REGION_LC] for d in list_of_custom_dicts}

    # Sum the confirmed, recovered and deaths for each region of a country
    # to have a total for each case for each country
    country_dicts = []
    for country in countries:
        for dictionary in list_of_custom_dicts:
            if dictionary[COUNTRY_REGION_LC].lower() == country.lower():
                dictionary = replace_empty_values(dictionary)
                confirmed += int(dictionary["confirmed"])
                recovered += int(dictionary["recovered"])
                deaths += int(dictionary["deaths"])
            else:
                continue

        country_dicts.append({
            "date": list_of_custom_dicts[0]["date"],
            COUNTRY_REGION_LC: country,
            "confirmed": confirmed,
            "recovered": recovered,
            "deaths": deaths
        })
        confirmed = 0
        recovered = 0
        deaths = 0

    return country_dicts


def replace_empty_values(dictionary):
    for case in ("confirmed", "recovered", "deaths"):
        if not dictionary[case]:
            dictionary[case] = 0

    return dictionary


def main():
    data_list, dates = request_csv.main()
    objects_to_save = []
    for datum, date in zip(data_list, dates):
        dicts = create_custom_dicts(datum, date)
        reduced_dicts = reduce_dicts(dicts)
        # Pass to service layer here
        for thingy in reduced_dicts:
            objects_to_save.append(thingy)

    for date in objects_to_save:
        print(date)


main()
