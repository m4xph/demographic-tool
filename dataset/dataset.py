from statistics import mean
from typing import Union


class ThesisDataset:
    dataset_id: str
    name: str
    disability: str

    series: Union[list[dict], None]

    fixed_dict: dict = None


    def __init__(self, dataset_id, name, disability, series = None, fixed_dict = None) -> None:
        self.id, self.name, self.disability = dataset_id, name, disability


        if fixed_dict is not None:
            self.fixed_dict = fixed_dict

        if series is not None:
            self.series: list[dict] = []
            for item in series:
                self.series.append(dict(item))
        else:
            self.series = None


    def average_by_gender(self, gender: str) -> float:

        proportions = []
        for item in self.series:
            if item['gender'] == gender:

                for age in range(item["age_start"], item["age_end"]):
                    proportions.append(item['proportion'])

        return mean(proportions)


    def average_by_age_range(self, start_age: int, end_age: int) -> float:
        # This takes the mean of all series, including all entries for the multiple genders
        age_range = range(start_age, end_age + 1)  # + 1 because range skips the last integer
        proportions: list[float] = []

        for item in self.series:
            for age in age_range:
                if item['age_start'] <= age <= item['age_end']:
                    # print(f"analysing age range ${age}")

                    proportions.append(item['proportion'])

        return mean(proportions)


    def average_by_combination(self, age_start: int, age_end: int, gender: str = None) -> float:
        age_range = range(age_start, age_end + 1)  # + 1 because range skips the last integer
        proportions: list[float] = []

        for item in self.series:
            for age in age_range:
                if item['age_start'] <= age <= item['age_end']\
                        and (item['gender'] == gender or gender is None):
                    proportions.append(item['proportion'])
        return mean(proportions)

    def get_original_series_prediction(self, age_start: int, age_end: int, gender: str) -> float:
        for item in self.series:
            if item['age_start'] == age_start\
                    and item['age_end'] == age_end\
                    and item['gender'] == gender:
                return item['proportion']
        raise KeyError("invalid age, gender combination. was not found in original series")

    def get_instructions(self):
        instructions = []
        for item in self.series:
            # Do not do double for female
            if item['gender'] == 'male':
                instructions.append({
                    "age_start": item["age_start"],
                    "age_end": item["age_end"]
                })
        return instructions


