import os
import re
import threading
import time
import colorama
from .exeptions import TooSmallScreen, NoSuchScreen

class _Screen:
    def __init__(self, child, centered):
        self.child = child
        self.centered = centered


    def center(self, line, width):
        def remove_styling(text):
            reaesc = re.compile(r'\x1b[^m]*m')
            return reaesc.sub('', text)

        real_length = len(remove_styling(line))
        left = (width - real_length) // 2
        right = width - real_length - left
        return ' ' * left + line + ' ' * right

    def _render(self):
        if self.child.width > os.get_terminal_size()[0] or self.child.height > os.get_terminal_size()[1]:
            raise TooSmallScreen
        content = [
            ''.join(row) + colorama.Style.RESET_ALL
            for row in self.child.build()
        ]
        if self.centered:
            content = list(map(lambda line: self.center(line, os.get_terminal_size()[0]), content))
        return content

    def __str__(self):
        return '\n'.join(self._render())


class ManualRefreshScreen(_Screen):
    def __init__(self, child, centered=True):
        super(ManualRefreshScreen, self).__init__(child, centered)

    def refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(self))
        return self


class ScreensManager:
    def __init__(self, **kwargs):
        for key, screen in kwargs.items():
            setattr(self, key, screen)

        self.displayed_screen = list(kwargs.items())[0][1]

    def display(self, screen_id):
        if screen_id in self.__dir__():
            self.displayed_screen = getattr(self, screen_id)
            self.refresh()
            return self
        else:
            raise NoSuchScreen


    def refresh(self):
        self.displayed_screen.refresh()
        return self
