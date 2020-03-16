import csv
import itertools
import os
from typing import Dict, List

import numpy
import pandas
from pandas import DataFrame

from webapp.functions.plotting import build_line_plot, set_seaborn_features


def get_dates(dataframe: DataFrame) -> list:
    return dataframe.dates.dt.strftime('%Y-%m-%d')


def read_csv_files_to_dict(data_dir: str, country: str):
    """
    Creates a dictionary wherein keys are dates corresponding
    to CSV file names, and values are the data in those CSVs.

    :return: Dictionary of dates and raw csv data
    """
    cases_dict = {
        "dates": [],
        "confirmed": [],
        "recovered": [],
        "deaths": [],
    }
    filenames = sorted(os.scandir(data_dir), key=lambda x: x.name)
    for filename in filenames:
        if filename.name.endswith("csv"):
            with open(filename, "r", encoding="utf-8") as f_obj:
                reader = csv.DictReader(f_obj)
                date = filename.name.split(".")[0]
                cases_dict = extract_confirmed_deaths_recovered(reader,
                                                                country,
                                                                date,
                                                                cases_dict)

    return cases_dict


def extract_confirmed_deaths_recovered(reader: csv.DictReader, country: str,
                                       date: str, cases_dict: Dict):
    """
    Creates a new dict wherein keys are sorted (ascending) dates
    and values are the confirmed, recovered and death cases for
    the country supplied.

    :param reader:
    :param country:
    :param date:
    :return:
    """
    list_of_country_dicts = [d for d in list(reader)
                             if country in d["Country/Region"].lower()]

    confirmed = 0
    recovered = 0
    deaths = 0
    # Sum values for multiple states/provinces within the same country
    for d in list_of_country_dicts:
        confirmed_str = d["Confirmed"]
        recovered_str = d["Recovered"]
        deaths_str = d["Deaths"]
        if confirmed_str:
            confirmed += int(confirmed_str)
        if recovered_str:
            recovered += int(recovered_str)
        if deaths_str:
            deaths += int(deaths_str)

    cases_dict["confirmed"].append(confirmed)
    cases_dict["recovered"].append(recovered)
    cases_dict["deaths"].append(deaths)

    cases_dict["dates"].append(date)
    return cases_dict


def data_to_dataframe(cases):
    """
    Takes dict of dates and confirmed covid-19 cases and
    re-organises it into a dictionary of lists suitable for
    converting into a pandas DataFrame.

    :param cases: Dict of dates and cases
    :return: a list of dates and a pandas DataFrame
    """
    print(len(cases["dates"]))
    print(len(cases["confirmed"]))
    print(len(cases["recovered"]))
    print(len(cases["deaths"]))
    dataframe = DataFrame(data=cases)
    dataframe.replace("", 0)
    dataframe["dates"] = pandas.to_datetime(dataframe["dates"])
    dataframe["confirmed"] = pandas.to_numeric(dataframe["confirmed"])
    dataframe["recovered"] = pandas.to_numeric(dataframe["recovered"])
    dataframe["deaths"] = pandas.to_numeric(dataframe["deaths"])
    dataframe.fillna(0, inplace=True)
    dataframe["confirmed"] = dataframe["confirmed"].astype(int)
    dataframe["recovered"] = dataframe["recovered"].astype(int)
    dataframe["deaths"] = dataframe["deaths"].astype(int)
    print(dataframe)

    return dataframe


def main(country: str, data_dir: str, img_dir: str):
    data = read_csv_files_to_dict(data_dir, country)
    dataframe = data_to_dataframe(data)
    dates = get_dates(dataframe)
    set_seaborn_features()
    build_line_plot(dataframe, country.title(), dates, img_dir)
