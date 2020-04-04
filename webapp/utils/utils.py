import csv
import os

from pathlib import Path

from webapp.data.transformation.country_transformer import CountryTransformer


def purge_images():
    with os.scandir(Path("webapp/static/images")) as iterator:
        for filename in iterator:
            if filename.name.endswith("png"):
                os.remove(filename)
