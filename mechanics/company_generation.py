import random
from classes.company import Company

SECTORS = [
    ("Будівництво", 600_000, 40_000),
    ("Сільське господарство", 450_000, 30_000),
    ("Медіа", 750_000, 50_000),
    ("IT-послуги", 900_000, 60_000),
    ("Торгівля", 500_000, 35_000),
    ("Транспорт", 550_000, 38_000)
]

NAME_PREFIXES = ["ТОВ", "ПП", "ФОП"]
NAME_CORES = ["ХерсонБуд", "АгроСила", "DigitalNet", "МедіаГруп", "БізПром", "ЛогістикТранс"]

def generate_random_company():
    prefix = random.choice(NAME_PREFIXES)
    core = random.choice(NAME_CORES)
    sector, cost, income = random.choice(SECTORS)
    name = f"{prefix} '{core}'"
    return Company(name, sector, cost, income)

def generate_company_list(n=5):
    return [generate_random_company() for _ in range(n)]
