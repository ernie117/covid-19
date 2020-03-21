import csv
from pathlib import Path


class CSVWriter:
    current_filenames: str = Path("webapp/COVID-19-data/current_filenames.txt")

    def __init__(self):
        self.path = Path("webapp/COVID-19-data/")

    def write_data(self, data):
        """
        todo
        :param data:
        :return:
        """
        if not data:
            return

        for key, value in data.items():
            with open(self.path + key, "w", encoding="utf-8", newline="") as obj:
                reader = csv.reader(value.splitlines())
                writer = csv.writer(obj)
                writer.writerows(reader)
                print(key + " file written!")

            with open(self.current_filenames, "a") as file_obj:
                file_obj.write(key + "\n")
