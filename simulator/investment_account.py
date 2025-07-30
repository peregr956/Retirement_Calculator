class InvestmentAccount:
    def __init__(self, name, balance, annual_return, contributions, employer_match=0, tax_type='tax_deferred'):
        self.name = name
        self.balance = balance
        self.annual_return = annual_return
        self.contributions = contributions
        self.employer_match = employer_match
        self.tax_type = tax_type
        self.history = []

    def project_year(self, year_index, is_contributing):
        if is_contributing:
            self.balance += self.contributions[year_index] + self.employer_match
        self.balance *= (1 + self.annual_return)
        self.history.append(self.balance)
