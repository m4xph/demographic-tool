class AgeEntry:
    age_start: int
    age_end: int

    population_count: int

    def __init__(self, age_start, age_end, pop_count):
        self.age_start = age_start
        self.age_end = age_end
        self.population_count = pop_count


def get_dutch_age_distributions() -> list[AgeEntry]:
    return [
        AgeEntry(0, 4, 864653),
        AgeEntry(5, 9, 894620),
        AgeEntry(10, 14, 953188),
        AgeEntry(15, 19, 1025356),
        AgeEntry(20, 24, 1132885),
        AgeEntry(25, 29, 1134506),
        AgeEntry(30, 34, 1148479),
        AgeEntry(35, 39, 1071971),
        AgeEntry(40, 44, 1044047),
        AgeEntry(45, 49, 1088454),
        AgeEntry(50, 54, 1283070),
        AgeEntry(55, 59, 1265493),
        AgeEntry(60, 64, 1158497),
        AgeEntry(65, 69, 1017316),
        AgeEntry(70, 74, 941425),
        AgeEntry(75, 79, 713605),
        AgeEntry(80, 84, 457540),
        AgeEntry(85, 89, 262018),
        AgeEntry(90, 94, 106740),
        AgeEntry(96, 99, 24214),
        AgeEntry(100, 100, 1146),
        AgeEntry(101, 101, 705),
        AgeEntry(102, 102, 355),
        AgeEntry(103, 103, 199),
        AgeEntry(104, 104, 104),
        AgeEntry(105, 105, 86),
    ]
class Population:
    # age_start, age_end, amount
    age_distribution_entries: list[AgeEntry]
    male_prop: int
    female_prop: int

    def __init__(self, male_prop, female_prop):
        self.male_prop = male_prop
        self.female_prop = female_prop

        self.age_distribution_entries = get_dutch_age_distributions()

    def get_total_pop(self) -> int:
        total = 0
        for entry in self.age_distribution_entries:
            total += entry.population_count
        return total


    def get_amount_of_people(self, age_start, age_end) -> int:
        pop_total = 0
        age_range = range(age_start, age_end + 1)

        for age in age_range:
            for entry in self.age_distribution_entries:
                if entry.age_start <= age <= entry.age_end:
                    pop_total += entry.population_count

        return pop_total


