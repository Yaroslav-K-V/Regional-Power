import random
from classes.company import Company

SECTORS = [
    ("Будівництво", 500_000, 700_000, 30_000, 50_000),
    ("Сільське господарство", 400_000, 600_000, 25_000, 40_000),
    ("Медіа", 600_000, 800_000, 40_000, 60_000),
    ("IT-послуги", 800_000, 1_200_000, 50_000, 80_000),
    ("Торгівля", 450_000, 650_000, 28_000, 45_000),
    ("Транспорт", 500_000, 750_000, 30_000, 50_000),
    ("Фінанси", 900_000, 1_500_000, 60_000, 100_000),
    ("Освіта", 300_000, 500_000, 15_000, 30_000),
    ("Енергетика", 1_000_000, 2_000_000, 80_000, 150_000),
]

NAME_PREFIXES = ["ТОВ", "ПП", "ФОП", "АТ", "Група", "Консорціум"]
NAME_CORES = [
    "ХерсонБуд", "АгроСила", "DigitalNet", "МедіаГруп", "БізПром", "ЛогістикТранс",
    "Сонячна Енергія", "ГрошіПлюс", "АкадемСервіс", "NovaSpace", "GreenStep", "СтарЛінк",
    "ІнфоСкан", "КиївТех", "ВінАгро", "AutoPro", "BioFarma", "PowerGen", "SmartTrade",
    "AgroNova", "SkyNet", "УкрФінанс", "ТехноМаркет", "FutureWay", "CloudVision",
    "ЕкоБуд", "TransExpress", "CyberCore", "UrbanLab", "ДніпроСоюз", "BlackSeaCorp",
    "MegaLink", "AI Лабораторія", "QuantumEdge", "EcoStream", "EuroSoft", "DataHub",
    "IT Генерація", "АльфаБіз", "ProInvest", "SoftSpace", "MediaLand", "FarmLogic",
    "StarAgro", "TechBuild", "GlobalTech", "NextMove", "AgroTechno", "NetGroup"
]

NAME_SUFFIXES = ["Плюс", "Інвест", "Груп", "Систем", "Сервіс", "Холдинг", "ЛТД", "Юа"]

def generate_random_company():
    prefix = random.choice(NAME_PREFIXES)
    core = random.choice(NAME_CORES)
    suffix = random.choice(NAME_SUFFIXES)
    sector, min_cost, max_cost, min_income, max_income = random.choice(SECTORS)

    cost = random.randint(min_cost, max_cost)
    income = random.randint(min_income, max_income)
    name = f"{prefix} '{core} {suffix}'"

    cost = rounded(random.randint(min_cost, max_cost))
    income = rounded(random.randint(min_income, max_income), base=5_000)

    return Company(name, sector, cost, income)

def generate_company_list(n=5):
    return [generate_random_company() for _ in range(n)]

def rounded(value, base=50_000):
    return int(round(value / base) * base)