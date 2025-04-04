import pygame
import sys
import random
from classes.character import Character
from classes.player import Player
from classes.company import Company
from classes.company_button import CompanyButton
from resources import *
from mechanics.company_generation import generate_company_list
from classes.real_estate import *
from classes.loan import *
from events.events import create_event_dnipro_tax

available_companies = []

pygame.init()

import datetime
popup_rect = None
scroll_offset_assets = 0
scroll_offset_liabilities = 0
scroll_offset_market = 0
selected_fin_item = None
selected_company = None
visible_assets = []
visible_liabilities = []
assets_rect = pygame.Rect(290, 180, 380, 130)


game_time = datetime.datetime(2007, 3, 30, 0, 0)
time_speed = 1.0
paused = False
hour_interval = 1_250
last_update = pygame.time.get_ticks()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Regional Power")

WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
DARK = (34, 25, 24)

font = pygame.font.SysFont("arial", 36)
small_font = pygame.font.SysFont("arial", 18)
small_plus_font = pygame.font.SysFont("arial", 20)
medium_plus_font = pygame.font.SysFont("arial", 30)
medium_bold_font = pygame.font.SysFont("arial", 20, bold=True)
selected_partner = None
available_speeds = [0.5, 1, 2, 5, 10, 50]
partners = []
for i in range(6):
    x = 960 + (i % 3) * 130
    y = 340 + (i // 3) * 110
    name = f"N . P . C #{i + 1}"
    partner = Character(name, "Бізнес-партнер", (x, y))
    partners.append(partner)

last_updated_month = -1
player = Player("Іван", 32, 8, 5)

balance_history = []
MAX_HISTORY_POINTS = 30

images = load_images()
images["company_bg"] = images["company_bg"].convert_alpha()

buttons = [
    {"label": "Дія", "rect": pygame.Rect(100, 450, 120, 40)},
    {"label": "Переговори", "rect": pygame.Rect(250, 450, 160, 40)},
    {"label": "Розвідка", "rect": pygame.Rect(440, 450, 140, 40)},
]

events = [
    {"date": datetime.datetime(2007, 3, 25, 14), "title": "Зустріч з інвестором", "desc": "Обговорення майбутнього фінансування."},
    {"date": datetime.datetime(2007, 3, 26, 10), "title": "Виступ у парламенті", "desc": "Запропонована нова економічна реформа."},
    {"date": datetime.datetime(2007, 3, 28, 9),  "title": "Рада безпеки", "desc": "Термінове обговорення ситуації в регіоні."},
]

new_loan = Loan("ПриватБанк", 100_000, 0.15, 12)
player.loans.append(new_loan)
player.balance += new_loan.principal
player.log.insert(0, f"{game_time.strftime('%d.%m.%Y')} — Отримано кредит 100 000 ₴ від {new_loan.lender}")


active_event = None
selected_real_estate = selected_fin_item
last_random_event_month = -10

REAL_ESTATE_TYPE_NAMES = {
    "ResidentialProperty": "Житлова",
    "CommercialProperty": "Комерційна",
    "LandPlot": "Земельна ділянка"
}


current_screen = "main"
clicked = False

company_buttons = []
real_estate_buttons = []

assets_area = pygame.Rect(0, 0, 0, 0)
liabilities_area = pygame.Rect(0, 0, 0, 0)


main_screen_data = {}

main_surface = pygame.Surface((WIDTH, HEIGHT))
main_needs_redraw = True

weekly_real_estate = [
    ResidentialProperty("1-к квартира", "Київ", 450_000, income=5000, tenants=1),
    CommercialProperty("Магазин біля вокзалу", "Харків", 900_000, income=12000, business_type="Retail"),
    LandPlot("Ділянка на дачах", "Львів", 320_000, area_sqm=600)
]


real_estate_news = [
    "Ціни на квартири зросли на 5%",
    "Комерційна нерухомість дорожчає",
    "Земельні ділянки активно скуповують фермери"
]

news_pool = [
    "Уряд змінив курс валюти",
    "Почався весняний призов",
    "Нові податкові пільги для малого бізнесу",
    "У Києві зростає попит на житло",
    "Інфляція за місяць склала 2.3%",
    "Збільшено фінансування оборони",
    "Ціни на зерно зросли",
    "Нацбанк підвищив облікову ставку",
    "Будівельна активність зросла",
    "Бізнес очікує зростання ВВП"
]

res_news = [
    "Квартири в Києві дорожчають",
    "Попит на житло зростає",
    "Ціни на житло у столичних районах б’ють рекорди",
    "Зростає інтерес до оренди квартир",
    "Ринок вторинного житла оживає",
    "Покупці масово інвестують у житло",
    "Аналітики прогнозують зростання цін на житлову нерухомість",
    "Столичні квартири стали дорожчими на 7%",
    "Зниження іпотечних ставок стимулює попит на житло"
]

com_news = [
    "Ріст цін на комерційну нерухомість",
    "Бізнес орендує більше площ",
    "Офісна нерухомість стає дефіцитом",
    "Попит на торгові площі зростає",
    "Ринок комерційної нерухомості на підйомі",
    "Нові бізнес-центри заповнені на 90%",
    "Компанії повертаються до офісного формату",
    "Ціни на магазини в центрі міста зросли на 10%",
    "Інвестори скуповують комерційні об’єкти"
]

land_news = [
    "Фермери скуповують ділянки",
    "Земля у Львові в дефіциті",
    "Попит на сільськогосподарські ділянки різко зріс",
    "Ціни на землю під будівництво ростуть",
    "Дачні масиви розпродуються миттєво",
    "Інвестори цікавляться прибережними ділянками",
    "Уряд анонсував нові дотації для фермерів",
    "Міська земля стає дорожчою",
    "Земельні аукціони збирають рекордну кількість учасників"
]


def generate_random_news():
    return "Останні новини:", random.choice(news_pool)

def generate_magazine_news():
    return ["Нерухомість:"] + [f"{p.name}, {p.value:,} грн" for p in random.sample(weekly_real_estate, min(2, len(weekly_real_estate)))]

def rounded(value, base=10_000):
    return int(round(value / base) * base)

def refresh_weekly_real_estate():
    global weekly_real_estate, real_estate_news

    weekly_real_estate = [
        ResidentialProperty("1-к квартира", "Київ", rounded(random.randint(400_000, 550_000)), income=5000, tenants=1),
        CommercialProperty("Магазин біля вокзалу", "Харків", rounded(random.randint(850_000, 950_000)), income=12000, business_type="Retail"),
        LandPlot("Ділянка на дачах", "Львів", rounded(random.randint(300_000, 350_000)), area_sqm=600)
    ]

    real_estate_news = []

    for obj in weekly_real_estate:
        if isinstance(obj, ResidentialProperty):
            real_estate_news.append(random.choice(res_news))
        elif isinstance(obj, CommercialProperty):
            real_estate_news.append(random.choice(com_news))
        elif isinstance(obj, LandPlot):
            real_estate_news.append(random.choice(land_news))

    today = game_time.strftime("%d.%m.%Y")
    real_estate_news.append(f"{today} — {random.choice(res_news)}")

def generate_main_screen_data():
    import random
    global main_screen_data
    news_pool = [
        "Уряд змінив курс валюти",
        "Почався весняний призов",
        "Нові податкові пільги для малого бізнесу",
        "У Києві зростає попит на житло",
        "Інфляція за місяць склала 2.3%",
        "Збільшено фінансування оборони",
        "Ціни на зерно зросли",
        "Національний банк підвищив облікову ставку",
        "Будівельна активність на заході зросла",
        "Бізнес впевнено дивиться в майбутнє",
    ]
    sample_events = [
        "Зустріч з депутатом",
        "Обговорення з МВФ",
        "Судове засідання",
        "Подача нової реформи",
        "Голосування у ВР"
    ]
    sample_assets = [
        "Активи:",
        "Загальна вартість:",
        "Дохід/міс:"
    ]
    sample_properties = [
    ]

    main_screen_data.update({
        "map": ["Карта світу", "Локація: Київ"],
        "graph": [],
        "news": list(generate_random_news()),
        "assets": ["Стан активів:", random.choice(sample_assets)],
        "event_calendar": ["Найближча подія:", random.choice(sample_events)],
        "profile": [ f"{player.name}, {player.age} років",
                    f"Статус: Бізнесмен",
                    f"Репутація: 72% | Вплив: 456",
                    f"Баланс: {player.balance:,} ₴".replace(",", " "),
                    f"Активи: {len(player.assets)} | Дохід: {player.monthly_income:,} ₴/міс".replace(",", " ")],
        "log": ["Останні дії:"] + player.log[:5],
        "ukraine_map": ["Мапа України", "Область: Херсон"],
        "magazine": generate_magazine_news(),
    })

generate_main_screen_data()

def draw_main_screen():
    main_surface.fill(LIGHT_GRAY)

    blocks = {
        "map": pygame.Rect(20, 20, 250, 300),
        "graph": pygame.Rect(290, 20, 250, 150),
        "news": pygame.Rect(290, 320, 380, 140),
        "assets": pygame.Rect(290, 180, 380, 130),
        "event_calendar": pygame.Rect(680, 180, 250, 280),
        "profile": pygame.Rect(950, 20, 250, 250),
        "partners": pygame.Rect(950, 300, 420, 280),
        "log": pygame.Rect(680, 480, 690, 300),
        "ukraine_map": pygame.Rect(20, 340, 250, 240),
        "magazine": pygame.Rect(290, 480, 380, 240)
    }

    for name, rect in blocks.items():
        pygame.draw.rect(main_surface, WHITE, rect)
        pygame.draw.rect(main_surface, GRAY, rect, 2)

        label = small_plus_font.render(name.replace("_", " ").title(), True, BLACK)
        main_surface.blit(label, (rect.x + 10, rect.y + 10))
        if name == "graph":
            draw_dummy_graph(rect, surface=main_surface)
            continue
        elif name == "partners":
            for partner in partners:
                partner.draw(main_surface, small_font, small_font)
        if name in main_screen_data:
            for i, line in enumerate(main_screen_data[name]):
                text = small_font.render(line, True, DARK_GRAY)
                main_surface.blit(text, (rect.x + 10, rect.y + 40 + i * 20))

def set_followup_event(new_event):
    global active_event
    active_event = new_event
def update_game_time():
    global game_time, last_update, last_updated_month, main_needs_redraw,last_random_event_month, active_event
    now = pygame.time.get_ticks()
    main_screen_data["news"] = list(generate_random_news())
    main_screen_data["magazine"] = generate_magazine_news()
    if game_time.month - last_random_event_month >= 1 or (
            game_time.month < last_random_event_month and 12 - last_random_event_month + game_time.month >= 3):
        if random.random() < 0.9:
            active_event = create_event_dnipro_tax(player, game_time)
            last_random_event_month = game_time.month

    if not paused and now - last_update >= hour_interval / time_speed:
        game_time += datetime.timedelta(hours=1)
        last_update = now
        if game_time.day == 1 and game_time.month != last_updated_month:
            refresh_weekly_real_estate()
            print(f"Місяць оновлено: {game_time.month}, оновлюємо баланс та графік.")
            company_income, loan_payment_total = player.apply_monthly_update()
            refresh_available_companies()
            update_balance_history()
            update_main_assets_block()
            last_updated_month = game_time.month
            income_entry = f"Місячний дохід: +{player.monthly_income:,} ₴, від компаній: +{company_income:,} ₴".replace(
                ",", " ")
            if loan_payment_total > 0:
                loan_entry = f"Платежі по кредитах: -{loan_payment_total:,} ₴".replace(",", " ")
                if loan_entry not in player.log[:3]:
                    player.log.insert(0, loan_entry)

            if income_entry not in player.log[:3]:
                player.log.insert(0, income_entry)
            main_screen_data["log"] = ["Останні дії:"] + player.log[:5]
            if current_screen == "main":
                main_needs_redraw = True
            else:
                main_needs_redraw = True

def update_balance_history():
    print("Додаємо точку в історію балансу!")
    balance_history.append(player.balance)
    if len(balance_history) > MAX_HISTORY_POINTS:
        balance_history.pop(0)

def draw_game_clock(x_offset=470, y_offset = 40):
    ukr_months = [
        "січня", "лютого", "березня", "квітня", "травня", "червня",
        "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"
    ]
    month_name = ukr_months[game_time.month - 1]
    time_str = f"Час: {game_time.strftime('%H:%M')}   |   {game_time.day} {month_name} {game_time.year}"
    label = small_plus_font.render(time_str, True, BLACK)
    screen.blit(label, (x_offset+100, 10))

    for i, spd in enumerate(available_speeds):
        text_color = (200, 0, 0) if paused else BLACK
        font_to_use = medium_bold_font if spd == time_speed and not paused else small_plus_font
        text = f"{int(spd) if spd >= 1 else spd}x"
        rendered = font_to_use.render(text, True, text_color)
        screen.blit(rendered, (x_offset + 100 + i * 50, y_offset))

    if paused:
        paused_label = medium_bold_font.render("", True, (200, 0, 0))
        screen.blit(paused_label, (x_offset + 100 + len(available_speeds) * 50 + 20, y_offset))

def draw_event_calendar_screen():
    screen.fill(LIGHT_GRAY)

    title = font.render("Календар подій", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    sorted_events = sorted(events, key=lambda e: e["date"])

    y = 80
    for ev in sorted_events:
        time_str = ev["date"].strftime("%d.%m.%Y %H:%M")
        pygame.draw.rect(screen, WHITE, (100, y, 1200, 60))
        pygame.draw.rect(screen, GRAY, (100, y, 1200, 60), 1)

        screen.blit(small_plus_font.render(time_str, True, BLACK), (110, y + 5))
        screen.blit(small_plus_font.render(ev["title"], True, BLACK), (300, y + 5))
        screen.blit(small_font.render(ev["desc"], True, DARK_GRAY), (300, y + 30))
        y += 70

    back_btn = pygame.Rect(50, HEIGHT - 60, 120, 40)
    pygame.draw.rect(screen, WHITE, back_btn)
    pygame.draw.rect(screen, BLACK, back_btn, 1)
    screen.blit(small_plus_font.render("← Назад", True, BLACK), (60, HEIGHT - 50))

def draw_dummy_graph(rect, surface=screen):
    padding_top = 20
    padding_bottom = 30
    padding_x = 20

    graph_width = rect.width - 2 * padding_x
    graph_height = rect.height - padding_top - padding_bottom

    pygame.draw.rect(surface, WHITE, rect)
    for i in range(6):
        y = rect.y + padding_top + i * (graph_height // 5)
        pygame.draw.line(surface, GRAY, (rect.x + padding_x, y), (rect.x + rect.width - padding_x, y), 1)

    if len(balance_history) < 2:
        surface.blit(small_font.render("Недостатньо даних", True, DARK_GRAY), (rect.x + 10, rect.y + rect.height - 20))
        return

    points = balance_history[-MAX_HISTORY_POINTS:]
    min_val = min(points)
    max_val = max(points)
    range_val = max(1, max_val - min_val)
    scaled = [(p - min_val) / range_val for p in points]

    step_x = graph_width / (len(scaled) - 1)

    for i in range(len(scaled) - 1):
        x1 = int(rect.x + padding_x + i * step_x)
        y1 = int(rect.y + padding_top + graph_height * (1 - scaled[i]))
        x2 = int(rect.x + padding_x + (i + 1) * step_x)
        y2 = int(rect.y + padding_top + graph_height * (1 - scaled[i + 1]))
        pygame.draw.line(surface, BLUE, (x1, y1), (x2, y2), 2)

    min_text = small_font.render(f"{min_val:,} ₴".replace(",", " "), True, DARK_GRAY)
    max_text = small_font.render(f"{max_val:,} ₴".replace(",", " "), True, DARK_GRAY)
    surface.blit(max_text, (rect.x + 5, rect.y + padding_top - 15))
    surface.blit(min_text, (rect.x + 5, rect.y + padding_top + graph_height))

    surface.blit(small_font.render("Баланс гравця (історія)", True, DARK_GRAY), (rect.x + 10, rect.y + rect.height - 20))
    print("Balance history:", balance_history)

def draw_assets_screen():
    global selected_fin_item, popup_rect
    screen.fill(LIGHT_GRAY)
    offset_x = 250

    panel_rect = pygame.Rect(offset_x + 250, 50, 1000, 620)
    pygame.draw.rect(screen, WHITE, panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 3)

    screen.blit(medium_plus_font.render("Фінансовий огляд", True, BLACK), (offset_x + 270, 60))
    screen.blit(small_plus_font.render(f"Баланс: {player.balance:,} ₴".replace(",", " "), True, BLACK), (offset_x + 270, 100))
    screen.blit(small_plus_font.render(f"Дохід/міс: {player.monthly_income:,} ₴".replace(",", " "), True, BLACK), (offset_x + 500, 100))

    global liabilities
    liabilities = player.loans[:]

    global assets_area, liabilities_area
    assets_area = pygame.Rect(offset_x + 270, 200, 800, 210)
    pygame.draw.rect(screen, WHITE, assets_area)
    pygame.draw.rect(screen, GRAY, assets_area, 1)
    screen.blit(font.render("Активи", True, BLACK), (assets_area.x, assets_area.y - 40))

    asset_surface = pygame.Surface((assets_area.width, len(player.assets) * 70), pygame.SRCALPHA)
    visible_assets.clear()

    for i, item in enumerate(player.assets):
        item_y = i * 70
        item_rect = pygame.Rect(0, item_y, assets_area.width, 60)
        pygame.draw.rect(asset_surface, (240, 240, 255), item_rect)
        pygame.draw.rect(asset_surface, GRAY, item_rect, 1)

        if isinstance(item, Company):
            name_text = item.name
            type_text = item.sector
            value_text = f"{item.cost:,} ₴".replace(",", " ")
        elif isinstance(item, RealEstate):
            name_text = item.name
            type_key = type(item).__name__
            type_text = REAL_ESTATE_TYPE_NAMES.get(type_key, "Нерухомість")
            value_text = f"{item.value:,} ₴".replace(",", " ")
        else:
            name_text = item["name"]
            type_text = item["type"]
            value_text = f"{item['value']:,} ₴".replace(",", " ")

        asset_surface.blit(small_plus_font.render(name_text, True, BLACK), (20, item_y + 10))
        asset_surface.blit(small_font.render(type_text, True, DARK_GRAY), (20, item_y + 35))
        asset_surface.blit(small_plus_font.render(value_text, True, BLACK), (asset_surface.get_width() - 180, item_y + 20))

        visible_assets.append((item, pygame.Rect(assets_area.x, assets_area.y + item_y - scroll_offset_assets, item_rect.width, item_rect.height)))

    screen.blit(asset_surface, assets_area.topleft, area=pygame.Rect(0, scroll_offset_assets, assets_area.width, assets_area.height))

    if asset_surface.get_height() > assets_area.height:
        scroll_height = max(40, assets_area.height * assets_area.height // asset_surface.get_height())
        scroll_y = assets_area.y + scroll_offset_assets * assets_area.height // asset_surface.get_height()
        pygame.draw.rect(screen, DARK_GRAY, (assets_area.right - 10, assets_area.y, 6, assets_area.height))
        pygame.draw.rect(screen, GRAY, (assets_area.right - 10, scroll_y, 6, scroll_height))

    liabilities_area = pygame.Rect(offset_x + 270, 440, 800, 210)
    pygame.draw.rect(screen, WHITE, liabilities_area)
    pygame.draw.rect(screen, GRAY, liabilities_area, 1)
    screen.blit(font.render("Пасиви", True, BLACK), (liabilities_area.x, liabilities_area.y - 40))

    liabilities_surface = pygame.Surface((liabilities_area.width, len(liabilities) * 70), pygame.SRCALPHA)
    visible_liabilities.clear()

    visible_liabilities.clear()

    for i, item in enumerate(liabilities):
        item_y = i * 70
        item_rect = pygame.Rect(0, item_y, liabilities_area.width, 60)
        pygame.draw.rect(liabilities_surface, WHITE, item_rect)
        pygame.draw.rect(liabilities_surface, GRAY, item_rect, 1)

        if isinstance(item, Loan):
            name = f"Кредит від {item.lender}"
            type_info = f"{item.interest_rate * 100:.1f}% на {item.term_months} міс"
            value = f"{item.remaining_balance:,.0f} ₴".replace(",", " ")
        else:
            name = item["name"]
            type_info = item["type"]
            value = item["value"]

        liabilities_surface.blit(small_plus_font.render(name, True, BLACK), (20, item_y + 10))
        liabilities_surface.blit(small_font.render(type_info, True, DARK_GRAY), (20, item_y + 35))
        liabilities_surface.blit(small_plus_font.render(value, True, (200, 0, 0)),
                                 (liabilities_surface.get_width() - 180, item_y + 20))

        visible_liabilities.append((item, pygame.Rect(liabilities_area.x,
                                                      liabilities_area.y + item_y - scroll_offset_liabilities,
                                                      item_rect.width, item_rect.height)))

    screen.blit(liabilities_surface, liabilities_area.topleft, area=pygame.Rect(0, scroll_offset_liabilities, liabilities_area.width, liabilities_area.height))

    if liabilities_surface.get_height() > liabilities_area.height:
        scroll_height = max(40, liabilities_area.height * liabilities_area.height // liabilities_surface.get_height())
        scroll_y = liabilities_area.y + scroll_offset_liabilities * liabilities_area.height // liabilities_surface.get_height()
        pygame.draw.rect(screen, DARK_GRAY, (liabilities_area.right - 10, liabilities_area.y, 6, liabilities_area.height))
        pygame.draw.rect(screen, GRAY, (liabilities_area.right - 10, scroll_y, 6, scroll_height))

    net_worth = int(player.get_net_worth())
    screen.blit(medium_plus_font.render(f"Чистий капітал: {net_worth:,} ₴".replace(",", " "), True, (0, 150, 0)), (offset_x + 270, 680))

    if selected_fin_item:
        draw_asset_popup(selected_fin_item, 260)

def draw_company_manage_screen(company):
    screen.fill(LIGHT_GRAY)

    main_rect = pygame.Rect(150, 50, 1100, 620)

    bg_image = pygame.transform.scale(images["company_bg"], main_rect.size)
    overlay = pygame.Surface(main_rect.size, pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))
    bg_image.blit(overlay, (0, 0))
    screen.blit(bg_image, main_rect.topleft)

    pygame.draw.rect(screen, BLACK, main_rect, 3)

    title = medium_plus_font.render(company.name, True, BLACK)
    screen.blit(title, (170, 60))

    info_lines = [
        f"Сектор: {company.sector}",
        f"Базовий дохід: {company.income} ₴/міс",
        f"Ефективність: {company.efficiency:.2f}",
        f"Працівники: {company.employees}",
        f"Витрати: {company.expenses} ₴/міс",
        f"Кредит: {company.debt} ₴",
        f"Чистий прибуток: {company.calculate_net_income()} ₴",
        f"Менеджер: {company.manager or 'Немає'}",
    ]

    for i, line in enumerate(info_lines):
        txt = small_plus_font.render(line, True, BLACK)
        screen.blit(txt, (170, 120 + i * 30))

    button_defs = [
        ("Найняти", (180, 420)),
        ("Звільнити", (320, 420)),
        ("Ефективність", (180, 470)),
        ("⬇Ефективність", (380, 470)),
        ("Кредит +50K", (180, 520)),
        ("Погасити 50K", (380, 520)),
    ]

    company.manage_btns = []
    for label, (x, y) in button_defs:
        rect = pygame.Rect(x, y, 180, 40)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        screen.blit(small_plus_font.render(label, True, BLACK), (x + 10, y + 10))
        company.manage_btns.append((label, rect))

    log_rect = pygame.Rect(650, 140, 560, 500)
    pygame.draw.rect(screen, WHITE, log_rect)
    pygame.draw.rect(screen, BLACK, log_rect, 1)
    screen.blit(font.render("Журнал компанії", True, BLACK), (650, 100))

    for i, line in enumerate(company.log[-12:][::-1]):
        log_line = small_font.render(f"— {line}", True, DARK_GRAY)
        screen.blit(log_line, (log_rect.x + 10, log_rect.y + 10 + i * 28))

def draw_asset_popup(item, anchor_y=260):
    global popup_rect

    popup_rect = pygame.Rect(400, anchor_y, 600, 220)
    pygame.draw.rect(screen, WHITE, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 2)

    screen.blit(medium_plus_font.render("Деталі об'єкта:", True, BLACK), (popup_rect.x + 20, popup_rect.y + 20))

    lines = []

    if isinstance(item, Company):
        lines = [
            f"Назва: {item.name}",
            f"Сектор: {item.sector}",
            f"Вартість: {item.cost:,} ₴".replace(",", " "),
            f"Дохід/міс: {item.income:,} ₴".replace(",", " ")
        ]
    elif isinstance(item, RealEstate):
        lines = [
            f"Назва: {item.name}",
            f"Локація: {item.location}",
            f"Вартість: {item.value:,} ₴".replace(",", " "),
            f"Дохід/міс: {item.income:,} ₴".replace(",", " ")
        ]

        if isinstance(item, ResidentialProperty):
            lines.append(f"Орендарі: {item.tenants}")
        elif isinstance(item, CommercialProperty):
            lines.append(f"Бізнес: {item.business_type or 'Невідомо'}")
        elif isinstance(item, LandPlot):
            lines.append(f"Площа: {item.area_sqm} м²")
    elif isinstance(item, dict):
        lines = [f"{k}: {v}" for k, v in item.items()]

    elif isinstance(item, Loan):
        lines = [
            f"Кредитор: {item.lender}",
            f"Тіло кредиту: {item.principal:,} ₴".replace(",", " "),
            f"Відсотки: {item.interest_rate * 100:.1f}%",
            f"Щомісячний платіж: {item.monthly_payment:,} ₴".replace(",", " "),
            f"Залишок: {item.remaining_balance:,.0f} ₴".replace(",", " "),
            f"Залишилось місяців: {item.months_remaining}"
        ]

        item.repay_btn = pygame.Rect(popup_rect.x + 20, popup_rect.y + 210, 180, 30)
        pygame.draw.rect(screen, LIGHT_GRAY, item.repay_btn)
        pygame.draw.rect(screen, BLACK, item.repay_btn, 1)
        screen.blit(small_font.render("Погасити 10 000 ₴", True, BLACK), (item.repay_btn.x + 10, item.repay_btn.y + 5))

        item.full_repay_btn = pygame.Rect(popup_rect.x + 220, popup_rect.y + 210, 200, 30)
        pygame.draw.rect(screen, LIGHT_GRAY, item.full_repay_btn)
        pygame.draw.rect(screen, BLACK, item.full_repay_btn, 1)
        screen.blit(small_font.render("Погасити повністю", True, BLACK),
                    (item.full_repay_btn.x + 10, item.full_repay_btn.y + 5))

    for i, line in enumerate(lines):
        txt = small_plus_font.render(line, True, DARK_GRAY)
        screen.blit(txt, (popup_rect.x + 20, popup_rect.y + 60 + i * 25))

    if isinstance(item, (Company, RealEstate)):
        item.manage_btn = pygame.Rect(popup_rect.x + 20, popup_rect.y + 180, 120, 30)
        pygame.draw.rect(screen, LIGHT_GRAY, item.manage_btn)
        pygame.draw.rect(screen, BLACK, item.manage_btn, 1)
        screen.blit(small_font.render("Менеджмент", True, BLACK), (item.manage_btn.x + 10, item.manage_btn.y + 5))

        item.sell_btn = pygame.Rect(popup_rect.x + 160, popup_rect.y + 180, 100, 30)
        pygame.draw.rect(screen, LIGHT_GRAY, item.sell_btn)
        pygame.draw.rect(screen, BLACK, item.sell_btn, 1)
        screen.blit(small_font.render("Продати", True, BLACK), (item.sell_btn.x + 20, item.sell_btn.y + 5))

def draw_company_market_screen():
    global company_buttons
    screen.fill(LIGHT_GRAY)
    draw_game_clock(300)
    y_offset = 150

    panel_rect = pygame.Rect(50, y_offset, 1000, 520)
    pygame.draw.rect(screen, WHITE, panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 3)

    title = medium_plus_font.render("Створити або купити компанію", True, BLACK)
    screen.blit(title, (70, y_offset + 20))

    scroll_area = pygame.Rect(70, y_offset + 70, 960, 430)
    market_surface = pygame.Surface((scroll_area.width, len(available_companies) * 120), pygame.SRCALPHA)

    company_buttons.clear()

    for i, company in enumerate(available_companies):
        y = i * 120
        pygame.draw.rect(market_surface, WHITE, (0, y, 960, 100))
        pygame.draw.rect(market_surface, GRAY, (0, y, 960, 100), 1)
        market_surface.blit(small_plus_font.render(company.name, True, BLACK), (20, y + 10))
        market_surface.blit(small_font.render(f"Сектор: {company.sector}", True, DARK_GRAY), (20, y + 40))
        market_surface.blit(small_font.render(f"Вартість: {company.cost:,} ₴".replace(",", " "), True, DARK_GRAY), (20, y + 65))
        market_surface.blit(small_font.render(f"Дохід: {company.income:,} ₴/міс".replace(",", " "), True, DARK_GRAY), (300, y + 65))

        button = CompanyButton(company, 830, y + 30, small_plus_font)
        company_buttons.append(button)
        button.draw(market_surface)

    visible_part = market_surface.subsurface(pygame.Rect(0, scroll_offset_market, scroll_area.width, scroll_area.height))
    screen.blit(visible_part, scroll_area.topleft)

    if market_surface.get_height() > scroll_area.height:
        scroll_height = max(40, scroll_area.height * scroll_area.height // market_surface.get_height())
        scroll_y = scroll_area.y + scroll_offset_market * scroll_area.height // market_surface.get_height()
        pygame.draw.rect(screen, DARK_GRAY, (scroll_area.right - 10, scroll_area.y, 6, scroll_area.height))
        pygame.draw.rect(screen, GRAY, (scroll_area.right - 10, scroll_y, 6, scroll_height))

    pygame.draw.rect(screen, LIGHT_GRAY, (1100, 50, 250, 620))
    pygame.draw.rect(screen, GRAY, (1100, 50, 250, 620), 1)

def draw_real_estate_manage_screen(real_estate):
    screen.fill(LIGHT_GRAY)
    panel_rect = pygame.Rect(150, 50, 1100, 620)

    if isinstance(real_estate, ResidentialProperty):
        bg_img = images["residential_bg"]
    elif isinstance(real_estate, CommercialProperty):
        bg_img = images["commercial_bg"]
    elif isinstance(real_estate, LandPlot):
        bg_img = images["land_bg"]
    else:
        bg_img = None

    if bg_img:
        bg_image = pygame.transform.scale(bg_img, panel_rect.size)
        screen.blit(bg_image, panel_rect.topleft)
        overlay = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        screen.blit(overlay, panel_rect.topleft)

    pygame.draw.rect(screen, BLACK, panel_rect, 3)

    title = medium_plus_font.render(real_estate.name, True, BLACK)
    screen.blit(title, (170, 60))

    lines = [
        f"Локація: {real_estate.location}",
        f"Вартість: {real_estate.value:,} ₴".replace(",", " "),
        f"Дохід/міс: {real_estate.income:,} ₴".replace(",", " "),
    ]

    if isinstance(real_estate, ResidentialProperty):
        lines.append(f"Орендарі: {real_estate.tenants}")
    elif isinstance(real_estate, CommercialProperty):
        lines.append(f"Бізнес: {real_estate.business_type or 'Невідомо'}")
    elif isinstance(real_estate, LandPlot):
        lines.append(f"Площа: {real_estate.area_sqm} м²")

    for i, line in enumerate(lines):
        txt = small_plus_font.render(line, True, BLACK)
        screen.blit(txt, (170, 120 + i * 30))

    button_defs = [
        ("Здати в оренду", (180, 420)),
        ("Звільнити", (360, 420)),
        ("Покращити", (180, 480)),
        ("Кредит +25K", (360, 480)),
        ("Погасити 25K", (180, 540)),
    ]

    real_estate.manage_btns = []
    for label, (x, y) in button_defs:
        rect = pygame.Rect(x, y, 160, 40)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        screen.blit(small_plus_font.render(label, True, BLACK), (x + 10, y + 10))
        real_estate.manage_btns.append((label, rect))

    if not hasattr(real_estate, "log"):
        real_estate.log = []

    log_rect = pygame.Rect(650, 140, 440, 460)
    pygame.draw.rect(screen, WHITE, log_rect)
    pygame.draw.rect(screen, BLACK, log_rect, 1)
    screen.blit(font.render("Журнал об'єкта", True, BLACK), (650, 100))

    for i, line in enumerate(real_estate.log[-12:][::-1]):
        log_line = small_font.render(f"— {line}", True, DARK_GRAY)
        screen.blit(log_line, (log_rect.x + 10, log_rect.y + 10 + i * 28))

def draw_event_popup(event):
    popup_rect = pygame.Rect(200, 150, 1000, 500)
    pygame.draw.rect(screen, WHITE, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 3)

    title = medium_plus_font.render(event["title"], True, BLACK)
    screen.blit(title, (popup_rect.x + 20, popup_rect.y + 20))

    lines = event["text"].split("\n")
    for i, line in enumerate(lines):
        txt = small_plus_font.render(line, True, BLACK)
        screen.blit(txt, (popup_rect.x + 20, popup_rect.y + 70 + i * 30))

    event["buttons"] = []
    if event["type"] == "info":
        btn_rect = pygame.Rect(popup_rect.x + 400, popup_rect.y + 400, 200, 40)
        pygame.draw.rect(screen, GRAY, btn_rect)
        pygame.draw.rect(screen, BLACK, btn_rect, 2)
        label = small_plus_font.render("Закрити", True, BLACK)
        screen.blit(label, (btn_rect.x + 60, btn_rect.y + 10))
        event["buttons"].append(("Закрити", btn_rect))

    elif event["type"] == "choice":
        for i, option in enumerate(event["options"]):
            btn_rect = pygame.Rect(popup_rect.x + 50 + i * 300, popup_rect.y + 400, 250, 40)
            pygame.draw.rect(screen, GRAY, btn_rect)
            pygame.draw.rect(screen, BLACK, btn_rect, 2)
            label = small_plus_font.render(option, True, BLACK)
            screen.blit(label, (btn_rect.x + 20, btn_rect.y + 10))
            event["buttons"].append((option, btn_rect))

def draw_profile_screen():
    screen.fill(LIGHT_GRAY)
    offset = 90

    panel_rect = pygame.Rect(250 + offset, 50, 1000, 620)

    pygame.draw.rect(screen, BLACK, panel_rect, 3)

    pygame.draw.circle(screen, DARK_GRAY, (800 + offset, 150), 60)
    images["company_bg"] = images["company_bg"].convert_alpha()
    images["profile_bg"] = pygame.image.load("assets/profile_bg.png").convert_alpha()

    if "avatar" in images:
        avatar_img = pygame.transform.scale(images["avatar"], (120, 120))
        screen.blit(avatar_img, (740 + offset, 90))

    if "profile_bg" in images:
        bg_img = pygame.transform.scale(images["profile_bg"], panel_rect.size)
        screen.blit(bg_img, panel_rect.topleft)

        overlay = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        screen.blit(overlay, panel_rect.topleft)
    else:
        pygame.draw.rect(screen, WHITE, panel_rect)

    screen.blit(bg_img, panel_rect.topleft)

    name_text = medium_plus_font.render(player.name, True, BLACK)
    screen.blit(name_text, (300 + offset, 60))

    status_block = [
        f"Роль: Гравець",
        f"Вік: {player.age}"
    ]

    financial_block = [
        "Фінансовий стан",
        f"Баланс: {player.balance:,} ₴".replace(",", " "),
        f"Активи: {len(player.assets)}",
        f"Доходи: {player.monthly_income:,} ₴/міс".replace(",", " ")
    ]

    image_block = [
        "Імідж",
        "Репутація: 72%",
        "Вплив: 456",
        "Юридичні проблеми: Немає"
    ]

    draw_text_block("\n".join(financial_block), 310 + offset, 130)
    draw_text_block("\n".join(status_block), 580 + offset, 130)
    draw_text_block("\n".join(image_block), 850 + offset, 130)

    pygame.draw.rect(screen, WHITE, (310 + offset, 330, 820, 300))
    pygame.draw.rect(screen, BLACK, (310 + offset, 330, 820, 300), 1)
    screen.blit(font.render("Останні дії", True, BLACK), (320 + offset, 340))

    for i, entry in enumerate(player.log[:6]):
        log_text = small_font.render(entry, True, DARK_GRAY)
        screen.blit(log_text, (320 + offset, 370 + i * 30))

def draw_text_block(text, x, y):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        screen.blit(small_plus_font.render(line, True, BLACK), (x, y + i * 22))

def update_main_assets_block():
    net_worth = player.get_net_worth()
    companies = sum(1 for a in player.assets if isinstance(a, Company))
    monthly_income = player.monthly_income
    main_screen_data["assets"] = [
        f"Активи: {companies} компаній",
        f"Загальна вартість: {int(net_worth):,} ₴".replace(",", " "),
        f"Дохід/міс: {int(monthly_income):,} ₴".replace(",", " ")
    ]

def refresh_available_companies():
    global available_companies
    available_companies = generate_company_list(n=5)

def draw_partner_screen(partner):
    screen.fill(LIGHT_GRAY)
    offset = 90

    pygame.draw.rect(screen, WHITE, (250 + offset, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (250 + offset, 50, 1000, 620), 3)

    pygame.draw.circle(screen, DARK_GRAY, (800 + offset, 150), 60)

    name = medium_plus_font.render(partner.name + " Вікторович", True, BLACK)
    screen.blit(name, (300 + offset, 230))

    draw_text_block(f"Фінансовий стан\nКапітал: {partner.capital}\nАктиви: {partner.assets}\n{partner.income}", 310 + offset, 290)
    draw_text_block(f"Відношення\nДовіра: {partner.trust}\nПідтримує: {partner.supports}", 580 + offset, 290)
    draw_text_block(f"Імідж\nРепутація: {partner.reputation}\nВплив: {partner.influence}\nЮридичні проблеми: {partner.legal_issues}", 850 + offset, 290)

    pygame.draw.rect(screen, LIGHT_GRAY, (840 + offset, 430, 380, 220))
    pygame.draw.rect(screen, BLACK, (840 + offset, 430, 380, 220), 1)
    screen.blit(font.render("Останні дії", True, BLACK), (850 + offset, 440))

    for i, entry in enumerate(partner.log[:5]):
        log_text = font.render(entry, True, BLACK)
        screen.blit(log_text, (850 + offset, 470 + i * 30))

    pygame.draw.rect(screen, WHITE, (300 + offset, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (500 + offset, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (700 + offset, 450, 140, 40))
    screen.blit(font.render("Переговори", True, BLACK), (330 + offset, 460))
    screen.blit(font.render("Розвідка", True, BLACK), (550 + offset, 460))
    screen.blit(font.render("Дії", True, BLACK), (750 + offset, 460))

def draw_real_estate_screen():
    screen.fill(LIGHT_GRAY)
    title = font.render("Газета нерухомості", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    pygame.draw.line(screen, GRAY, (WIDTH // 2, 100), (WIDTH // 2, HEIGHT - 50), 2)

    screen.blit(medium_plus_font.render("Новини", True, BLACK), (100, 100))
    for i, news in enumerate(real_estate_news):
        txt = small_plus_font.render(f"• {news}", True, DARK_GRAY)
        screen.blit(txt, (100, 150 + i * 40))

    screen.blit(medium_plus_font.render("Об'єкти для продажу", True, BLACK), (WIDTH // 2 + 40, 100))
    real_estate_buttons.clear()
    for i, obj in enumerate(weekly_real_estate):
        y = 150 + i * 120
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 + 30, y, 600, 100))
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 + 30, y, 600, 100), 1)
        obj_type = type(obj).__name__.replace("Property", "").replace("Plot", "Ділянка")
        type_text = REAL_ESTATE_TYPE_NAMES.get(type(obj).__name__, "Нерухомість")
        screen.blit(small_plus_font.render(f"{obj.name} ({type_text})", True, BLACK), (WIDTH // 2 + 40, y + 10))
        screen.blit(small_font.render(f"Локація: {obj.location}", True, DARK_GRAY), (WIDTH // 2 + 40, y + 40))
        screen.blit(
            small_font.render(f"Ціна: {obj.value:,} ₴".replace(",", " "), True, DARK_GRAY),
            (WIDTH // 2 + 40, y + 65)
        )
        buy_rect = pygame.Rect(WIDTH // 2 + 500, y + 30, 80, 30)
        pygame.draw.rect(screen, GREEN, buy_rect)
        pygame.draw.rect(screen, BLACK, buy_rect, 1)
        screen.blit(small_font.render("Купити", True, BLACK), (buy_rect.x + 10, buy_rect.y + 5))
        real_estate_buttons.append((obj, buy_rect))

def draw_player_screen(player):
    screen.fill(LIGHT_GRAY)
    offset = 90

    pygame.draw.rect(screen, WHITE, (250 + offset, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (250 + offset, 50, 1000, 620), 3)

    pygame.draw.circle(screen, DARK_GRAY, (800 + offset, 150), 60)

    name = medium_plus_font.render(player.name, True, BLACK)
    screen.blit(name, (300 + offset, 230))

    draw_text_block(
        f"Фінансовий стан\nБаланс: {player.balance} ₴\nАктиви: {len(player.assets)}\nДоходи: {player.monthly_income}",
        310 + offset, 290
    )

    draw_text_block(
        f"Характеристики\nІнтелект: {player.intelligence}\nХаризма: {player.charisma}",
        580 + offset, 290
    )

    draw_text_block(
        f"Статус\nРоль: Гравець\nВік: {player.age}",
        850 + offset, 290
    )

    pygame.draw.rect(screen, LIGHT_GRAY, (840 + offset, 430, 380, 220))
    pygame.draw.rect(screen, BLACK, (840 + offset, 430, 380, 220), 1)
    screen.blit(font.render("Останні дії", True, BLACK), (850 + offset, 440))

    for i, entry in enumerate(player.log[:5]):
        log_text = font.render(entry, True, BLACK)
        screen.blit(log_text, (850 + offset, 470 + i * 30))

def is_clicked(rect, pos):
    return rect.collidepoint(pos)

while True:

    update_game_time()
    draw_game_clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if current_screen == "assets_w":
                mouse_pos = pygame.mouse.get_pos()
                if assets_area.collidepoint(mouse_pos):
                    scroll_offset_assets = max(0, min(scroll_offset_assets - event.y * 30,
                                                      max(0, len(player.assets) * 70 - assets_area.height)))
                elif liabilities_area.collidepoint(mouse_pos):
                    scroll_offset_liabilities = max(0, min(scroll_offset_liabilities - event.y * 30,
                                                           max(0, len(liabilities) * 70 - liabilities_area.height)))
            elif current_screen == "company_creation":
                scroll_area = pygame.Rect(70, 220, 960, 430)
                if scroll_area.collidepoint(mouse_pos):
                    max_scroll = max(0, len(available_companies) * 120 - scroll_area.height)
                    scroll_offset_market = max(0, min(scroll_offset_market - event.y * 30, max_scroll))
        elif active_event and active_event["type"] == "info" and label == "Закрити":
            active_event = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if active_event:
                for label, rect in active_event["buttons"]:
                    if rect.collidepoint(event.pos):
                        choice = label
                        if active_event["type"] == "choice":
                            choice = label
                            func = active_event["on_choice"].get(choice)
                            if func:
                                active_event = func()

            elif current_screen == "company_manage" and selected_company:
                if hasattr(selected_company, "manage_btns"):
                    for label, rect in selected_company.manage_btns:
                        if rect.collidepoint(event.pos):
                            if label == "Найняти":
                                selected_company.hire_employees(1)
                            elif label == "Звільнити":
                                selected_company.fire_employees(1)
                            elif label == "Ефективність":
                                selected_company.change_efficiency(0.1)
                            elif label == "Ефективність":
                                selected_company.change_efficiency(-0.1)
                            elif label == "Кредит +50K":
                                selected_company.take_loan(50_000)
                            elif label == "Погасити 50K":
                                selected_company.repay_loan(50_000)
            elif current_screen == "real_estate_manage" and selected_real_estate:
                if hasattr(selected_real_estate, "manage_btns"):
                    for label, rect in selected_real_estate.manage_btns:
                        if rect.collidepoint(event.pos):
                            if label == "Здати в оренду":
                                selected_real_estate.income += 5000
                                selected_real_estate.log.append("Здано в оренду (+5000 ₴)")
                            elif label == "Звільнити":
                                selected_real_estate.income = 0
                                selected_real_estate.log.append("Орендарі виселені")
                            elif label == "Покращити":
                                selected_real_estate.value += 50_000
                                selected_real_estate.income += 1000
                                selected_real_estate.log.append("Об'єкт покращено")
                            elif label == "Кредит +25K":
                                if not hasattr(selected_real_estate, "debt"):
                                    selected_real_estate.debt = 0
                                selected_real_estate.debt += 25_000
                                selected_real_estate.log.append("Отримано кредит: 25 000 ₴")
                            elif label == "Погасити 25K":
                                if hasattr(selected_real_estate, "debt") and selected_real_estate.debt > 0:
                                    payment = min(25_000, selected_real_estate.debt)
                                    selected_real_estate.debt -= payment
                                    selected_real_estate.log.append(f"Погашено кредит: {payment} ₴")
            elif isinstance(selected_fin_item, Loan):
                if hasattr(selected_fin_item, "repay_btn") and selected_fin_item.repay_btn.collidepoint(event.pos):
                    repayment = 10_000
                    if player.balance >= repayment:
                        selected_fin_item.remaining_balance -= repayment
                        player.balance -= repayment
                        player.log.insert(0,
                                          f"{game_time.strftime('%d.%m.%Y')} — Частково погашено кредит: {repayment:,} ₴".replace(
                                              ",", " "))
                        if selected_fin_item.remaining_balance <= 0:
                            player.loans.remove(selected_fin_item)
                            selected_fin_item = None
                elif hasattr(selected_fin_item, "full_repay_btn") and selected_fin_item.full_repay_btn.collidepoint(
                        event.pos):
                    repayment = selected_fin_item.remaining_balance
                    if player.balance >= repayment:
                        player.balance -= repayment
                        player.log.insert(0,
                                          f"{game_time.strftime('%d.%m.%Y')} — Повністю погашено кредит: {repayment:,} ₴".replace(
                                              ",", " "))
                        player.loans.remove(selected_fin_item)
                        selected_fin_item = None
            elif current_screen == "assets_w":
                if selected_fin_item and popup_rect and popup_rect.collidepoint(event.pos):
                    if isinstance(selected_fin_item, Company):
                        if hasattr(selected_fin_item, "manage_btn") and selected_fin_item.manage_btn.collidepoint(
                                event.pos):
                            selected_company = selected_fin_item
                            current_screen = "company_manage"
                        elif hasattr(selected_fin_item, "sell_btn") and selected_fin_item.sell_btn.collidepoint(
                                event.pos):
                            player.assets.remove(selected_fin_item)
                            player.balance += selected_fin_item.cost
                            player.monthly_income -= selected_fin_item.income
                            selected_fin_item = None
                    elif isinstance(selected_fin_item, RealEstate):
                        if hasattr(selected_fin_item, "manage_btn") and selected_fin_item.manage_btn.collidepoint(
                                event.pos):
                            selected_real_estate = selected_fin_item
                            current_screen = "real_estate_manage"
                        elif hasattr(selected_fin_item, "sell_btn") and selected_fin_item.sell_btn.collidepoint(
                                event.pos):
                            player.assets.remove(selected_fin_item)
                            player.balance += selected_fin_item.value
                            player.log.insert(0,
                                              f"{game_time.strftime('%d.%m.%Y')} — Продано нерухомість: {selected_fin_item.name}")
                            selected_fin_item = None
                            selected_real_estate = None
                else:
                    if selected_fin_item and popup_rect and not popup_rect.collidepoint(event.pos):
                        selected_fin_item = None
                    else:
                        for item, rect in visible_assets + visible_liabilities:
                            if rect.collidepoint(event.pos):
                                selected_fin_item = item
                                break

            elif current_screen == "company_creation":
                for btn in company_buttons:
                    if btn.is_clicked(event.pos):
                        if player.balance >= btn.company.cost:
                            player.balance -= btn.company.cost
                            player.assets.append(btn.company)
                            player.monthly_income += btn.company.income
                            available_companies.remove(btn.company)
                            company_buttons.clear()
                            main_needs_redraw = True

                            timestamp = game_time.strftime("%d.%m.%Y %H:%M")
                            player.log.insert(0, f"{timestamp} — Куплено компанію: {btn.company.name}")
                            update_balance_history()
                        else:
                            print("Недостатньо коштів")
            elif current_screen == "assets_w":
                for item, rect in visible_assets + visible_liabilities:
                    if rect.collidepoint(event.pos):
                        selected_fin_item = item
                        break
            elif current_screen == "real_estate_market":
                for obj, rect in real_estate_buttons:
                    if rect.collidepoint(event.pos):
                        if player.balance >= obj.value:
                            player.balance -= obj.value
                            player.assets.append(obj)
                            timestamp = game_time.strftime("%d.%m.%Y %H:%M")
                            player.log.insert(0, f"{timestamp} — Куплено об'єкт: {obj.name}")
                            weekly_real_estate.remove(obj)
                            main_needs_redraw = True
                            break
                        else:
                            print("Недостатньо коштів для покупки.")

            elif current_screen == "assets_w":
                for item, rect in visible_assets:
                    if rect.collidepoint(event.pos):
                        if "name" in item and item["name"] in [c.name for c in available_companies]:
                            continue
                        for c in player.assets:
                            if isinstance(c, Company) and c.name == item["name"]:
                                selected_company = c
                                current_screen = "company_manage"
                                break
            if current_screen == "main":
                for partner in partners:
                    if partner.rect.collidepoint(event.pos):
                        selected_partner = partner
                        current_screen = "partner"
                        print(f"-> Обрано партнера: {partner.name}")
                if assets_rect.collidepoint(event.pos):
                    current_screen = "assets_w"
                event_calendar_rect = pygame.Rect(680, 180, 250, 280)
                if event_calendar_rect.collidepoint(event.pos):
                    current_screen = "event_calendar"
                profile_rect = pygame.Rect(950, 20, 180, 250)
                if profile_rect.collidepoint(event.pos):
                    current_screen = "player_profile"
                real_estate_rect = pygame.Rect(290, 480, 380, 240)
                if real_estate_rect.collidepoint(event.pos):
                    current_screen = "real_estate_market"



        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if current_screen == "main":
                    current_screen = "assets_w"
                elif current_screen == "assets_w":
                    current_screen = "event_calendar"
                elif current_screen == "event_calendar":
                    current_screen = "company_creation"
                elif current_screen == "company_creation":
                    current_screen = "real_estate_market"
                elif current_screen == "real_estate_market":
                    current_screen = "main"
            elif event.key == pygame.K_ESCAPE:
                if current_screen == "company_manage":
                    current_screen = "assets_w"
                    selected_company = None
                    selected_fin_item = None
                elif selected_fin_item:
                    selected_fin_item = None
                else:
                    current_screen = "main"
                    selected_partner = None
                    main_needs_redraw = True
            elif event.key == pygame.K_SPACE:
                        paused = not paused
            elif event.key == pygame.K_RIGHT:
                    idx = available_speeds.index(time_speed)
                    if idx < len(available_speeds) - 1:
                        time_speed = available_speeds[idx + 1]
            elif event.key == pygame.K_LEFT:
                idx = available_speeds.index(time_speed)
                if idx > 0:
                    time_speed = available_speeds[idx - 1]
            elif active_event:
                active_event = None
            elif event.type == pygame.MOUSEMOTION:
                for btn in company_buttons:
                    btn.check_hover(event.pos)

    if current_screen == "main":
        if main_needs_redraw:
            draw_main_screen()
            main_needs_redraw = False

        screen.blit(main_surface, (0, 0))
        draw_game_clock()

    elif current_screen == "profile":
        draw_profile_screen()
    elif current_screen == "partner" and selected_partner:
        draw_partner_screen(selected_partner)
    elif current_screen == "assets_w":
        draw_assets_screen()
    elif current_screen == "event_calendar":
        draw_event_calendar_screen()
    elif current_screen == "company_creation":
        draw_company_market_screen()
    elif current_screen == "player_profile":
        draw_player_screen(player)
    elif current_screen == "company_manage" and selected_company:
        draw_company_manage_screen(selected_company)
    elif current_screen == "real_estate_manage" and selected_real_estate:
        draw_real_estate_manage_screen(selected_real_estate)
    elif current_screen == "real_estate_market":
        draw_real_estate_screen()
    if active_event:
        draw_event_popup(active_event)

    pygame.display.flip()
