import pygame

def load_images():
    bg_image = pygame.image.load("resources/img/bg_company_manage_window.jpg")
    residential_bg = pygame.image.load("resources/img/bg_real_estate__residential_manage_window.jpg").convert_alpha()
    commercial_bg = pygame.image.load("resources/img/bg_real_estate__comercy_manage_window.jpg").convert_alpha()
    land_bg = pygame.image.load("resources/img/bg_real_estate__land_plot_manage_window.jpg").convert_alpha()
    player_profile_bg = pygame.image.load("resources/img/player_profile_bg.jpg").convert_alpha()

    return {
        "company_bg": bg_image,
        "residential_bg":residential_bg,
        "commercial_bg":commercial_bg,
        "land_bg":land_bg,
        "profile_bg": player_profile_bg,

    }
