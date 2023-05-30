from dataset import dataset
from helper import dataset_functions, prediction_functions

default_datasets = {
    # "visual impairment": "",
    "auditory impairment": "data/gehoorverlies.json",
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

    for industry in industries:
        for serie in industry['series']:
            get_prediction_from_dataset(datasets[0], serie['age_start'], serie['age_end'])


def get_prediction_from_dataset(ds: dataset.ThesisDataset, age_range: list[int]) -> list[float]:
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