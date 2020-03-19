"""
Here we'll transform the data retrieved by the request module.
"""


def main():
    csv_list, dates = request_csv.main()
    reduced_dicts = []
    for csv, date in zip(csv_list, dates):
        dicts = create_custom_dicts(csv, date)
        reduced_dicts.append(reduce_dicts(dicts, date))

    with open("dates.json", "w") as f:
        f.write(json.dumps(reduced_dicts, indent=2))


if __name__ == "__main__":
    main()
