from enum import Enum

import colorama

colorama.init(autoreset=True)


class Colors:
    class FontColors(Enum):
        Black = colorama.Fore.BLACK
        Red = colorama.Fore.RED
        Green = colorama.Fore.GREEN
        Yellow = colorama.Fore.YELLOW
        Blue = colorama.Fore.BLUE
        Magenta = colorama.Fore.MAGENTA
        Cyan = colorama.Fore.CYAN
        White = colorama.Fore.WHITE

    class BackgroundColors(Enum):
        Black = colorama.Back.BLACK
        Red = colorama.Back.RED
        Green = colorama.Back.GREEN
        Yellow = colorama.Back.YELLOW
        Blue = colorama.Back.BLUE
        Magenta = colorama.Back.MAGENTA
        Cyan = colorama.Back.CYAN
        White = colorama.Back.WHITE

    class FontBrightness(Enum):
        Dim = colorama.Style.DIM
        Normal = colorama.Style.NORMAL
        Bright = colorama.Style.BRIGHT


class StyleData:
    def __init__(self,
                 font_color='DEFAULT',
                 background_color='DEFAULT',
                 font_brightness='DEFAULT'):
        self.font_color = ('' if type(font_color) == str else font_color.value)
        self.background_color = ('' if type(background_color) == str else background_color.value)
        self.font_brightness = ('' if type(font_brightness) == str else font_brightness.value)

    def get_data(self):
        return self.font_color + self.background_color + self.font_brightness
