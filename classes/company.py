class Company:
    def __init__(self, name, sector, cost, income):
        self.name = name
        self.sector = sector
        self.cost = cost
        self.income = income

    def get_info(self):
        return f"{self.name} | {self.sector} | {self.cost} ₴ | +{self.income} ₴/міс"
