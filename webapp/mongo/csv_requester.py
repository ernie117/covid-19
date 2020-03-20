"""
todo
"""
import csv
import json
import re
from pathlib import Path
from typing import Dict

import requests
import yaml
from bs4 import BeautifulSoup

from webapp.mongo.csv_transformer import CSVTransformer


class CSVRequester:
    """
    todo
    """
    config: dict
    FILENAMES_FILE: str = Path("webapp/COVID-19-data/current_filenames.txt")
    new_data = {}

    def __init__(self):
        with open(Path("config/config.yml"), "r") as f_obj:
            self.config = yaml.load(f_obj, Loader=yaml.FullLoader)
        with open(self.FILENAMES_FILE, "r") as file_obj:
            self.current_filenames = file_obj.read().splitlines()

        self.repo_url = self.config["URLs"]["githubCovid19RepoURL"]
        self.root_url = self.config["URLs"]["githubRawRootURL"]

    def check_for_new_csv(self):
        """
        todo
        :return:
        """
        html = self._request_html_content()
        urls_files = self._get_urls(html)
        for url, file in zip(urls_files["urls"], urls_files["filenames"]):
            self.new_data.update(self._get_new_csv(file, url))

        return self.new_data

    def _request_html_content(self) -> BeautifulSoup:
        """
        Simply requests the webpage content from the daily reports
        data page of Johns Hopkins COVID-19 repo.

        :return: BeautifulSoup object of html
        """
        return BeautifulSoup(requests.get(self.repo_url).content, "lxml")

    def _get_urls(self, html: BeautifulSoup) -> Dict:
        """
        Interrogates the requested HTML for hrefs leading to COVID-19
        csv data files and their filenames (dates).

        :return: Dict of URLs for csv data and filenames
        """
        a_tags = html.find_all(href=re.compile(r"\.csv"))
        urls_and_filenames = {"urls": [], "filenames": []}

        for tag in a_tags:
            url = self.root_url + tag["href"].replace("blob/", "")
            urls_and_filenames["urls"].append(url)
            urls_and_filenames["filenames"].append(tag["title"])

        return urls_and_filenames

    def _get_new_csv(self, github_filename: str, url: str) -> Dict:
        """
        Checks our list of csv files against those available in
        the COVID-19 repo and identify any new ones to download.

        :return: Dict of new csv filename as key with data as value
        """
        new_data = {}
        if github_filename not in self.current_filenames:
            print("New CSV data to download...")
            response = requests.get(url).content.decode("utf-8-sig")
            data = csv.DictReader(response.splitlines())
            new_data[github_filename.split(".")[0]] = data
        else:
            print("No new CSV data.")

        return new_data
