from classes.company import Company

class Player:
    def __init__(self, name, age, intelligence, charisma):
        self.name = name
        self.age = age
        self.intelligence = intelligence
        self.charisma = charisma

        # Економіка
        self.balance = 350000
        self.credit = 200000
        self.monthly_income = 120000
        self.monthly_expenses = 30000

        self.assets = [
            Company("ТОВ 'ХерсонБуд'", "Будівництво", 800_000, 50_000),
            {"name": "Квартира в Києві", "type": "Нерухомість", "value": 950_000},
        ]

        self.log = []

    def get_net_worth(self):
        total = 0
        for a in self.assets:
            if isinstance(a, Company):
                total += a.cost
            elif isinstance(a, dict):
                total += a.get("value", 0)
        return total - self.credit

    def apply_monthly_update(self):
        company_income = 0
        for a in self.assets:
            if isinstance(a, Company):
                net_income = a.calculate_net_income()
                company_income += net_income
                a.log.append(f"Прибуток за місяць: +{net_income:,} ₴".replace(",", " "))

        self.balance += self.monthly_income + company_income - self.monthly_expenses
        self.log.insert(0, f"📈 Місячний дохід: +{self.monthly_income:,} ₴, від компаній: +{company_income:,} ₴".replace(",", " "))
