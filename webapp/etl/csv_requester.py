"""
todo
"""
import csv
import re
from pathlib import Path
from typing import Dict, Set

import requests
from bs4 import BeautifulSoup

from ..app import app
from ..loggers.loggers import build_logger


class CSVRequester:
    """
    todo
    """
    config: dict = app.config
    new_data: dict = {}

    def __init__(self):
        self.logger = build_logger("CSVRequester")
        self.repo_url = self.config["URLs"]["githubCovid19RepoURL"]
        self.root_url = self.config["URLs"]["githubRawRootURL"]
        with open(Path(self.config["directories"]["currentDatesFile"]),
                  "r") as file_obj:
            self.current_dates = file_obj.read().splitlines()

    def check_for_new_csv(self):
        """
        todo
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
