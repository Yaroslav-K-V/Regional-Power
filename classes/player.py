from classes.company import Company
from classes.real_estate import *

class Player:
    def __init__(self, name, age, intelligence, charisma):
        self.name = name
        self.age = age
        self.intelligence = intelligence
        self.charisma = charisma

        self.balance = 350000
        self.monthly_income = 120000
        self.monthly_expenses = 30000

        self.loans = []

        self.assets = [
            Company("ТОВ 'ХерсонБуд'", "Будівництво", 800_000, 50_000),
            ResidentialProperty("Квартира в Києві","Кихїв",300000,3000,0)
        ]

        self.log = []

    def get_net_worth(self):
        total = 0
        for a in self.assets:
            if isinstance(a, Company):
                total += a.cost
            elif isinstance(a, dict):
                total += a.get("value", 0)
        return total

    def apply_monthly_update(self):
        company_income = 0
        loan_payment_total = 0
        for loan in self.loans[:]:
            payment = loan.apply_monthly_payment()
            self.balance -= payment
            loan_payment_total += payment
            if loan.months_remaining <= 0 or loan.remaining_balance <= 0:
                self.loans.remove(loan)

        if loan_payment_total > 0:
            self.log.insert(0, f"Платежі по кредитах: -{loan_payment_total:,} ₴".replace(",", " "))
        for a in self.assets:
            if isinstance(a, Company):
                net_income = a.calculate_net_income()
                company_income += net_income
                a.log.append(f"Прибуток за місяць: +{net_income:,} ₴".replace(",", " "))

        self.balance += self.monthly_income + company_income - self.monthly_expenses
        self.log.insert(0, f"📈 Місячний дохід: +{self.monthly_income:,} ₴, від компаній: +{company_income:,} ₴".replace(",", " "))
