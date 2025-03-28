import pygame

class Character:
    def __init__(self, name, role, position, color=(100, 100, 100)):
        self.name = name
        self.role = role
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], 100, 100)

        self.capital = "3 200 000 грн"
        self.assets = "4 компанії"
        self.income = "+15 000 грн/міс"
        self.trust = "50"
        self.supports = "Правих"
        self.reputation = "72%"
        self.influence = "456"
        self.legal_issues = "Так"
        self.log = []
        self.selected = False

    def draw(self, surface, font_name, font_role):
        pygame.draw.rect(surface, pygame.Color("white"), self.rect)
        pygame.draw.rect(surface, pygame.Color("black"), self.rect, 2)
        pygame.draw.circle(surface, self.color, self.rect.center, 30)

        name_text = font_name.render(self.name, True, pygame.Color("black"))
        role_text = font_role.render(self.role, True, pygame.Color("gray"))

        name_x = self.rect.centerx - name_text.get_width() // 2
        role_x = self.rect.centerx - role_text.get_width() // 2

        surface.blit(name_text, (name_x, self.rect.bottom - 35))
        surface.blit(role_text, (role_x, self.rect.bottom - 15))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
