import os
import threading
import time


class _Screen:
    class ToSmallTerminal(Exception):
        pass

    def __init__(self, child, centered):
        self.child = child
        self.centered = centered
        self.content = []

    def _render(self):
        if self.child.width > os.get_terminal_size()[0] or self.child.height > os.get_terminal_size()[1]:
            # raise self.ToSmallTerminal()
            pass
        self.content = [(line.center(os.get_terminal_size()[0]) if self.centered else line) for line in
                        self.child.build()]
        return self.content

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
            os.system('cls')
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
        os.system('cls')
        print(str(self))
        return self


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
        else:
            self.displayed_screen.refresh()
        return self

    def refresh(self):
        if isinstance(self.displayed_screen, ManualRefreshScreen):
            self.displayed_screen.refresh()
        return self
