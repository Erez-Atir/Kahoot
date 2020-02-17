import pygame
import time


class InputBox:
    """
    Creates an input box which you can use to get the username for the first screen.
    :param screen: the surface you want to draw on
    :param size: (x, y) -> where x is the length of the box and y is the height
    :param place: (x, y) -> where x is the x-coordinate of the box and y is the y-coordinate, in relation to 'screen'
    :param color: (R, G, B) of the background color of the box
    :param border_width: the width of the border, 0 for no border
    :param border_color: (R, G, B) of the border color
    :param text_color: (R, G, B) of the text color
    :param font: the name of the font for the text
    """
    def __init__(self, screen, size, place, color=(255, 255, 255), border_width=0, border_color=(0, 0, 0), text_color=(0, 0, 0), font="Arial"):
        self.__start = time.time()
        self.__input_text = ""
        self.__keys = {letter: time.time() for letter in [chr(let) for let in range(97, 123) + range(48, 58) + [8, 32, 127]] + ["<-", "->"]}
        self.__toggle = False
        self.__toggle__spot = -1
        self.__last_size = None
        self._screen = screen
        self.size = size
        self.place = place
        self.color = color
        self.border_width = border_width
        self.border_color = border_color
        self.text_color = text_color
        self.font = font

    def draw(self):
        """
        Call this inside the loop in order to draw the textbox to the screen
        """
        if self.color:
            pygame.draw.rect(self._screen, self.color, (self.place, self.size))
        if self.border_width:
            pygame.draw.rect(self._screen, self.border_color, (tuple([x-self.border_width/2 for x in self.place]), tuple([x+self.border_width for x in self.size])), self.border_width)

        last = self.__toggle
        if pygame.mouse.get_pressed()[0]:
            self.__toggle = True if all(p <= x <= p+s for x, s, p in zip(pygame.mouse.get_pos(), self.size, self.place)) else False

        self.__toggle__spot = -1 if last != self.__toggle else self.__toggle__spot

        text_to_print = self.__input_text
        backspaced = False
        if self.__toggle:
            pressed = pygame.key.get_pressed()
            shift = 97-65 if any(pressed[303:305]) else 0
            for key in range(97, 123) + range(48, 58) + [8, 32, 127, 275, 276, 278, 279]:
                if pressed[key]:
                    if key in [275, 276]:
                        key = "<-" if key == 276 else "->"
                        if time.time() - self.__keys[key] >= 0.2:
                            self.__keys[key] = time.time()
                            if key == "<-":
                                self.__toggle__spot = self.__toggle__spot - 1 if self.__toggle__spot*-1 <= len(self.__input_text) else self.__toggle__spot
                            else:
                                self.__toggle__spot = self.__toggle__spot + 1 if self.__toggle__spot < -1 else self.__toggle__spot
                        backspaced = True
                    elif key in [278, 279]:
                        key = "<-" if key == 278 else "->"
                        self.__toggle__spot = -1 if key == "->" else len(self.__input_text)*-1-1
                        backspaced = True
                    elif time.time() - self.__keys[chr(key)] >= 0.4 and key not in [8, 127, 275, 276]:
                        self.__keys[chr(key)] = time.time()
                        if 97 <= key <= 122:
                            if self.__toggle__spot == -1:
                                self.__input_text += chr(key-shift)
                            else:
                                self.__input_text = self.__input_text[:self.__toggle__spot+1] + chr(key-shift) + self.__input_text[self.__toggle__spot+1:]
                        else:
                            if self.__toggle__spot == -1:
                                self.__input_text += chr(key)
                            else:
                                self.__input_text = self.__input_text[:self.__toggle__spot+1] + chr(key) + self.__input_text[self.__toggle__spot+1:]
                    elif key == 8:
                        if time.time() - self.__keys[chr(key)] >= 0.15:
                            self.__keys[chr(key)] = time.time()

                            if self.__toggle__spot == -1:
                                self.__input_text = self.__input_text[:-1]
                            else:
                                self.__input_text = self.__input_text[:self.__toggle__spot] + self.__input_text[self.__toggle__spot+1:]

                            self.__last_size += 100
                        backspaced = True
                    elif key == 127:
                        if time.time() - self.__keys[chr(key)] >= 0.15:
                            self.__keys[chr(key)] = time.time()
                            if self.__toggle__spot == -2:
                                self.__input_text = self.__input_text[:self.__toggle__spot+1]
                                self.__toggle__spot += 1
                            elif self.__toggle__spot != -1:
                                self.__input_text = self.__input_text[:self.__toggle__spot+1] + self.__input_text[self.__toggle__spot+2:]
                                self.__toggle__spot += 1

                            self.__last_size += 100
                        backspaced = True
                else:
                    if key in [278, 279]:
                        pass
                    elif key in [275, 276]:
                        key = "<-" if key == 276 else "->"
                        self.__keys[key] = 0
                    else:
                        self.__keys[chr(key)] = 0
        font_size = self.__last_size if self.__last_size else self.size[1]
        text_font = pygame.font.Font(self.font, font_size)
        while any(x >= y*0.95 for x, y in zip(text_font.size(self.__input_text + '|'), self.size)):
            font_size -= 1
            text_font = pygame.font.Font(self.font, font_size)

        if self.__toggle and int((time.time() - self.__start)*2) % 2 == 0 or backspaced:
            textW, textH = text_font.size(self.__input_text)
            W, H = text_font.size(self.__input_text[self.__toggle__spot+1:])
            W = 0 if self.__toggle__spot == -1 else W
            pygame.draw.line(self._screen, self.text_color, (self.place[0] + self.size[0]/2 + textW/2 - W, self.place[1] + self.size[1]/2 - textH/2),
                                                            (self.place[0] + self.size[0]/2 + textW/2 - W, self.place[1] + self.size[1]/2 + textH/2), font_size/10)



        self.__last_size = font_size
        printext = text_font.render(text_to_print, False, self.text_color)
        textW, textH = text_font.size(self.__input_text)
        self._screen.blit(printext, (self.place[0] + self.size[0]/2 - textW/2, self.place[1] + self.size[1]/2 - textH/2))

    def get_input(self):
        """
        Call this after the loop is done and the user has submitted his input in order to get it
        :return The user's input
        """
        return self.__input_text


