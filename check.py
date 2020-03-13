import csv


with open("COVID-19-data/01-31-2020.csv", "r") as f:
    reader = csv.DictReader(f)
    for thing in reader:
        print(thing)