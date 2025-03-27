class RealEstate:
    def __init__(self, name, location, value, income=0):
        self.name = name
        self.location = location
        self.value = value
        self.income = income

    def calculate_income(self):
        return self.income

    def __str__(self):
        return f"{self.name} ({self.location}) - {self.value} ₴"


class ResidentialProperty(RealEstate):
    def __init__(self, name, location, value, income=0, tenants=0):
        super().__init__(name, location, value, income)
        self.tenants = tenants


class CommercialProperty(RealEstate):
    def __init__(self, name, location, value, income=0, business_type=None):
        super().__init__(name, location, value, income)
        self.business_type = business_type


class LandPlot(RealEstate):
    def __init__(self, name, location, value, area_sqm):
        super().__init__(name, location, value)
        self.area_sqm = area_sqm
