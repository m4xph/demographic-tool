from dataset import dataset, measure, age_distribution
from helper import dataset_functions, prediction_functions
from statistics import mean
import matplotlib.pyplot as plt
import json

import numpy as np
import datetime

default_datasets = {
    "visual impairment": "data/datasets/(vi) Gezondheid en zorggebruik 2021.json",
    "auditory impairment": "data/datasets/(ai) Gezondheid en zorggebruik 2021.json",
    "illiteracy": "data/datasets/(il) OECD Data.json",
    "color-blindness": "data/datasets/(cb) Color-blindness general prevelance.json",
}

default_datasets = {
    # "1": "data/datasets/rec_PersonenMetGebruikZVWZorgVoorZintuiglijkGehandicapten2018.json",
    "visual impairment": "data/datasets/rec_PersonenMetGebruikZVWZorgVoorZintuiglijkGehandicapten2019.json",
    "visual impairment-rec": "data/datasets/PersonenMetGebruikZVWZorgVoorZintuiglijkGehandicapten2019.json",
    # "3": "data/datasets/rec_visueleBeperkingenEnEenDemografischeVerkenning2005.json",
    "auditory impairment": "data/datasets/rec_(ai) (2020) prevelentie beperkend gehoorverlies in Nederland.json",
    "auditory impairment-rec": "data/datasets/(ai) (2020) prevelentie beperkend gehoorverlies in Nederland.json",
}

def assert_input(input_text, default_return = None) -> bool:
    if input_text == "Y" or input_text == "y" or input_text == "yes":
        return True

    if input_text == "N" or input_text == "n" or input_text == "no":
        return False

    if default_return is not None and input_text == "":
        return default_return

    return assert_input(input("Please answer with 'Y' or 'N': "))


def assert_industry_input(input_text, industry_names: list[str]):
    if input_text in industry_names:
        return input_text
    return assert_industry_input(input(f"What is your industry? {industry_names}\nindustry?: "), industry_names)


def init_model():
    use_default = assert_input(input("Would you like to use default datasets?\n(Y/n)?: "), True)
    print_warnings = assert_input(input("Would you like to use print warnings?\n(Y/n)?: "), True)

    datasets: list[dataset.ThesisDataset] = []

    if use_default:
        for key, value in default_datasets.items():
            datasets.append(dataset_functions.get_dataset(value))

    industries = dataset_functions.get_industry_demographics()
    industry_names: list[str] = []
    prediction_sets = []

    for ds in datasets:
        print(f"Disability: {ds.disability}\nDataset: {ds.name}\n")
        for industry in industries['entries']:
            industry_names.append(industry['sector'])
            pred = get_prediction_from_industry(industry, ds, print_warnings)
            prediction_sets.append([industry['sector'], ds.disability, pred])

            print(f"[{industry['sector']}] Estimated proportion for disability {ds.disability}: {pred}")

        print("\n\n")


    for industry in industries['entries']:
        print_results_by_industry(industry['sector'], prediction_sets)

    chosen_industry = assert_industry_input(input(f"What is your industry? {industry_names}\nindustry?: "), industry_names)

    give_advice(chosen_industry, prediction_sets)

    # for industry in industries['entries']:
    #     give_advice(industry["sector"], prediction_sets)
    #     # print_results_by_industry(industry['sector'], prediction_sets)


def print_results_by_industry(industry: str, prediction_sets: list):
    data = {}

    for pred_set in prediction_sets:
        if pred_set[0] != industry:
            continue

        data[pred_set[1]] = pred_set[2]

    disabilities = list(data.keys())
    estimations = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(disabilities, estimations, color='maroon',
            width=0.4)

    plt.xlabel("Disabilities")
    plt.ylabel(f"Percentage (%) of total {industry} demographic")
    plt.title(f"Disability for industry {industry}")
    plt.show()


