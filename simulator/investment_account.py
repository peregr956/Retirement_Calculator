class InvestmentAccount:
    def __init__(self, name, balance, annual_return, contributions, employer_match_pct=0.0, tax_type='tax_deferred'):
        self.name = name
        self.balance = balance
        self.annual_return = annual_return
        self.contributions = contributions  # list of contributions per year
        self.employer_match_pct = employer_match_pct  # percent of salary
        self.tax_type = tax_type
        self.history = []

    def project_year(self, year_index, is_contributing, salary):
        if is_contributing:
            employer_match = salary * self.employer_match_pct
            self.balance += self.contributions[year_index] + employer_match
        self.balance *= (1 + self.annual_return)
        self.history.append(self.balance)
