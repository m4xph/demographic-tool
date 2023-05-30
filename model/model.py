from dataset import dataset
from helper import dataset_functions, prediction_functions
from statistics import mean

default_datasets = {
    # "visual impairment": "",
    "visual impairment": "data/dataset3.json",
    # "illiteracy": ""
}


def assert_input(input_text, default_return = None) -> bool:
    if input_text == "Y" or input_text == "y" or input_text == "yes":
        return True

    if input_text == "N" or input_text == "n" or input_text == "no":
        return False

    if default_return is not None and input_text == "":
        return default_return

    return assert_input(input("Please answer with 'Y' or 'N': "))


def init_model():
    use_default = assert_input(input("Would you like to use default datasets?\n(Y/N)?: "), True)

    datasets: list[dataset.ThesisDataset] = []

    if use_default:
        for key, value in default_datasets.items():
            datasets.append(dataset_functions.get_dataset(value))

    industries = dataset_functions.get_industry_demographics()

    for ds in datasets:
        for industry in industries['entries']:
            pred = get_prediction_from_industry(industry, ds)
            print(f"[{industry['sector']}] Estimated proportion for disability {ds.disability}: {pred}")


def get_prediction_from_industry(industry_config: dict, ds: dataset.ThesisDataset) -> float:
    # print(industry_config)
    male_prop = industry_config['male_proportion']
    female_prop = industry_config['female_proportion']
    series = industry_config['series']

    prediction_list: list[float] = []
    for serie in series:
        age_range = [serie['age_start'], serie['age_end']]

        male_pred, female_pred = get_prediction_from_dataset(ds, age_range)

        male_count = male_prop + age_range[1] - age_range[0]
        female_count = female_prop + age_range[1] - age_range[0]

        for _ in range(male_count):
            prediction_list.append(male_pred)
        for _ in range(female_count):
            prediction_list.append(female_pred)

    return mean(prediction_list)



def get_prediction_from_dataset(ds: dataset.ThesisDataset, age_range: list[int]) -> list[float]:
    # print(ds.fixed_dict)
    if ds.fixed_dict is not None:
        male_fixed_proportion = ds.fixed_dict['gender']['male']
        female_fixed_proportion = ds.fixed_dict['gender']['female']

        return prediction_functions.get_fixed_prediction_by_bias_method(ds, age_range[0],
                                                                                         age_range[1],
                                                                                         male_fixed_proportion,
                                                                                         female_fixed_proportion
                                                                                         )

    return [ds.average_by_combination(age_range[0], age_range[1], 'male'),
            ds.average_by_combination(age_range[0], age_range[1], 'female')]