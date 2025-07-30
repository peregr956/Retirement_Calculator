import pandas as pd
import math

class SimulationEngine:
    def __init__(self, user_profile, accounts):
        self.user = user_profile
        self.accounts = accounts
        self.years = list(range(self.user.current_age, self.user.end_age + 1))
        self.results = pd.DataFrame(index=self.years)

    def run_projection(self):
        salaries = self.user.projected_salaries()
        projection_years = len(self.years)

        for i, age in enumerate(self.years):
            is_contributing = age < self.user.retirement_age
            salary = salaries[i]
            for account in self.accounts:
                account.project_year(i, is_contributing, salary)

        for account in self.accounts:
            self.results[account.name] = account.history
            self.results[f"{account.name} (Today's $)"] = [
                bal / ((1 + self.user.inflation_rate) ** i) for i, bal in enumerate(account.history)
            ]

        return self.results

    def compute_monthly_income_at_retirement(self):
        """Calculate real and nominal monthly income from each account, assuming fixed real withdrawals to $0 at end_age."""
        income_summary = []

        retirement_index = self.user.retirement_age - self.user.current_age
        retirement_years = self.user.end_age - self.user.retirement_age
        total_months = retirement_years * 12

        # Real rate of return = nominal - inflation
        def monthly_withdrawal(balance, nominal_return, inflation):
            real_return = (1 + nominal_return) / (1 + inflation) - 1
            monthly_real_rate = (1 + real_return) ** (1 / 12) - 1

            if monthly_real_rate == 0:
                return balance / total_months  # fallback
            else:
                return balance * (monthly_real_rate / (1 - (1 + monthly_real_rate) ** -total_months))

        for account in self.accounts:
            balance_at_retirement = account.history[retirement_index]
            withdrawal_real = monthly_withdrawal(
                balance_at_retirement,
                account.annual_return,
                self.user.inflation_rate
            )
            withdrawal_nominal = withdrawal_real * ((1 + self.user.inflation_rate) ** retirement_years)

            income_summary.append({
                "account": account.name,
                "real_monthly": round(withdrawal_real, 2),
                "nominal_monthly_first_year": round(withdrawal_nominal, 2)
            })

        return income_summary
