#-----------------------Imports-----------------------
import pygame
import textbox

#-------------------------Main-------------------------
def main():
    """
    Add Documentation here
    """
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("textbox")
    pygame.font.init()

    finish = False
    Textbox = textbox.InputBox(screen, size=(700, 200), place=(50, 50), color=(255, 255, 255), border_width=10, border_color=(0, 0, 0))
    Inputbox = textbox.InputBox(screen, size=(700, 200), place=(50, 310), color=(255, 255, 255), border_width=10, border_color=(0, 0, 0))
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        screen.fill((30, 144, 255))
        Textbox.draw()
        Inputbox.draw()
        pygame.display.flip()

    print Inputbox.get_input()
    pygame.quit()

if __name__ == '__main__':
    main()