import pygame
import sys

pygame.init()

import datetime

# Початковий ігровий час
game_time = datetime.datetime(2007, 3, 24, 0, 0)
time_speed = 1.0  # 1x
paused = False
hour_interval = 5_000  # 5 секунд (в мілісекундах)
last_update = pygame.time.get_ticks()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Екрани у Pygame")

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

available_speeds = [0.5, 1, 2, 5, 10, 50]
partners = []
for i in range(6):
    rect = pygame.Rect(20, 20 + i * 100, 300, 80)
    partners.append({"name": f"А.В. Красницький", "rect": rect})

player = {
    "name": "Іван",
    "age": 32,
    "gender": "Чоловік",
    "intelligence": 8,
    "charisma": 5
}

buttons = [
    {"label": "Дія", "rect": pygame.Rect(100, 450, 120, 40)},
    {"label": "Переговори", "rect": pygame.Rect(250, 450, 160, 40)},
    {"label": "Розвідка", "rect": pygame.Rect(440, 450, 140, 40)},
]

current_screen = "main"
clicked = False
money = 0
power = 1

assets_rect = pygame.Rect(290, 180, 380, 130)

def draw_main_screen():
    screen.fill(LIGHT_GRAY)

    blocks = {
        "map": pygame.Rect(20, 20, 250, 300),
        "graph": pygame.Rect(290, 20, 250, 150),
        "news": pygame.Rect(290, 320, 380, 140),
        "assets": assets_rect,  # глобальна змінна
        "event_calendar": pygame.Rect(680, 180, 250, 280),
        "profile": pygame.Rect(950, 20, 180, 250),
        "partners": pygame.Rect(950, 300, 420, 280),
        "log": pygame.Rect(680, 480, 690, 100),
        "ukraine_map": pygame.Rect(20, 340, 250, 240)
    }

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

    placeholder_data = {
        "map": ["Карта світу", "Локація: Київ"],
        "graph": [],  # Малюємо окремо вручну
        "news": ["Останні новини:", random.choice(sample_news)],
        "assets": ["Стан активів:", random.choice(sample_assets)],
        "event_calendar": ["Найближча подія:", random.choice(sample_events)],
        "profile": [f"{player['name']}, Вік: {player['age']}",
                    f"Інтелект: {player['intelligence']} | Харизма: {player['charisma']}"],
        "partners": ["Партнери: 6", "— Красницький, Ігоренко"],
        "log": ["Останні дії:", "— 23.03: Зустріч"],
        "ukraine_map": ["Мапа України", "Область: Херсон"]
    }

    for name, rect in blocks.items():
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, GRAY, rect, 2)

        # Назва
        label = small_plus_font.render(name.replace("_", " ").title(), True, BLACK)
        screen.blit(label, (rect.x + 10, rect.y + 10))

        # Спеціальна обробка графіка
        if name == "graph":
            draw_dummy_graph(rect)
            continue

        # Текст-заглушка
        if name in placeholder_data:
            for i, line in enumerate(placeholder_data[name]):
                text = small_font.render(line, True, DARK_GRAY)
                screen.blit(text, (rect.x + 10, rect.y + 40 + i * 20))
        draw_game_clock()

    pygame.display.flip()

def update_game_time():
    global game_time, last_update
    now = pygame.time.get_ticks()
    if not paused and now - last_update >= hour_interval / time_speed:
        game_time += datetime.timedelta(hours=1)
        last_update = now


def draw_game_clock(x_offset=470, y_offset = 40):
    # Центрована дата і час
    time_str = game_time.strftime("Час: %H:%M   |   %d %B %Y")
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


def draw_dummy_graph(rect):
    # Намалювати сітку
    for i in range(6):
        y = rect.y + 20 + i * 20
        pygame.draw.line(screen, GRAY, (rect.x + 5, y), (rect.x + rect.width - 5, y), 1)

    # Фіктивні дані
    points = [100, 80, 90, 110, 130, 120, 140]
    for i in range(len(points) - 1):
        x1 = rect.x + 20 + i * 30
        y1 = rect.y + rect.height - points[i] * 0.4
        x2 = rect.x + 20 + (i + 1) * 30
        y2 = rect.y + rect.height - points[i + 1] * 0.4
        pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 3)

    # Підпис
    screen.blit(small_font.render("Графік популярності", True, DARK_GRAY), (rect.x + 10, rect.y + rect.height - 20))


