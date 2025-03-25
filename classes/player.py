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
            {"name": "ТОВ 'БудАльянс'", "type": "Компанія", "value": 1_200_000},
            {"name": "Квартира в Києві", "type": "Нерухомість", "value": 950_000},
        ]
        self.log = []

    def get_net_worth(self):
        total_assets = sum(a["value"] for a in self.assets)
        return total_assets - self.credit

    def apply_monthly_update(self):
        self.balance += self.monthly_income - self.monthly_expenses
