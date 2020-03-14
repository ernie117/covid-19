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
    for case in ("confirmed", "recovered", "deaths"):
        print(case)
        ax = sns.lineplot(x="dates",
                          y=case,
                          marker="o",
                          markersize=5,
                          label=case.title(),
                          data=dataframe)

    font = {
        "family": "IBM Plex Mono",
        "color": "black",
        "weight": "normal",
        "size": 14,
    }

    ax.set_facecolor("#c5c8ff")
    ax.grid(color="black", linewidth=0.3)
    ax.set_xlabel("Dates", fontdict=font, labelpad=20)
    ax.set_ylabel("COVID-19 Cases", fontdict=font, labelpad=20)
    plt.xticks(dataframe["dates"], dates, fontsize=10, rotation=70)
    plt.yticks(fontsize=12)
    plt.legend(prop=FontProperties(family="IBM Plex Mono", size=12))
    plt.tight_layout()
    plt.savefig(f"{img_dir}\\{country.lower()}.png")
