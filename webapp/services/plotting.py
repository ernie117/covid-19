from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
from pandas import DataFrame

from webapp.loggers.loggers import build_logger


class SeabornPlotter:

    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe
        self.logger = build_logger("SeabornPlotter")

    @staticmethod
    def set_seaborn_features():
        """
        todo
        """
        sns.set_style("whitegrid")
        sns.set_context("talk")
        sns.set_palette("colorblind")

    def build_line_plot(self, country: str) -> None:
        """
        Creates, customizes and renders a Seaborn lineplot.

        :param country: Country for which we are plotting data
        """
        self.logger.info("Building plot figure for %s date data.",
                         country)
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
                              data=self.dataframe)

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
        plt.xticks(self.dataframe["dates"],
                   self.dataframe["dates"],
                   fontsize=10,
                   rotation=70)
        plt.yticks(fontsize=12)
        plt.legend(prop=FontProperties(family="IBM Plex Mono Medium", size=12))
        plt.tight_layout(pad=0.3)
        plt.savefig(Path(f"webapp/static/images/{country}.png"))
        plt.close()
