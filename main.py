import json

import matplotlib.pyplot as plt

from dataset import dataset as d
from model import model
from industry import industry
import datetime

from os import walk
def get_all_datasets() -> list[d.ThesisDataset]:
    experiment_file_names = ["PersonenMetGebruikZVWZorgVoorZintuiglijkGehandicapten2019.json", "PersonenMetGebruikZVWZorgVoorZintuiglijkGehandicapten2018.json", "visueleBeperkingenEnEenDemografischeVerkenning2005.json", "(ai) (2020) prevelentie beperkend gehoorverlies in Nederland.json"]
    filenames = next(walk("data/datasets/"), (None, None, []))[2]  # [] if no file
    datasets = []
    for file in filenames:
        if file in experiment_file_names:
            datasets.append(get_dataset(("data/datasets/" + file)))

    return datasets


def get_dataset(file_path: str) -> d.ThesisDataset:
    with open(file_path, 'r') as f:
        data = json.load(f)
        return d.ThesisDataset(data['id'], data['name'], data['disability'], data['series'], data.get('fixed'))


def get_prediction_by_average_of_dimensions(dataset: d.ThesisDataset, age_start: int, age_end: int):
    male_average = dataset.average_by_gender('male')
    female_average = dataset.average_by_gender('female')
    range_average = dataset.average_by_age_range(age_start, age_end)

    male_prediction = (male_average + range_average) / 2
    female_prediction = (female_average + range_average) / 2

    return [male_prediction, female_prediction]


def get_prediction_by_bias_method(dataset: d.ThesisDataset, age_start: int, age_end: int):
    male_average = dataset.average_by_gender('male')
    female_average = dataset.average_by_gender('female')
    range_average = dataset.average_by_age_range(age_start, age_end)

    all_average = (male_average + female_average) / 2
    male_difference_from_average = male_average - all_average
    male_bias = (male_difference_from_average - all_average) / all_average

    female_difference_from_average = female_average - all_average
    female_bias = (female_difference_from_average - all_average) / all_average

    # male_bias = (male_average - ((male_average + female_average) / 2) / (male_average + female_average))
    # female_bias = (female_average - ((male_average + female_average) / 2) / (male_average + female_average))

    print('malebias',abs(male_bias))
    print("female_bias", abs(female_bias))
    male_prediction = range_average * abs(female_bias)
    female_prediction = range_average * abs(male_bias)

    return [male_prediction, female_prediction]


def get_delta_of_prediction(male_prediction: float, female_prediction: float, male_original: float,
                            female_original: float):
    male_delta = (male_prediction - male_original) / male_original * 100
    female_delta = (female_prediction - female_original) / female_original * 100

    return [male_delta, female_delta]


def analyze_dataset(file_path: str = None, predefined_dataset: d.ThesisDataset = None):
    dataset: d.ThesisDataset
    if predefined_dataset:
        dataset = predefined_dataset
    else:
        dataset = get_dataset(file_path)

    instructions = dataset.get_instructions()
    results: list = []
    for instruction in instructions:
        age_start = instruction['age_start']
        age_end = instruction['age_end']

        age_average = dataset.average_by_age_range(age_start, age_end)
        gender_male_average = dataset.average_by_gender('male')
        gender_female_average = dataset.average_by_gender('female')

        male_original = dataset.get_original_series_prediction(age_start, age_end, 'male')
        female_original = dataset.get_original_series_prediction(age_start, age_end, 'female')

        print(f"{dataset.name}")
        # print(
        #     F"age:{age_start}-{age_end} Original male: {round(male_original, 3)} and female: {round(female_original, 3)}")
        # Average method
        average_male, average_female = get_prediction_by_average_of_dimensions(dataset, age_start,
                                                                               age_end)
        male_delta_average, female_delta_average = get_delta_of_prediction(average_male, average_female, male_original,
                                                                           female_original)
        # print(
        #     f"age:{age_start}-{age_end} Predictions for average methods are male: {round(average_male, 3)} and female: {round(average_female, 3)}")
        # print(
        #     f"age:{age_start}-{age_end} Delta's for average method are male:{male_delta_average} and female:{female_delta_average}")

        # Bias method
        bias_male, bias_female = get_prediction_by_bias_method(dataset, age_start,
                                                               age_end)
        male_delta_bias, female_delta_bias = get_delta_of_prediction(bias_male, bias_female, male_original,
                                                                     female_original)
        print(
            f"age:{age_start}-{age_end} Predictions for bias methods are male: {round(bias_male, 3)} and female: {round(bias_female, 3)}")
        # print(
        #     f"age:{age_start}-{age_end} Delta's for bias method are male:{male_delta_bias} and female:{female_delta_bias}")

        results.append({
            "male_original": male_original,
            "male_average": average_male,
            "male_bias": bias_male,

            "female_original": female_original,
            "female_average": average_female,
            "female_bias": bias_female,

            "age_average": age_average,
            "gender_male_average": gender_male_average,
            "gender_female_average": gender_female_average,

            "age_start": age_start,
            "age_end": age_end
        })
    plot_graph_from_gender(results, 'male', dataset.name, dataset.disability)
    plot_graph_from_gender(results, 'female', dataset.name, dataset.disability)
    # plot_female(results)


