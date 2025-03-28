class Loan:
    def __init__(self, lender, principal, interest_rate, term_months):
        self.lender = lender
        self.principal = principal
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_balance = principal
        self.monthly_payment = self.calculate_monthly_payment()
        self.months_remaining = term_months

    def calculate_monthly_payment(self):
        r = self.interest_rate / 12
        n = self.term_months
        if r == 0:
            return self.principal / n
        return int(self.principal * r / (1 - (1 + r) ** -n))

    def apply_monthly_payment(self):
        if self.months_remaining <= 0:
            return 0

        interest = self.remaining_balance * (self.interest_rate / 12)
        principal_payment = self.monthly_payment - interest
        self.remaining_balance -= principal_payment
        self.months_remaining -= 1

        return int(self.monthly_payment)