def give_advice(industry: str, prediction_sets: list):
    data = {}

    # pred set [industry, disability, estimation]
    for pred_set in prediction_sets:
        if pred_set[0] != industry:
            continue

        data[pred_set[1]] = pred_set[2]
    # print(data)
    ranking = sorted(data, key=data.get, reverse=True)

    with open("data/accessibility_measures.json", 'r') as f:
        json_measures = json.load(f)['measures']

    measures: list[measure.AccessibilityMeasure] = []
    for j_measure in json_measures:
        measures.append(measure.AccessibilityMeasure(j_measure))

    print("\nYour demographics have the following disabilities:")

    for i, rank in enumerate(ranking, 1):
        print(f"{i}. {rank} ({round(data[rank], 2)}%)")

    for i, rank in enumerate(ranking):
        wcag_criteria: list[str] = []
        show = assert_input(input(f"Get accessibility measure recommendations for {rank}?\n(Y,n)?:"), True)
        if show:
            print(f"\nWe recommend you to take the following measures to make your website more accessible for group {rank}:")
            for msr in measures:
                # print(rank, msr.disabilities)
                if rank in msr.disabilities:
                    print(msr.get_user_requirement_text())

                    for criteria in msr.wcag_succes_criteria:
                        if criteria not in wcag_criteria:
                            wcag_criteria.append(criteria)
            print("\nBy implementing the following WCAG Success criteria:")
            wcag_criteria.sort()
            print(wcag_criteria)





    # print(disabilities)
    # print(estimations)

def get_prediction_from_industry(industry_config: dict, ds: dataset.ThesisDataset, print_warnings=True) -> float:
    male_prop = industry_config['male_proportion']
    female_prop = industry_config['female_proportion']
    industry_series = industry_config['series']

    population_dataset = age_distribution.Population(male_prop, female_prop)

    prediction_list: list[float] = []

    if ds.series is None:
        male_pred, female_pred = get_prediction_from_dataset(ds, [])
        # people_in_pop = population_dataset.get_total_pop()

        male_pred = male_pred
        female_pred = female_pred
        for _ in range(male_prop):
            prediction_list.append(male_pred)
        for _ in range(female_prop):
            prediction_list.append(female_pred)
        return mean(prediction_list)

    for serie in industry_series:
        age_range = [serie['age_start'], serie['age_end']]

        last_count_m = 0
        last_count_f = 0
        for age in range(age_range[0], age_range[1]):

            try:
                male_pred, female_pred = get_prediction_from_dataset(ds, [age, age])
                people_in_pop = population_dataset.get_amount_of_people(age, age)

                for _ in range(round(.0005 * serie['proportion'] * male_prop * people_in_pop)):
                    last_count_m = round(.0005 * serie['proportion'] * male_prop * people_in_pop)
                    prediction_list.append(male_pred)
                for _ in range(round(.0005 * serie['proportion'] * female_prop * people_in_pop)):
                    last_count_f = round(.0005 * serie['proportion'] * female_prop * people_in_pop)
                    prediction_list.append(female_pred)
            except:
                last_count_m = 0
                last_count_f = 0
                if print_warnings:
                    print(
                        f"    [warning] For industry {industry_config['sector']}: Could not get data for age {age} in this dataset.\n"
                        f"              This age is left out of calculations.")
                continue
        if last_count_m != 0:
            print(f"Last serie {age_range}:"
                  f"M{prediction_list[-(last_count_m + last_count_f)]}:"
                  f"F{prediction_list[-last_count_f]}")

    return sum(prediction_list) / len(prediction_list)


def get_prediction_from_dataset(ds: dataset.ThesisDataset, age_range: list[int]) -> list[float]:
    if ds.fixed_dict is not None:
        male_fixed_proportion = ds.fixed_dict['gender']['male']
        female_fixed_proportion = ds.fixed_dict['gender']['female']

        if ds.series is None:
            return [male_fixed_proportion, female_fixed_proportion]

        return prediction_functions.get_fixed_prediction_by_bias_method(ds, age_range[0],
                                                                        age_range[1],
                                                                        male_fixed_proportion,
                                                                        female_fixed_proportion
                                                                        )



    return [ds.average_by_combination(age_range[0], age_range[1], 'male'),
            ds.average_by_combination(age_range[0], age_range[1], 'female')]