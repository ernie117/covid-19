import csv
import os
from pathlib import Path
from typing import Dict

import pandas
from pandas import DataFrame

from webapp.etl.country_transformer import CountryTransformer
from webapp.services.plotting import SeabornPlotter


def get_dates(dataframe: DataFrame) -> list:
    return dataframe.dates.dt.strftime('%m-%d')


def read_csv_files_to_dict(country: str):
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
    data_path = Path("webapp/COVID-19-data")
    filenames = sorted(os.scandir(data_path), key=lambda x: x.name)
    for filename in filenames:
        if filename.name.endswith("csv"):
            with open(filename, "r", encoding="utf-8") as f_obj:
                reader = list(csv.DictReader(f_obj))
                date = filename.name.split(".")[0]
                cases_dict = extract_confirmed_deaths_recovered(reader,
                                                                country,
                                                                date,
                                                                cases_dict)

    return cases_dict


def extract_confirmed_deaths_recovered(reader: list, country: str,
                                       date: str, cases_dict: Dict):
    """
    Creates a new dict wherein keys are sorted (ascending) dates
    and values are the confirmed, recovered and death cases for
    the country supplied.

    :param cases_dict:
    :param reader:
    :param country:
    :param date:
    :return:
    """
    country = CountryTransformer(country).transform()
    list_of_country_dicts = [d for d in reader
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

    # Don't want rows with no values
    if confirmed == 0 and recovered == 0 and deaths == 0:
        return cases_dict

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
    dataframe = DataFrame(data=cases)
    dataframe.replace("", 0)
    dataframe["dates"] = pandas.to_datetime(dataframe["dates"])

    return dataframe


def main(country: str):
    data = read_csv_files_to_dict(country)
    dataframe = data_to_dataframe(data)
    dates = get_dates(dataframe)
    plotter = SeabornPlotter(dataframe)
    plotter.set_seaborn_features()
    plotter.build_line_plot(country, dates)
