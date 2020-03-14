import csv
import os
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame


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
                with open(filename, "r", encoding="utf-8-sig") as f_obj:
                    reader = csv.DictReader(f_obj)
                    csv_dicts_list[filename.name.split(".")[0]] = list(reader)

    return csv_dicts_list


def extract_confirmed_cases(data: Dict[any, List[str]]) -> Dict[str, int]:
    """
    Creates a new dict wherein keys are sorted (ascending) dates
    and values are the confirmed cases for the UK (just UK for now).

    :param data: Dict of dates and raw csv data
    :return: Dict of dates and reduced csv data
    """
    sorted_data = dict(sorted(data.items()))
    new_data = dict.fromkeys(sorted_data.keys())

    for key, value in sorted_data.items():
        for element in value:
            # We don't want Gibraltar or Channel Island cases.
            # TODO find a nicer way of doing this.
            # Eventually filter by country, not just UK.
            if (element["Country/Region"] == "United Kingdom"
                or
                element["Country/Region"] == "UK") and (
                    element["Province/State"] != "Gibraltar"
                    and element["Province/State"] != "Channel Islands"):
                new_data[key] = int(element["Confirmed"])

    # Dates with no cases for the country get set to 0
    for key, value in new_data.items():
        if not value:
            new_data[key] = 0

    return new_data


def data_to_dataframe(cases: Dict[str, int]) -> Tuple[list, DataFrame]:
    """
    Takes dict of dates and confirmed covid-19 cases and
    re-organises it into a dictionary of lists suitable for
    converting into a pandas DataFrame.

    :param cases: Dict of dates and cases
    :return: a list of dates and a pandas DataFrame
    """
    dates = sorted([f.name.split(".")[0] for f in os.scandir("COVID-19-data")
                    if f.name.endswith("csv")])

    dataframe_dict = {"dates": list(cases.keys()), "cases": list(cases.values())}
    dataframe = DataFrame(data=dataframe_dict)

    return dates, dataframe


def build_line_plot(dates: list, dataframe: DataFrame) -> None:
    """
    Creates and renders a Seaborn lineplot.

    :param dates: sorted list of dates for x labels
    :param dataframe: pandas DataFrame of dates and cases
    """
    sns.set_style("darkgrid")

    plt.figure(figsize=(15, 8))
    ax = sns.lineplot(data=dataframe,
                      x="dates",
                      y="cases",
                      marker="o")
    ax.set_xlabel("Dates", fontsize=14, labelpad=10)
    ax.set_ylabel("Confirmed Cases", fontsize=14, labelpad=10)

    plt.xticks(dataframe["dates"], dates, fontsize=10, rotation=70)
    plt.yticks(fontsize=14)

    plt.show()
