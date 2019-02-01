import curses
from curses import panel

from fool._base import Base
from fool._listener import KeyListener


def display(view, model, **kwargs):
    return curses.wrapper(setup_console, view, model, **kwargs)


def setup_console(stdscreen, view, model, **kwargs):
    curses.curs_set(0)
    with Console(stdscreen, view, model, **kwargs) as console:
        action = console.show()
    return action


class Console(Base):

    def close(self):
        return 'exit'

    def __init__(self, stdscreen, view, model, **kwargs):
        self.screen = stdscreen.subwin(0, 0)
        self.panel = panel.new_panel(self.screen)

        self.render_ui = view(self.screen, model)
        self.key_map = {
            value: getattr(self, key)
            for key, value in kwargs.items()
        }

        self.listener = KeyListener()
        self.collect_keys()
        self.attach_screens()

    def __enter__(self):
        panel.update_panels()
        self.panel.hide()
        self.panel.top()
        self.panel.show()

        self.screen.keypad(1)
        self.screen.clear()
        return self

    def __exit__(self, _type, value, traceback):
        self.screen.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def attach_screens(self):
        for ui in self.render_ui:
            # If a ui object has content, sometimes we are
            # required to prepare this content for rendering.
            if hasattr(ui, 'content'):
                ui.setup_content()
            ui.attach_screen(self.screen)
        self.listener.attach_screen(self.screen)

    def collect_keys(self):
        self.visit(self.listener)
        for ui in self.render_ui:
            ui.visit(self.listener)

    def render(self):
        self.screen.clear()
        for ui in self.render_ui:
            ui.update()
            ui.draw()

    def show(self):
        action = False
        while not action:
            self.render()
            action = self.listener.key_press()

        return action
