import os
import re
import threading
import time

import colorama

from .exeptions import TooSmallScreen


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


class AutoRefreshingScreen(_Screen):
    def __init__(self, child, centered=True, refresh_time=0.1):
        super(AutoRefreshingScreen, self).__init__(child, centered)
        self.refresh_rate = refresh_time
        self.running = False
        self.child.build()

    def _refresh(self):
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(str(self))
            time.sleep(self.refresh_rate)

    def start(self):
        self.running = True
        _ = threading.Thread(target=self._refresh).start()
        return self

    def stop(self):
        self.running = False
        return self


class ManualRefreshScreen(_Screen):
    def __init__(self, child, centered=True):
        super(ManualRefreshScreen, self).__init__(child, centered)

    def refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(self))
        return self


class InputScreen(ManualRefreshScreen):
    def __init__(self, child, centered=True):
        super(InputScreen, self).__init__(child, centered)

    def get_input(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return input(str(self))


class ScreensManager:
    def __init__(self, **kwargs):
        for key, screen in kwargs.items():
            setattr(self, key, screen)

        self.displayed_screen = list(kwargs.items())[0][1]

    def display(self, screen_id):
        if isinstance(self.displayed_screen, AutoRefreshingScreen):
            self.displayed_screen.stop()
        self.displayed_screen = getattr(self, screen_id)
        if isinstance(self.displayed_screen, AutoRefreshingScreen):
            self.displayed_screen.start()
        elif isinstance(self.displayed_screen, ManualRefreshScreen):
            self.displayed_screen.refresh()
        else:
            return self.displayed_screen.get_input()

    def refresh(self):
        if isinstance(self.displayed_screen, ManualRefreshScreen):
            self.displayed_screen.refresh()
        return self
