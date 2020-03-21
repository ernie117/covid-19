"""
Here we'll use requests to get the raw csv data from
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
"""
import csv

import requests

from webapp.csv import get_new_csv


def download_csv(urls_dict):
    csv_data_list = []
    for url in urls_dict["urls"]:
        # Decode to remove BOMs
        response = requests.get(url).content.decode("utf-8-sig")
        csv_data_list.append(csv.DictReader(response.splitlines()))

    return csv_data_list, urls_dict["filenames"]


def main():
    html = get_new_csv.request_html_content()
    urls = get_new_csv.get_csv_a_tags(html)
    csv_data = download_csv(urls)

    return csv_data


if __name__ == "__main__":
    main()
