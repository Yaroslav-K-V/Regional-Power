import pygame

GREEN = (100, 255, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (50, 200, 50)

class CompanyButton:
    def __init__(self, company, x, y, font):
        self.company = company
        self.rect = pygame.Rect(x, y, 150, 35)
        self.font = font
        self.hovered = False

    def draw(self, surface):
        color = HOVER_COLOR if self.hovered else GREEN
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        label = self.font.render("Купити", True, WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
