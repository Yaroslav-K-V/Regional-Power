import pygame
import sys
import subprocess
import time

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Economic Lab")

font = pygame.font.SysFont("arial", 36)
button_font = pygame.font.SysFont("arial", 28)

bg_img = pygame.image.load("resources/img/menu_bg.jpg").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay.fill((255, 255, 255, 150))

buttons = [
    {"label": "Почати гру", "rect": pygame.Rect(WIDTH // 2 - 120, 360, 240, 50)},
    {"label": "Продовжити гру", "rect": pygame.Rect(WIDTH // 2 - 120, 430, 240, 50)},
    {"label": "Вийти", "rect": pygame.Rect(WIDTH // 2 - 120, 500, 240, 50)},
]

start_clicked = False
start_time = 0

running = True
while running:
    screen.blit(bg_img, (0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("Regional Power", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    for btn in buttons:
        pygame.draw.rect(screen, GRAY, btn["rect"])
        pygame.draw.rect(screen, BLACK, btn["rect"], 2)
        label = button_font.render(btn["label"], True, BLACK)
        screen.blit(label, (btn["rect"].x + 30, btn["rect"].y + 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if buttons[0]["rect"].collidepoint(pos):
                start_clicked = True
                start_time = time.time()
            elif buttons[2]["rect"].collidepoint(pos):
                pygame.quit()
                sys.exit()

    if start_clicked and time.time() - start_time > 2:
        subprocess.Popen([sys.executable, "main.py"])
        time.sleep(1)
        pygame.quit()
        sys.exit()
