

class AccessibilityMeasure:
    user_requirement: str
    disabilities: list[str]
    wcag_succes_criteria: list[str]

    def __init__(self, measure_dict: dict):
        self.user_requirement = measure_dict['user requirement']
        self.disabilities = measure_dict['disabilities']
        self.wcag_succes_criteria = measure_dict['WCAG success criterion']

    def get_user_requirement_text(self):
        return f"{self.user_requirement} (WCAG {self.wcag_succes_criteria})"