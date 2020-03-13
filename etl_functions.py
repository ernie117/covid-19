import csv
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("darkgrid")


def read_csv_files_to_list():
    with os.scandir("COVID-19-data") as iterator:
        csv_dicts_list = {}
        for filename in iterator:
            if filename.name.endswith("csv"):
                with open(filename, "r", encoding="utf-8-sig") as f_obj:
                    reader = csv.DictReader(f_obj)
                    csv_dicts_list[filename.name.split(".")[0]] = list(reader)

    return csv_dicts_list


def extract_confirmed_cases(data):
    sorted_data = dict(sorted(data.items()))
    new_data = dict.fromkeys(sorted_data.keys())

    for key, value in sorted_data.items():
        for element in value:
            # We don't want Gibraltar or Channel Island cases.
            # TODO find a nicer way of doing this.
            if (element["Country/Region"] == "United Kingdom"
                or
                element["Country/Region"] == "UK") and (
                    element["Province/State"] != "Gibraltar"
                    and element["Province/State"] != "Channel Islands"):
                new_data[key] = int(element["Confirmed"])

    for key, value in new_data.items():
        if not value:
            new_data[key] = 0

    print(new_data)
    return new_data


def zip_dates_and_cases(cases):
    dates = sorted([f.name.split(".")[0] for f in os.scandir("COVID-19-data")
                    if f.name.endswith("csv")])

    dataframe_dict = {"dates": list(cases.keys()), "cases": list(cases.values())}
    dataframe = pd.DataFrame(data=dataframe_dict)

    return dates, dataframe


def build_line_plot(dates, dataframe):
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=dataframe, x="dates", y="cases", marker="o")
    plt.xticks(dataframe["dates"], dates, fontsize=10, rotation=70)

    plt.show()
