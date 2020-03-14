import csv
import re

import requests
import yaml
from bs4 import BeautifulSoup

with open("config/config.yml", "r") as f_obj:
    CONFIG = yaml.load(f_obj, Loader=yaml.FullLoader)

RAW_DATA_ROOT_URL = CONFIG["URLs"]["githubRawRootURL"]


def request_html_content():
    html_resp = requests.get(CONFIG["URLs"]["githubCovid19RepoURL"]).content

    return BeautifulSoup(html_resp, "lxml")


def get_csv_a_tags(html):
    a_tags = html.find_all(href=re.compile(r"\.csv"))
    urls_and_filenames_dict = {"urls": [], "filenames": []}

    for tag in a_tags:
        url = RAW_DATA_ROOT_URL + tag["href"].replace("blob/", "")
        urls_and_filenames_dict["urls"].append(url)
        urls_and_filenames_dict["filenames"].append(tag["title"])

    return urls_and_filenames_dict


def get_new_csv(dictionary):
    with open("COVID-19-data/current_filenames.txt", "r") as file_obj:
        current_filenames = file_obj.read().splitlines()

    new_csv_data = {}
    for github_filename in dictionary["filenames"]:
        if github_filename not in current_filenames:
            print("New CSV data to download...")
            for url in dictionary["urls"]:
                if github_filename in url:
                    response = requests.get(url)
                    new_csv_data[github_filename] = response.text

    if not new_csv_data:
        print("No new CSV data.")

    return new_csv_data


def write_new_csv(data):
    if not data:
        return

    for key, value in data.items():
        with open("COVID-19-data/" + key,
                  "w",
                  encoding="utf-8",
                  newline="") as file_obj:
            reader = csv.reader(value.splitlines())
            writer = csv.writer(file_obj)
            writer.writerows(reader)

        with open("COVID-19-data/current_filenames.txt", "a") as file_obj:
            file_obj.write(key)


write_new_csv(
    get_new_csv(
        get_csv_a_tags(
            request_html_content()
        )
    )
)