class OutputBox:
    """
    Creates an input box which you can use to get the username for the first screen.
    :param screen: the surface you want to draw on
    :param text: the text you want to print
    :param size: (x, y) -> where x is the length of the box and y is the height
    :param place: (x, y) -> where x is the x-coordinate of the box and y is the y-coordinate, in relation to 'screen'
    :param color: (R, G, B) of the background color of the box
    :param border_width: the width of the border, 0 for no border
    :param border_color: (R, G, B) of the border color
    :param text_color: (R, G, B) of the text color
    :param font: the name of the font for the text
    """
    def __init__(self, screen, text, size, place, color=(255, 255, 255), border_width=0, border_color=(0, 0, 0), text_color=(0, 0, 0), font=None):
        self.__font_size = size[1]
        self._screen = screen
        self.text = text
        self.size = size
        self.place = place
        self.color = color
        self.border_width = border_width
        self.border_color = border_color
        self.text_color = text_color
        self.font = font

    def draw(self):
        """
        Call this inside the loop in order to draw the textbox to the screen
        """
        if self.color:
            pygame.draw.rect(self._screen, self.color, (self.place, self.size))
        if self.border_width:
            pygame.draw.rect(self._screen, self.border_color, (tuple([x-self.border_width/2 for x in self.place]), tuple([x+self.border_width for x in self.size])), self.border_width)
        font_size = self.__font_size
        text_font = pygame.font.Font(self.font, font_size)
        while max([text_font.size(self.text.split("\n")[x])[0] for x in range(len(self.text.split("\n")))]) >= self.size[0] or (text_font.size(self.text)[1])*len(self.text.split("\n")) >= self.size[1]:
            font_size -= 1
            text_font = pygame.font.Font(self.font, font_size)
            self.__font_size = font_size
        linumber = 0
        for line in self.text.split("\n"):
            printext = text_font.render(line, False, self.text_color)
            textW, textH = text_font.size(self.text.split("\n")[linumber])
            self._screen.blit(printext, (self.place[0] + self.size[0]/2 - textW/2, self.place[1] + self.size[1]/2 - (textH/2)*len(self.text.split("\n")) + textH*linumber))
            linumber += 1


class ButtonBox:
    """
    Creates an input box which you can use to get the username for the first screen.
    :param screen: the surface you want to draw on
    :param text: the text you want to print
    :param size: (x, y) -> where x is the length of the box and y is the height
    :param place: (x, y) -> where x is the x-coordinate of the box and y is the y-coordinate, in relation to 'screen'
    :param color: (R, G, B) of the background color of the box
    :param border_width: the width of the border, 0 for no border
    :param border_color: (R, G, B) of the border color
    :param text_color: (R, G, B) of the text color
    :param font: the name of the font for the text
    """
    def __init__(self, screen, text, size, place, color=(255, 255, 255), border_width=3, border_color=(0, 0, 0), text_color=(0, 0, 0), font=None):
        self.__font_size = size[1]
        self._screen = screen
        self.text = text
        self.size = size
        self.place = place
        self.color = color
        self.border_width = border_width
        self.border_color = border_color
        self.text_color = text_color
        self.font = font
        self.clicked = False

    def draw(self):
        """
        Call this inside the loop in order to draw the textbox to the screen
        """
        if self.color:
            pygame.draw.rect(self._screen, self.color, (self.place, self.size))
        x, y = pygame.mouse.get_pos()
        if self.place[0] < x and x < self.place[0] + self.size[0] and y > self.place[1] and y < self.place[1] + self.size[1]:
            pygame.draw.rect(self._screen, self.border_color, (tuple([x-self.border_width/2 for x in self.place]), tuple([x+self.border_width for x in self.size])), self.border_width)
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        font_size = self.__font_size
        text_font = pygame.font.Font(self.font, font_size)
        while max([text_font.size(self.text.split("\n")[x])[0] for x in range(len(self.text.split("\n")))]) >= self.size[0] or (text_font.size(self.text)[1])*len(self.text.split("\n")) >= self.size[1]:
            font_size -= 1
            text_font = pygame.font.Font(self.font, font_size)
            self.__font_size = font_size
        linumber = 0
        for line in self.text.split("\n"):
            printext = text_font.render(line, False, self.text_color)
            textW, textH = text_font.size(self.text.split("\n")[linumber])
            self._screen.blit(printext, (self.place[0] + self.size[0]/2 - textW/2, self.place[1] + self.size[1]/2 - (textH/2)*len(self.text.split("\n")) + textH*linumber))
            linumber += 1


    def was_clicked(self):
        temp = self.clicked
        self.clicked = False
        return temp