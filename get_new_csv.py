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
    d = {"urls": [], "filenames": []}

    for tag in a_tags:
        d["urls"].append(RAW_DATA_ROOT_URL + tag["href"].replace("blob/", ""))
        d["filenames"].append(tag["title"])

    return d


def get_new_csv(dictionary):
    with open("COVID-19-data/current_filenames.txt", "r") as f:
        current_filenames = f.read().splitlines()

    new_csv_data = {}
    for github_filename in dictionary["filenames"]:
        if github_filename not in current_filenames:
            for url in dictionary["urls"]:
                if github_filename in url:
                    r = requests.get(url)
                    new_csv_data[github_filename] = r.text

    return new_csv_data


def write_new_csv(data):
    for k, v in data.items():
        with open("COVID-19-data/" + k, "w") as f:
            reader = csv.reader(v.splitlines())
            writer = csv.writer(f)
            writer.writerows(reader)


write_new_csv(
    get_new_csv(
        get_csv_a_tags(
            request_html_content()
        )
    )
)