def plot_graph_from_gender(results, gender, dataset_name='unknown dataset', disability="unknown disability"):
    timestamp = datetime.datetime.now()

    age_values = []
    original_line_values = []
    average_line_values = []
    bias_line_values = []
    age_average_values = []
    gender_male_average_values = []
    gender_female_average_values = []
    for result in results:
        age_values.append(result['age_start'])
        age_values.append(result['age_end'])

        original_line_values.append(result[f"{gender}_original"])
        original_line_values.append(result[f"{gender}_original"])

        bias_line_values.append(result[f"{gender}_bias"])
        bias_line_values.append(result[f"{gender}_bias"])

        average_line_values.append(result[f"{gender}_average"])
        average_line_values.append(result[f"{gender}_average"])

        age_average_values.append(result['age_average'])
        age_average_values.append(result['age_average'])
        gender_male_average_values.append(result[f"gender_{gender}_average"])
        gender_male_average_values.append(result[f"gender_{gender}_average"])

    fig, ax = plt.subplots()

    original_line, = ax.plot(age_values, original_line_values, label='Original values')
    original_line.set_color('#4daf4a')
    # original_line.set_linewidth(3)

    # Plot colors come from https://gist.github.com/thriveth/8560036 (optimal for color-blind)
    average_line, = ax.plot(age_values, average_line_values, label='Average rec. values')
    average_line.set_dashes([4, 2])
    average_line.set_color('#377eb8')#ff7f00
    bias_line, = ax.plot(age_values, bias_line_values, label='Bias rec. values', color='#ff7f00')
    bias_line.set_dashes([3, 2])
    bias_line.set_color('#ff7f00')

    age_average_line, = ax.plot(age_values, age_average_values, label='Age average')
    age_average_line.set_dashes([2, 2])
    age_average_line.set_color('#e41a1c')
    # original_line.set_dashes([2,1])
    # gender_average_line, = ax.plot(age_values, gender_male_average_values, label='Gender average')
    # gender_average_line.set_dashes([4, 2])

    ax.legend(handlelength=4)
    ax.set_title(f"Dataset {dataset_name}\n {gender} estimations for disability {disability}", wrap=True)
    plt.xlabel("Age (in years)")
    plt.ylabel(f"Prevalence estimation (in %)")
    plt.rcParams['lines.linewidth'] = 2
    plt.savefig(f"output/{timestamp}-{gender}-{dataset_name}.png")
    plt.show()


def assert_input(input_text) -> bool:
    if input_text == "Y" or input_text == "y" or input_text == "yes":
        return True

    if input_text == "N" or input_text == "n" or input_text == "no":
        return False

    return assert_input(input("Please answer with 'Y' or 'N': "))


def perform_experiment():
    use_all_datasets = assert_input(input("Would you like to use all datasets in the data directory?\n(Y/N)?: "))
    impairments = []
    datasets = get_all_datasets()

    if use_all_datasets:
        for dataset in datasets:
            analyze_dataset(predefined_dataset=dataset)
        return

    for dataset in datasets:
        if dataset.disability not in impairments:
            impairments.append(dataset.disability)

    wanted_impairments = []
    for index, impairment in enumerate(impairments):
        if assert_input(input(f"Use datasets for disability {impairment}?\n(Y/N)?: ")):
            wanted_impairments.append(impairment)

    if len(wanted_impairments) == 0:
        raise "no impairments were selected"

    for impairment in wanted_impairments:
        for dataset in datasets:
            if dataset.disability == impairment:
                analyze_dataset(predefined_dataset=dataset)


if __name__ == '__main__':

    if assert_input(input("Use demographic model?\n(Y/N)?: ")):
        model.init_model()
        print("-------------------------\nEND OF DEMOGRAPHIC MODEL\n-------------------------")


    if assert_input(input("Visualize industry demographicst?\n(Y/N)?: ")):
        industry.visualize_industry_demographics()
        print("--------------------\nEND OF VISUALIZATION\n--------------------")

    if assert_input(input("Perform experiment?\n(Y/N)?: ")):
        perform_experiment()
        print("------------------\nEND OF EXPERIMENT\n------------------")
