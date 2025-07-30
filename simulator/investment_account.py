class InvestmentAccount:
    def __init__(self, name, balance, annual_return, contribution, employer_match=0, tax_type='tax_deferred'):
        self.name = name
        self.balance = balance
        self.annual_return = annual_return
        self.contribution = contribution
        self.employer_match = employer_match
        self.tax_type = tax_type
        self.history = []

    def project_year(self, is_contributing):
        if is_contributing:
            self.balance += self.contribution + self.employer_match
        self.balance *= (1 + self.annual_return)
        self.history.append(self.balance)
