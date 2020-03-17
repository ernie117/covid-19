from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

from pandas import DataFrame


def set_seaborn_features():
    sns.set_style("whitegrid")
    sns.set_context("talk")
    sns.set_palette("colorblind")


def build_line_plot(dataframe: DataFrame,
                    country: str,
                    dates: list,
                    img_dir: str) -> None:
    """
    Creates and renders a Seaborn lineplot.

    :param img_dir: Directory for image storing
    :param dates: List of dates of available data
    :param country: Country for which we are plotting data
    :param dataframe: pandas DataFrame of dates and cases
    """
    plt.figure(figsize=(15, 9))
    for case, colour in (("confirmed", "blue"),
                         ("recovered", "green"),
                         ("deaths", "orange")):
        ax = sns.lineplot(x="dates",
                          y=case,
                          marker="o",
                          markersize=5,
                          label=case.title(),
                          color=colour,
                          data=dataframe)

    font = {
        "family": "IBM Plex Mono Medium",
        "color": "black",
        "weight": "normal",
        "size": 14,
    }

    ax.set_facecolor("#6696AE")
    ax.grid(color="black", linewidth=0.3)
    ax.set_xlabel("Dates", fontdict=font, labelpad=10)
    ax.set_ylabel("COVID-19 Cases", fontdict=font, labelpad=10)
    plt.xticks(dataframe["dates"], dates, fontsize=10, rotation=70)
    plt.yticks(fontsize=12)
    plt.legend(prop=FontProperties(family="IBM Plex Mono Medium", size=12))
    plt.tight_layout(pad=0.3)
    plt.savefig(Path(f"{img_dir}/{country.lower()}.png"))
    plt.close()
