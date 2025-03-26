import pygame
import sys

from classes.character import Character
from classes.player import Player
from classes.company import Company
from classes.company_button import CompanyButton

pygame.init()

import datetime
popup_rect = None
scroll_offset_assets = 0
scroll_offset_liabilities = 0
selected_fin_item = None
visible_assets = []
visible_liabilities = []
assets_rect = pygame.Rect(290, 180, 380, 130)


game_time = datetime.datetime(2007, 3, 24, 0, 0)
time_speed = 1.0  # 1x
paused = False
hour_interval = 1_250  # 5 секунд (в мілісекундах)
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
    name = f"А.В. Красницький #{i + 1}"
    partner = Character(name, "Бізнес-партнер", (x, y))
    partners.append(partner)


player = Player("Іван", 32, 8, 5)

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

available_companies = [
    Company("ТОВ 'ХерсонБуд'", "Будівництво", 800_000, 50_000),
    Company("ТОВ 'АгроХолдинг'", "Сільське господарство", 650_000, 42_000),
    Company("ТОВ 'Digital Media'", "Медіа", 950_000, 60_000),
]

active_event = None  # Поточна активна подія

if not active_event:
    active_event = {
        "type": "choice",  # або "info"
        "title": "Політична пропозиція",
        "text": "Вас запрошують приєднатися до партії Солідарності...",
        "options": ["Приєднатися", "Обдумати", "Відмовитися"],
        "on_choice": {
            "Приєднатися": print("Event_1_exit_1"),
            "Обдумати": print("Event_1_exit_2"),
            "Відмовитися":print("Event_1_exit_3")
        }
    }

current_screen = "main"
clicked = False

company_buttons = []

assets_area = pygame.Rect(0, 0, 0, 0)
liabilities_area = pygame.Rect(0, 0, 0, 0)


main_screen_data = {}

main_surface = pygame.Surface((WIDTH, HEIGHT))
main_needs_redraw = True