def draw_assets_screen():
    offset_x = 250  # зміщення праворуч
    screen.fill(LIGHT_GRAY)

    # Заголовок вікна
    pygame.draw.rect(screen, WHITE, (offset_x + 250, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (offset_x + 250, 50, 1000, 620), 3)

    title = medium_plus_font.render("Фінансовий огляд", True, BLACK)
    screen.blit(title, (offset_x + 270, 60))

    # Список активів
    assets = [
        {"name": "ТОВ 'БудАльянс'", "type": "Компанія", "value": "1 200 000 ₴"},
        {"name": "Квартира (Одеса)", "type": "Нерухомість", "value": "800 000 ₴"},
        {"name": "Акції 'НафтаПлюс'", "type": "Інвестиція", "value": "400 000 ₴"},
    ]

    # Список пасивів
    liabilities = [
        {"name": "Кредит в банку", "type": "Заборгованість", "value": "-350 000 ₴"},
        {"name": "Лізинг авто", "type": "Щомісячний платіж", "value": "-15 000 ₴/міс"},
    ]

    # Малюємо активи
    screen.blit(font.render("Активи", True, BLACK), (offset_x + 280, 120))
    for i, item in enumerate(assets):
        y = 160 + i * 70
        pygame.draw.rect(screen, WHITE, (offset_x + 270, y, 800, 60))
        pygame.draw.rect(screen, GRAY, (offset_x + 270, y, 800, 60), 1)
        screen.blit(small_plus_font.render(item["name"], True, BLACK), (offset_x + 290, y + 10))
        screen.blit(small_font.render(item["type"], True, DARK_GRAY), (offset_x + 290, y + 35))
        screen.blit(small_plus_font.render(item["value"], True, BLACK), (offset_x + 950, y + 20))

    # Малюємо пасиви
    screen.blit(font.render("Пасиви", True, BLACK), (offset_x + 280, 160 + len(assets) * 70 + 20))
    for i, item in enumerate(liabilities):
        y = 160 + len(assets) * 70 + 60 + i * 70
        pygame.draw.rect(screen, WHITE, (offset_x + 270, y, 800, 60))
        pygame.draw.rect(screen, GRAY, (offset_x + 270, y, 800, 60), 1)
        screen.blit(small_plus_font.render(item["name"], True, BLACK), (offset_x + 290, y + 10))
        screen.blit(small_font.render(item["type"], True, DARK_GRAY), (offset_x + 290, y + 35))
        screen.blit(small_plus_font.render(item["value"], True, (200, 0, 0)), (offset_x + 950, y + 20))

    # Підсумок
    total = medium_plus_font.render("Чистий капітал: 2 035 000 ₴", True, (0, 100, 0))
    draw_game_clock(50,40)
    screen.blit(total, (offset_x + 270, 620))



def draw_profile_screen():
    screen.fill(LIGHT_GRAY)
    central_panel_offset_x = 90
    for partner in partners:
        pygame.draw.rect(screen, WHITE, partner["rect"])
        pygame.draw.rect(screen, BLACK, partner["rect"], 2)
        name_text = font.render(partner["name"], True, BLACK)
        role_text = font.render("Бізнес-Партнер", True, DARK_GRAY)
        screen.blit(name_text, (partner["rect"].x + 10, partner["rect"].y + 10))
        screen.blit(role_text, (partner["rect"].x + 10, partner["rect"].y + 35))

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


def draw_partner_screen():
    screen.fill(LIGHT_GRAY)
    central_panel_offset_x = 90
    for partner in partners:
        pygame.draw.rect(screen, WHITE, partner["rect"])
        pygame.draw.rect(screen, BLACK, partner["rect"], 2)
        name_text = font.render(partner["name"], True, BLACK)
        role_text = font.render("Бізнес-Партнер", True, DARK_GRAY)
        screen.blit(name_text, (partner["rect"].x + 10, partner["rect"].y + 10))
        screen.blit(role_text, (partner["rect"].x + 10, partner["rect"].y + 35))

    pygame.draw.rect(screen, WHITE, (250 + central_panel_offset_x, 50, 1000, 620))
    pygame.draw.rect(screen, BLACK, (250 + central_panel_offset_x, 50, 1000, 620), 3)

    pygame.draw.circle(screen, DARK_GRAY, (800 + central_panel_offset_x, 150), 60)

    name = medium_plus_font.render(partner["name"] + " Вікторович", True, BLACK)
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

    pygame.draw.rect(screen, WHITE, (300 + central_panel_offset_x, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (500 + central_panel_offset_x, 450, 180, 40))
    pygame.draw.rect(screen, WHITE, (700 + central_panel_offset_x, 450, 140, 40))
    screen.blit(font.render("Переговори", True, BLACK), (330 + central_panel_offset_x, 460))
    screen.blit(font.render("Розвідка", True, BLACK), (550 + central_panel_offset_x, 460))
    screen.blit(font.render("Дії", True, BLACK), (750 + central_panel_offset_x, 460))

while True:

    update_game_time()
    draw_game_clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main":
                if assets_rect.collidepoint(event.pos):
                    current_screen = "assets_w"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_screen == "main":
                    current_screen = "profile"
                elif current_screen == "profile":
                    current_screen = "partner"
                elif current_screen == "partner":
                    current_screen = "assets_w"
                elif current_screen == "assets_w":
                    current_screen = "main"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    idx = available_speeds.index(time_speed)
                    if idx < len(available_speeds) - 1:
                        time_speed = available_speeds[idx + 1]
                elif event.key == pygame.K_LEFT:
                    idx = available_speeds.index(time_speed)
                    if idx > 0:
                        time_speed = available_speeds[idx - 1]

    if current_screen == "main":
        draw_main_screen()
    elif current_screen == "profile":
        draw_profile_screen()
    elif current_screen == "partner":
        draw_partner_screen()
    elif current_screen == "assets_w":
        draw_assets_screen()



    pygame.display.flip()
