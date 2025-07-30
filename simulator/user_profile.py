class UserProfile:
    def __init__(self, current_age, retirement_age, end_age, salary, salary_growth=0.02, inflation_rate=0.02):
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.end_age = end_age
        self.salary = salary
        self.salary_growth = salary_growth
        self.inflation_rate = inflation_rate

    def projected_salaries(self):
        years = self.end_age - self.current_age + 1
        return [self.salary * ((1 + self.salary_growth) ** i) for i in range(years)]