def generate_main_screen_data():
    import random
    sample_news = [
        "Уряд змінив курс валюти",
        "Енергоринок перегрітий",
        "Нові правила оподаткування",
        "Інвестори масово купують акції",
        "НБУ знизив облікову ставку"
    ]
    sample_events = [
        "Зустріч з депутатом",
        "Обговорення з МВФ",
        "Судове засідання",
        "Подача нової реформи",
        "Голосування у ВР"
    ]
    sample_assets = [
        "Активи: 4 компанії",
        "Загальна вартість: 3.5 млн ₴",
        "Дохід/міс: 120 000 ₴"
    ]

    main_screen_data.update({
        "map": ["Карта світу", "Локація: Київ"],
        "graph": [],
        "news": ["Останні новини:", random.choice(sample_news)],
        "assets": ["Стан активів:", random.choice(sample_assets)],
        "event_calendar": ["Найближча подія:", random.choice(sample_events)],
        "profile": [f"{player.name}, Вік: {player.age}",
                    f"Інтелект: {player.intelligence} | Харизма: {player.charisma}"],
        "log": ["Останні дії:", "— 23.03: Зустріч"],
        "ukraine_map": ["Мапа України", "Область: Херсон"]
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
        "log": pygame.Rect(680, 480, 690, 100),
        "ukraine_map": pygame.Rect(20, 340, 250, 240)
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



def update_game_time():
    global game_time, last_update
    now = pygame.time.get_ticks()
    if not paused and now - last_update >= hour_interval / time_speed:
        game_time += datetime.timedelta(hours=1)
        last_update = now

        if game_time.hour == 0:
            player.apply_monthly_update()


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
    for i in range(6):
        y = rect.y + 20 + i * 20
        pygame.draw.line(surface, GRAY, (rect.x + 5, y), (rect.x + rect.width - 5, y), 1)

    points = [100, 80, 90, 110, 130, 120, 140]
    for i in range(len(points) - 1):
        x1 = rect.x + 20 + i * 30
        y1 = rect.y + rect.height - points[i] * 0.4
        x2 = rect.x + 20 + (i + 1) * 30
        y2 = rect.y + rect.height - points[i + 1] * 0.4
        pygame.draw.line(surface, BLUE, (x1, y1), (x2, y2), 3)

    surface.blit(small_font.render("Графік популярності", True, DARK_GRAY), (rect.x + 10, rect.y + rect.height - 20))



def draw_assets_screen():
    global selected_fin_item
    offset_x = 250
    screen.fill(LIGHT_GRAY)

    pygame.draw.rect(screen, WHITE, (offset_x + 250, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (offset_x + 250, 50, 1000, 620), 3)

    global assets_area, liabilities_area
    assets_area = pygame.Rect(offset_x + 270, 200, 800, 210)
    liabilities_area = pygame.Rect(offset_x + 270, 440, 800, 210)

    title = medium_plus_font.render("Фінансовий огляд", True, BLACK)
    screen.blit(title, (offset_x + 270, 60))

    balance_text = small_plus_font.render(f"Баланс: {player.balance:,} ₴".replace(",", " "), True, BLACK)
    income_text = small_plus_font.render(f"Дохід/міс: {player.monthly_income:,} ₴".replace(",", " "), True, BLACK)
    screen.blit(balance_text, (offset_x + 270, 100))
    screen.blit(income_text, (offset_x + 500, 100))

    # --- АКТИВИ ---
    pygame.draw.rect(screen, WHITE, assets_area)
    pygame.draw.rect(screen, GRAY, assets_area, 1)
    screen.blit(font.render("Активи", True, BLACK), (assets_area.x, assets_area.y - 40))

    asset_surface = pygame.Surface((assets_area.width, len(player.assets) * 70), pygame.SRCALPHA)
    global visible_assets
    visible_assets.clear()

    for i, item in enumerate(player.assets):
        y = i * 70 - scroll_offset_assets
        item_rect = pygame.Rect(0, i * 70, assets_area.width, 60)
        if y + 70 > 0 and y < assets_area.height:
            pygame.draw.rect(asset_surface, WHITE, item_rect)
            pygame.draw.rect(asset_surface, GRAY, item_rect, 1)
            pygame.draw.rect(asset_surface, (240, 240, 255), item_rect, 0)

            name = small_plus_font.render(item["name"], True, BLACK)
            typ = small_font.render(item["type"], True, DARK_GRAY)
            val = small_plus_font.render(f"{item['value']:,} ₴".replace(",", " "), True, BLACK)

            asset_surface.blit(name, (20, item_rect.y + 10))
            asset_surface.blit(typ, (20, item_rect.y + 35))
            asset_surface.blit(val, (asset_surface.get_width() - 180, item_rect.y + 20))

            visible_assets.append((item, pygame.Rect(assets_area.x, assets_area.y + y, item_rect.width, item_rect.height)))

    screen.blit(asset_surface, assets_area.topleft, area=pygame.Rect(0, scroll_offset_assets, assets_area.width, assets_area.height))

    if asset_surface.get_height() > assets_area.height:
        scroll_height = max(40, assets_area.height * assets_area.height // asset_surface.get_height())
        scroll_y = assets_area.y + scroll_offset_assets * assets_area.height // asset_surface.get_height()
        pygame.draw.rect(screen, DARK_GRAY, (assets_area.right - 10, assets_area.y, 6, assets_area.height))
        pygame.draw.rect(screen, GRAY, (assets_area.right - 10, scroll_y, 6, scroll_height))

    global liabilities
    liabilities = [
        {"name": "Кредит в банку", "type": "Заборгованість", "value": f"-{player.credit:,} ₴".replace(",", " ")},
        {"name": "Щомісячні витрати", "type": "Поточні", "value": f"-{player.monthly_expenses:,} ₴/міс".replace(",", " ")},
        {"name": "Кредит в банку", "type": "Заборгованість", "value": f"-{player.credit:,} ₴".replace(",", " ")},
        {"name": "Щомісячні витрати", "type": "Поточні","value": f"-{player.monthly_expenses:,} ₴/міс".replace(",", " ")},
        {"name": "Кредит в банку", "type": "Заборгованість", "value": f"-{player.credit:,} ₴".replace(",", " ")},
        {"name": "Щомісячні витрати", "type": "Поточні","value": f"-{player.monthly_expenses:,} ₴/міс".replace(",", " ")},
        {"name": "Кредит в банку", "type": "Заборгованість", "value": f"-{player.credit:,} ₴".replace(",", " ")},
        {"name": "Щомісячні витрати", "type": "Поточні",
         "value": f"-{player.monthly_expenses:,} ₴/міс".replace(",", " ")}
    ]

    pygame.draw.rect(screen, WHITE, liabilities_area)
    pygame.draw.rect(screen, GRAY, liabilities_area, 1)
    screen.blit(font.render("Пасиви", True, BLACK), (liabilities_area.x, liabilities_area.y - 40))

    liabilities_surface = pygame.Surface((liabilities_area.width, len(liabilities) * 70), pygame.SRCALPHA)
    global visible_liabilities
    visible_liabilities.clear()

    for i, item in enumerate(liabilities):
        y = i * 70 - scroll_offset_liabilities
        item_rect = pygame.Rect(0, i * 70, liabilities_area.width, 60)
        if y + 70 > 0 and y < liabilities_area.height:
            pygame.draw.rect(liabilities_surface, WHITE, item_rect)
            pygame.draw.rect(liabilities_surface, GRAY, item_rect, 1)
            name = small_plus_font.render(item["name"], True, BLACK)
            typ = small_font.render(item["type"], True, DARK_GRAY)
            val = small_plus_font.render(item["value"], True, (200, 0, 0))

            liabilities_surface.blit(name, (20, item_rect.y + 10))
            liabilities_surface.blit(typ, (20, item_rect.y + 35))
            liabilities_surface.blit(val, (liabilities_surface.get_width() - 180, item_rect.y + 20))

            visible_liabilities.append((item, pygame.Rect(liabilities_area.x, liabilities_area.y + y, item_rect.width, item_rect.height)))

    screen.blit(liabilities_surface, liabilities_area.topleft, area=pygame.Rect(0, scroll_offset_liabilities, liabilities_area.width, liabilities_area.height))

    if liabilities_surface.get_height() > liabilities_area.height:
        scroll_height = max(40, liabilities_area.height * liabilities_area.height // liabilities_surface.get_height())
        scroll_y = liabilities_area.y + scroll_offset_liabilities * liabilities_area.height // liabilities_surface.get_height()
        pygame.draw.rect(screen, DARK_GRAY, (liabilities_area.right - 10, liabilities_area.y, 6, liabilities_area.height))
        pygame.draw.rect(screen, GRAY, (liabilities_area.right - 10, scroll_y, 6, scroll_height))

    net_worth = player.get_net_worth()
    total = medium_plus_font.render(f"Чистий капітал: {net_worth:,} ₴".replace(",", " "), True, (0, 100, 0))
    draw_game_clock(50, 40)
    screen.blit(total, (offset_x + 270, 680))

    if selected_fin_item:
        global popup_rect
        popup_rect = pygame.Rect(400, 250, 600, 200)
        pygame.draw.rect(screen, WHITE, popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 2)
        screen.blit(medium_plus_font.render("Деталі об'єкта:", True, BLACK), (popup_rect.x + 20, popup_rect.y + 20))

        for i, (k, v) in enumerate(selected_fin_item.items()):
            txt = small_plus_font.render(f"{k}: {v}", True, DARK_GRAY)
            screen.blit(txt, (popup_rect.x + 20, popup_rect.y + 60 + i * 30))




def draw_company_market_screen():
    screen.fill(LIGHT_GRAY)
    draw_game_clock(300)
    y_offset = 150

    pygame.draw.rect(screen, WHITE, (50, y_offset, 1000, 520))
    pygame.draw.rect(screen, BLACK, (50, y_offset, 1000, 520), 3)

    title = medium_plus_font.render("Створити або купити компанію", True, BLACK)
    screen.blit(title, (70, y_offset + 20))

    # Оновити список кнопок
    company_buttons.clear()

    for i, company in enumerate(available_companies):
        y = y_offset + 70 + i * 120

        pygame.draw.rect(screen, WHITE, (70, y, 960, 100))
        pygame.draw.rect(screen, GRAY, (70, y, 960, 100), 1)
        screen.blit(small_plus_font.render(company.name, True, BLACK), (90, y + 10))
        screen.blit(small_font.render(f"Сектор: {company.sector}", True, DARK_GRAY), (90, y + 40))
        screen.blit(small_font.render(f"Вартість: {company.cost:,} ₴".replace(",", " "), True, DARK_GRAY), (90, y + 65))
        screen.blit(small_font.render(f"Дохід: {company.income:,} ₴/міс".replace(",", " "), True, DARK_GRAY), (300, y + 65))

        button = CompanyButton(company, 850, y + 30, small_plus_font)
        company_buttons.append(button)
        button.draw(screen)

    pygame.draw.rect(screen, LIGHT_GRAY, (1100, 50, 250, 620))
    pygame.draw.rect(screen, GRAY, (1100, 50, 250, 620), 1)



def draw_event_popup(event):
    popup_rect = pygame.Rect(200, 150, 1000, 500)
    pygame.draw.rect(screen, WHITE, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 3)

    # Заголовок
    title = medium_plus_font.render(event["title"], True, BLACK)
    screen.blit(title, (popup_rect.x + 20, popup_rect.y + 20))

    # Текст
    lines = event["text"].split("\n")
    for i, line in enumerate(lines):
        txt = small_plus_font.render(line, True, BLACK)
        screen.blit(txt, (popup_rect.x + 20, popup_rect.y + 70 + i * 30))

    # Кнопки
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
    central_panel_offset_x = 90
    for partner in partners:
        pygame.draw.rect(screen, WHITE, partner.rect)
        pygame.draw.rect(screen, BLACK, partner.rect, 2)
        name_text = font.render(partner.name, True, BLACK)
        role_text = font.render("Бізнес-Партнер", True, DARK_GRAY)
        screen.blit(name_text, (partner.rect.x + 10, partner.rect.y + 10))
        screen.blit(role_text, (partner.rect.x + 10, partner.rect.y + 35))

    pygame.draw.rect(screen, WHITE, (250 + central_panel_offset_x, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (250 + central_panel_offset_x, 50, 1000, 620), 3)

    pygame.draw.circle(screen, DARK_GRAY, (800 + central_panel_offset_x, 150), 60)

    name = medium_plus_font.render("Player", True, BLACK)
    screen.blit(name, (300 + central_panel_offset_x, 230))

    pygame.draw.rect(screen, LIGHT_GRAY, (300 + central_panel_offset_x, 280, 250, 130))
    pygame.draw.rect(screen, LIGHT_GRAY, (570 + central_panel_offset_x, 280, 250, 130))
    pygame.draw.rect(screen, LIGHT_GRAY, (840 + central_panel_offset_x, 280, 300, 130))

    draw_text_block("Фінансовий стан\nКапітал: 3 200 000 грн\nАктиви: 4 компанії\n+15 000 грн/міс", 310 + central_panel_offset_x, 290)
    draw_text_block("Відношення\nДовіра: 50\nПідтримує: Правих", 580 + central_panel_offset_x, 290)
    draw_text_block("Імідж\nРепутація: 72%\nВплив: 456\nЮридичні проблеми: Так", 850 + central_panel_offset_x, 290)

    pygame.draw.rect(screen, LIGHT_GRAY, (840 + central_panel_offset_x, 430, 380, 220))
    pygame.draw.rect(screen, BLACK, (840 + central_panel_offset_x, 430, 380, 220), 1)
    screen.blit(font.render("Останні дії", True, BLACK), (850 + central_panel_offset_x, 440))

    for i in range(5):
        log_text = font.render(f"{20 - i}.03.2007 - Подія №{i + 1}", True, BLACK)
        screen.blit(log_text, (850 + central_panel_offset_x, 470 + i * 30))

def draw_text_block(text, x, y):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        screen.blit(small_plus_font.render(line, True, BLACK), (x, y + i * 22))


def draw_partner_screen(partner):
    screen.fill(LIGHT_GRAY)
    offset = 90

    # Профільна панель
    pygame.draw.rect(screen, WHITE, (250 + offset, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (250 + offset, 50, 1000, 620), 3)

    # Аватар
    pygame.draw.circle(screen, DARK_GRAY, (800 + offset, 150), 60)

    # Ім’я
    name = medium_plus_font.render(partner.name + " Вікторович", True, BLACK)
    screen.blit(name, (300 + offset, 230))

    # Інфо-блоки
    draw_text_block(f"Фінансовий стан\nКапітал: {partner.capital}\nАктиви: {partner.assets}\n{partner.income}", 310 + offset, 290)
    draw_text_block(f"Відношення\nДовіра: {partner.trust}\nПідтримує: {partner.supports}", 580 + offset, 290)
    draw_text_block(f"Імідж\nРепутація: {partner.reputation}\nВплив: {partner.influence}\nЮридичні проблеми: {partner.legal_issues}", 850 + offset, 290)

    # Лог
    pygame.draw.rect(screen, LIGHT_GRAY, (840 + offset, 430, 380, 220))
    pygame.draw.rect(screen, BLACK, (840 + offset, 430, 380, 220), 1)
    screen.blit(font.render("Останні дії", True, BLACK), (850 + offset, 440))

    for i, entry in enumerate(partner.log[:5]):
        log_text = font.render(entry, True, BLACK)
        screen.blit(log_text, (850 + offset, 470 + i * 30))

    # Кнопки
    pygame.draw.rect(screen, WHITE, (300 + offset, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (500 + offset, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (700 + offset, 450, 140, 40))
    screen.blit(font.render("Переговори", True, BLACK), (330 + offset, 460))
    screen.blit(font.render("Розвідка", True, BLACK), (550 + offset, 460))
    screen.blit(font.render("Дії", True, BLACK), (750 + offset, 460))

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

while True:

    update_game_time()
    draw_game_clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEWHEEL:
            if current_screen == "assets_w":
                mouse_pos = pygame.mouse.get_pos()
                if assets_area.collidepoint(mouse_pos):
                    scroll_offset_assets = max(0, min(scroll_offset_assets - event.y * 30,
                                                      max(0, len(player.assets) * 70 - assets_area.height)))
                elif liabilities_area.collidepoint(mouse_pos):
                    scroll_offset_liabilities = max(0, min(scroll_offset_liabilities - event.y * 30,
                                                           max(0, len(liabilities) * 70 - liabilities_area.height)))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if active_event:
                for label, rect in active_event["buttons"]:
                    if rect.collidepoint(event.pos):
                        active_event = None  # Закриваємо івент
                        break
                continue

            elif current_screen == "assets_w":
                if selected_fin_item and popup_rect and not popup_rect.collidepoint(event.pos):
                    selected_fin_item = None  # Закрити попап, якщо клік поза ним
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
                            player.assets.append({
                                "name": btn.company.name,
                                "type": btn.company.sector,
                                "value": btn.company.cost
                            })
                            player.monthly_income += btn.company.income
                            available_companies.remove(btn.company)
                            company_buttons.clear()
                            main_needs_redraw = True

                            timestamp = game_time.strftime("%d.%m.%Y %H:%M")
                            player.log.insert(0, f"{timestamp} — Куплено компанію: {btn.company.name}")
                        else:
                            print("❌ Недостатньо коштів")
            elif current_screen == "assets_w":
                for item, rect in visible_assets + visible_liabilities:
                    if rect.collidepoint(event.pos):
                        selected_fin_item = item
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


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if current_screen == "main":
                    current_screen = "assets_w"
                elif current_screen == "assets_w":
                    current_screen = "event_calendar"
                elif current_screen == "event_calendar":
                    current_screen = "company_creation"
                elif current_screen == "company_creation":
                    current_screen = "main"
            elif event.key == pygame.K_ESCAPE:
                    current_screen = "main"
                    selected_partner = None
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
            elif event.key == pygame.K_ESCAPE:
                if selected_fin_item:
                    selected_fin_item = None
                else:
                    current_screen = "main"
                    selected_partner = None

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
    if active_event:
        draw_event_popup(active_event)

    pygame.display.flip()
