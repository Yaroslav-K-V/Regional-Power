class Company:
    def __init__(self, name, sector, cost, income):
        self.name = name
        self.sector = sector
        self.cost = cost
        self.income = income
        self.owner = None
        self.manager = None

        self.employees = 10
        self.salary_per_employee = 5000
        self.expenses = self.employees * self.salary_per_employee
        self.reputation = 50
        self.efficiency = 1.0
        self.risk = 0.1
        self.assets_value = cost
        self.active = True

        self.debt = 0
        self.events = []
        self.log = []

    def calculate_real_income(self):
        max_employees = 50
        effective_employees = min(self.employees, max_employees)
        multiplier = effective_employees / 10
        return int(self.income * multiplier * self.efficiency)

    def calculate_net_income(self):
        return self.calculate_real_income() - self.expenses - self.debt_payment()

    def debt_payment(self):
        return int(self.debt * 0.05)

    def monthly_update(self):
        profit = self.calculate_net_income()
        self.assets_value += int(profit * 0.1)
        self.log.append(f"+{profit} ₴ прибутку")
        if self.debt > 0:
            self.log.append(f"Виплата боргу: {self.debt_payment()} ₴")
        return profit

    def hire_employees(self, count):
        self.employees += count
        self.expenses = self.employees * self.salary_per_employee
        self.log.append(f"Найнято {count} працівників")

    def fire_employees(self, count):
        self.employees = max(0, self.employees - count)
        self.expenses = self.employees * self.salary_per_employee
        self.log.append(f"Звільнено {count} працівників")

    def change_efficiency(self, delta):
        self.efficiency = max(0.1, min(2.0, self.efficiency + delta))
        self.log.append(f"Ефективність змінено до {self.efficiency:.2f}")

    def take_loan(self, amount):
        self.debt += amount
        self.log.append(f"Отримано кредит: {amount} ₴")

    def repay_loan(self, amount):
        if self.debt <= 0:
            self.log.append("Боргу немає.")
            return
        actual_payment = min(amount, self.debt)
        self.debt -= actual_payment
        self.log.append(f"Погашено кредит: {actual_payment} ₴")

    def add_event(self, event_str):
        self.events.append(event_str)
        self.log.append(f"Подія: {event_str}")

    def assign_manager(self, manager_name):
        self.manager = manager_name
        self.log.append(f"Призначено менеджера: {manager_name}")

    def get_info(self):
        return (
            f"{self.name} | Сектор: {self.sector} | Вартість: {self.cost} ₴ | "
            f"Базовий дохід: +{self.income} ₴/міс | Працівники: {self.employees} | "
            f"Ефективність: {self.efficiency:.2f} | Менеджер: {self.manager or 'Немає'}"
        )