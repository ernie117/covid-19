import csv
import os
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from pandas import DataFrame


def get_dates() -> list:
    return sorted([f.name.split(".")[0] for f in os.scandir("COVID-19-data")
                   if f.name.endswith("csv")])


def read_csv_files_to_dict() -> Dict[str, List[str]]:
    """
    Creates a dictionary wherein keys are dates corresponding
    to CSV file names, and values are the data in those CSVs.

    :return: Dictionary of dates and raw csv data
    """
    with os.scandir("COVID-19-data") as iterator:
        csv_dicts_list: Dict[str, List[str]] = {}
        filename: os.DirEntry
        for filename in iterator:
            if filename.name.endswith("csv"):
                with open(filename, "r", encoding="utf-8") as f_obj:
                    reader = csv.DictReader(f_obj)
                    csv_dicts_list[filename.name.split(".")[0]] = list(reader)

    return csv_dicts_list


def extract_confirmed_cases_deaths_recovered(data: Dict[any, List[str]],
                                             country: str) -> Dict[str, list]:
    """
    Creates a new dict wherein keys are sorted (ascending) dates
    and values are the confirmed, recovered and death cases for
    the country supplied.

    :param data: Dict of dates and raw csv data
    :param country: String of country to search for cases
    :return: Dict of dates and reduced csv data
    """
    sorted_data = dict(sorted(data.items()))
    new_data = dict.fromkeys(sorted_data.keys())

    country = country.lower()
    confirmed_cases = 0
    recovered = 0
    deaths = 0
    for key, value in sorted_data.items():
        for element in value:
            # Due to inconsistencies in the CSV data UK is sometimes 'UK'
            # and sometimes 'United Kingdom' :/
            try:
                if ((country == "uk" or country == "united kingdom")
                        and (element["Country/Region"] == "United Kingdom"
                             or
                             element["Country/Region"] == "UK")):
                    confirmed_cases += int(element["Confirmed"])
                    recovered += int(element["Recovered"])
                    deaths += int(element["Deaths"])
                elif country in element["Country/Region"].lower():
                    confirmed_cases += int(element["Confirmed"])
                    recovered += int(element["Recovered"])
                    deaths += int(element["Deaths"])

            except ValueError:
                # Ignore empty values
                pass

        new_data[key] = [confirmed_cases, recovered, deaths]
        confirmed_cases = 0
        recovered = 0
        deaths = 0

    # Dates with no cases for the country get set to 0
    for key, value in new_data.items():
        if not value:
            new_data[key] = 0

    return new_data


def data_to_dataframe(cases: Dict[str, list]) -> DataFrame:
    """
    Takes dict of dates and confirmed covid-19 cases and
    re-organises it into a dictionary of lists suitable for
    converting into a pandas DataFrame.

    :param cases: Dict of dates and cases
    :return: a list of dates and a pandas DataFrame
    """
    confirmed = [element[0] for element in list(cases.values())]
    recovered = [element[1] for element in list(cases.values())]
    deaths = [element[2] for element in list(cases.values())]
    dataframe_dict = {"dates": list(cases.keys()),
                      "confirmed": confirmed,
                      "recovered": recovered,
                      "deaths": deaths}
    dataframe = DataFrame(data=dataframe_dict)
    dataframe["dates"] = pandas.to_datetime(dataframe["dates"])

    return dataframe


def build_line_plot(dataframe: DataFrame, country: str) -> None:
    """
    Creates and renders a Seaborn lineplot.

    :param country: Country for which we are plotting data
    :param dataframe: pandas DataFrame of dates and cases
    """
    sns.set_style("whitegrid")
    sns.set_context("talk")
    sns.set_palette("colorblind")

    plt.figure(figsize=(15, 9))
    ax = sns.lineplot(x="dates",
                      y="confirmed",
                      marker="o",
                      label="Confirmed",
                      data=dataframe)
    sns.lineplot(x="dates",
                 y="deaths",
                 marker="o",
                 label="Deaths",
                 data=dataframe)
    sns.lineplot(x="dates",
                 y="recovered",
                 marker="o",
                 label="Recovered",
                 data=dataframe)

    ax.set_title("COVID-19 cases by Date for " + country)
    ax.set_xlabel("Dates", fontsize=14, labelpad=10)
    ax.set_ylabel("COVID-19 Cases", fontsize=14, labelpad=10)

    plt.xticks(dataframe["dates"], get_dates(), fontsize=10, rotation=70)
    plt.yticks(fontsize=12)

    plt.setp(ax.get_legend().get_texts(), fontsize=14)

    plt.show()


def main(country: str):
    data = read_csv_files_to_dict()
    cases = extract_confirmed_cases_deaths_recovered(data, country)
    build_line_plot(data_to_dataframe(cases), country.title())
