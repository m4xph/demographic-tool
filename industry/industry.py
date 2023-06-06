import json
import numpy as np
import datetime

import matplotlib.pyplot as plt

from dataset import dataset as d
from os import walk


def get_industry_demographics() -> dict:
    with open("data/industry_demographics.json", 'r') as f:
        return json.load(f)


def visualize_industry_demographics():
    timestamp = datetime.datetime.now()

    industry_config = get_industry_demographics()

    for entry in industry_config['entries']:
        age_ranges = []
        weight_counts = {
            "male": [],
            "female": [],
        }

        industry_name = entry['sector']
        male_prop = entry['male_proportion']
        female_prop = entry['female_proportion']

        print(f"male_prop{male_prop},female_prop{female_prop}")
        for serie in entry['series']:
            age_ranges.append(f"{[serie['age_start'], serie['age_end']]}")
            weight_counts["male"].append(serie['proportion'] * (male_prop / (male_prop + female_prop)))
            weight_counts["female"].append(serie['proportion'] * (female_prop / (male_prop + female_prop)))


        width = 0.5
        fig, ax = plt.subplots()
        bottom = np.zeros(len(entry['series']))

        for boolean, weight_count in weight_counts.items():
            p = ax.bar(age_ranges, weight_count, width, label=boolean, bottom=bottom)
            bottom += weight_count

        ax.set_title(f"Age and gender distribution for industry {industry_name}")
        ax.legend(loc="upper right")
        plt.ylabel(ylabel="Percentage (%) of total demographic")
        plt.xlabel(xlabel="Age ranges")
        plt.ylim(0, 35)

        plt.savefig(f"output/{timestamp}-{industry_name}.png")
        plt.show()
