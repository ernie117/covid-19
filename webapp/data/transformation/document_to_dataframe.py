from typing import Dict, List

import pandas
from pandas import DataFrame

from webapp.utils.loggers import build_logger

LOGGER = build_logger("DocumentConverter")


class DocumentConverter:
    """
    todo
    """

    def __init__(self, data: List[Dict]):
        self.data = data

    def convert_dates_to_dataframe(self):
        """
        TODO

        :return:
        """
        temp_dict = {
            "dates": [],
            "confirmed": [],
            "recovered": [],
            "deaths": [],
        }

        for document in self.data:
            temp_dict["dates"].append(document["date"])
            cases = document["cases"]
            temp_dict["confirmed"].append(cases["confirmed"])
            temp_dict["recovered"].append(cases["recovered"])
            temp_dict["deaths"].append(cases["deaths"])

        LOGGER.info("Converting data to dataframe.")
        dataframe = DataFrame(data=temp_dict)
        dataframe["dates"] = pandas.to_datetime(dataframe["dates"])
        dataframe["dates"] = dataframe["dates"].dt.strftime("%m-%d")

        return dataframe
