import pandas as pd

class SimulationEngine:
    def __init__(self, user_profile, accounts):
        self.user = user_profile
        self.accounts = accounts
        self.years = list(range(self.user.current_age, self.user.end_age + 1))
        self.results = pd.DataFrame(index=self.years)

    def run_projection(self):
        projection_years = len(self.years)
        for i, age in enumerate(self.years):
            is_contributing = age < self.user.retirement_age
            for account in self.accounts:
                account.project_year(i, is_contributing)

        for account in self.accounts:
            self.results[account.name] = account.history
            self.results[f"{account.name} (Today's $)"] = [
                bal / ((1 + self.user.inflation_rate) ** i) for i, bal in enumerate(account.history)
            ]

        return self.results
