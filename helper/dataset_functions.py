import json

import matplotlib.pyplot as plt

from dataset import dataset as d
from os import walk


def get_all_datasets() -> list[d.ThesisDataset]:
    filenames = next(walk("data"), (None, None, []))[2]  # [] if no file
    datasets = []
    for file in filenames:
        datasets.append(get_dataset(("data/datasets" + file)))

    return datasets


def get_dataset(file_path: str) -> d.ThesisDataset:
    with open(file_path, 'r') as f:
        data = json.load(f)
        return d.ThesisDataset(data['id'], data['name'], data['disability'], data['series'], data.get('fixed'))


def get_industry_demographics() -> dict:
    with open("data/industry_demographics.json", 'r') as f:
        return json.load(f)
