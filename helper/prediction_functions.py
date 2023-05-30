import json

import matplotlib.pyplot as plt

from dataset import dataset as d
from os import walk

def get_fixed_prediction_by_bias_method(dataset: d.ThesisDataset, age_start: int, age_end: int, male_proportion: float, female_proportion: float):
    male_average = male_proportion
    female_average = female_proportion
    range_average = dataset.average_by_age_range(age_start, age_end)

    all_average = (male_average + female_average) / 2
    male_difference_from_average = male_average - all_average
    male_bias = (male_difference_from_average - all_average) / all_average

    female_difference_from_average = female_average - all_average
    female_bias = (female_difference_from_average - all_average) / all_average

    male_prediction = range_average * abs(female_bias)
    female_prediction = range_average * abs(male_bias)

    return [male_prediction, female_prediction]