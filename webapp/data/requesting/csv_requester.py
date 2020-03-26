"""
Contains a class responsible for requesting new CSV covid-19 data.
"""
import csv
import re
from pathlib import Path
from typing import Dict, Set

import requests
from bs4 import BeautifulSoup
from flask import current_app

from webapp.loggers.loggers import build_logger


class CSVRequester:
    """
    Class containing the functionality to check for new CSV data, request it,
    and write it to file should it be downloaded.
    """
    new_data: dict = {}

    def __init__(self):
        self.logger = build_logger("CSVRequester")
        self.repo_url = current_app.config["GIT_COVID_REPO_URL"]
        self.root_url = current_app.config["GITHUB_RAW_ROOT_URL"]
        with open(Path(current_app.config["CURRENT_DATES_FILE"]), "r") as f_obj:
            self.current_dates = f_obj.read().splitlines()

    def check_for_new_csv(self):
        """
        Retrieves list of urls and filenames from GitHub to eventually compare
        against already downloaded data.

        :return:
        """
        return self._get_urls()

    def request_new_csv(self, url: str, github_filename: str) -> Dict:
        """
        Checks our list of csv files against those available in
        the COVID-19 repo and identify any new ones to download.

        :return: Dict of new csv filename as key with data as value
        """
        new_data = {}
        if github_filename not in self.current_dates:
            self.logger.info("New data for %s. Downloading...", github_filename)
            response = requests.get(url).content.decode("utf-8-sig")
            self._write_new_csv_to_file(
                github_filename,
                response)
            data = csv.DictReader(response.splitlines())
            new_data[github_filename.split(".")[0]] = data
            self._write_new_date_to_file(github_filename)
        else:
            self.logger.info("Already have %s data.", github_filename)

        return new_data

    def _get_urls(self) -> Set:
        """
        Interrogates the requested HTML for hrefs leading to COVID-19
        csv data files and their filenames (dates).

        :return: Dict of URLs for csv data and filenames
        """
        a_tags = self._request_repo_html().find_all(href=re.compile(r"\.csv"))
        urls_and_filenames = set()

        for tag in a_tags:
            url = self.root_url + tag["href"].replace("blob/", "")
            urls_and_filenames.add((url, tag["title"]))

        return urls_and_filenames

    def _request_repo_html(self) -> BeautifulSoup:
        """
        Simply requests the webpage content from the daily reports
        data page of Johns Hopkins COVID-19 repo.

        :return: BeautifulSoup object of html
        """
        return BeautifulSoup(requests.get(self.repo_url).content, "lxml")

    def _write_new_date_to_file(self, date: str):
        """
        Append the date to the file of downloaded date files.

        :param date: String of date
        """
        with open(Path(self.config["directories"]["currentDatesFile"]),
                  "a") as file_obj:
            file_obj.write(date + "\n")

    def _write_new_csv_to_file(self, date: str, data: str):
        """
        Writes newly downloaded CSV data to a CSV file.

        :param date: String date to be used as the filename.
        :param data: DictReader of dicts representing CSV data.
        :return:
        """
        with open(Path("webapp/COVID-19-data/" + date), "w") as file_obj:
            writer = csv.writer(file_obj)
            for line in data.splitlines():
                writer.writerow([line.replace("\"", "")])

            self.logger.info("%s file written!", date)
