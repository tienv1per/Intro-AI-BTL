import pygame
import sys
from button import Button

pygame.init()
WIDTH = 1280
HEIGHT = 720

algo_option = ['Greedy', 'Minimax', 'Negamax', 'Negascout']
chosen_algo = 'Greedy'

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

new_cursor = pygame.image.load("assets/mouse.png")
new_cursor = pygame.transform.scale(new_cursor, size=(50, 50))
pygame.mouse.set_visible(False)

BG = pygame.image.load("assets/background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/SamuraiBlast.woff", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        PLAY_TEXT = get_font(45).render(
            "This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        SCREEN.blit(new_cursor, PLAY_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        global chosen_algo
        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(45).render(
            "Choose algorithm", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        index = 0
        option_algo_btns = []
        for algo in algo_option:
            option_algo = Button(image=None, pos=(640, 200 + index), text_input=algo,
                                 font=get_font(30), base_color="Black", hovering_color="Green")
            index += 80
            if algo == chosen_algo:
                option_algo.set_base_color("Red")
            option_algo.changeColor(OPTIONS_MOUSE_POS)
            option_algo.update(SCREEN)
            option_algo_btns.append(option_algo)

        OPTIONS_BACK = Button(image=None, pos=(640, 560),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        SCREEN.blit(new_cursor, OPTIONS_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                for btn in option_algo_btns:
                    if btn.checkForInput(OPTIONS_MOUSE_POS):
                        chosen_algo = btn.get_text_input()

        pygame.display.update()


def main_menu():
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        SCREEN.blit(new_cursor, MENU_MOUSE_POS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
