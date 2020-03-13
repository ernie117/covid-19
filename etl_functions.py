import csv
import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("darkgrid")


def read_csv_files_to_list():
    with os.scandir("COVID-19-data") as iterator:
        csv_dicts_list = {}
        for filename in iterator:
            if filename.name.endswith("csv"):
                with open(filename, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    csv_dicts_list[filename.name.split(".")[0]] = list(reader)

    return csv_dicts_list


def extract_confirmed_cases(data):
    sorted_data = dict(sorted(data.items()))
    new_data = dict.fromkeys(sorted_data.keys())

    for k, v in sorted_data.items():
        for element in v:
            # We don't want Gibraltar or Channel Island cases
            if ("United Kingdom" == element["Country/Region"]
                or
                "UK" == element["Country/Region"]) and (
                    element["Province/State"] != "Gibraltar"
                    and element["Province/State"] != "Channel Islands"):
                new_data[k] = int(element["Confirmed"])

    for k, v in new_data.items():
        if not v:
            new_data[k] = 0

    print(new_data)
    return new_data


def zip_dates_and_cases(cases):
    dates = sorted([f.name.split(".")[0] for f in os.scandir("COVID-19-data")
                    if f.name.endswith("csv")])

    d = {"dates": list(cases.keys()), "cases": list(cases.values())}
    df = pd.DataFrame(data=d)

    return dates, df


def build_line_plot(dates, dataframe):
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=dataframe, x="dates", y="cases", marker="o")
    plt.xticks(dataframe["dates"], dates, fontsize=10, rotation=70)

    plt.show()
