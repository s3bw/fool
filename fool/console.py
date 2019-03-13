"""
Call resolution:

Window:

    .__init__()
    .visit(listener)
    .attach_screen(screen)
    .setup_content()
    .update()
    .draw()
"""
import curses
from curses import panel

from fool._listener import KeyListener


def display(view, model, **kwargs):
    return curses.wrapper(setup_console, view, model, **kwargs)


def setup_console(stdscreen, view, model, **kwargs):
    curses.curs_set(0)
    with Console(stdscreen, view, model, **kwargs) as console:
        action = console.show()
    return action


class BaseMixin:
    def update_screen(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        #: bottom_y is the max y we can draw on
        self.bottom_y = self.max_y - 1
        #: right_x is the max x we can draw on
        self.right_x = self.max_x - 1
        self.centre_x = int(self.max_x / 2)

    def attach_screen(self, screen):
        self.screen = screen
        self.update_screen()

    def update(self):
        self.update_screen()

    @property
    def has_keys(self):
        return (hasattr(self, 'key_map') and self.key_map)

    def visit(self, listener):
        if self.has_keys:
            listener.keys.update(self.key_map)


class ConsoleReturn:
    """ConsoleReturn standardises the data structure returned by
    the console.
    """

    def __init__(self, action, value=None, key=None):
        #: action describes the action returned
        self.action = action
        #: value carries an integer related to the action
        #: (optional) Not all actions will have an integer
        self.value = value
        #: key carries a string related to the action
        #: (optional) Not all actions will have a string
        self.key = key

    def __str__(self):
        """String representation of console return."""
        return str({
            'action': self.action,
            'value': self.value,
            'key': self.key
        })


class Console(BaseMixin):
    def close(self):
        """Close will exit the current display."""
        return ConsoleReturn(action='close')

    def __init__(self, stdscreen, view, model, **kwargs):
        self.screen = stdscreen.subwin(0, 0)
        self.panel = panel.new_panel(self.screen)

        self.render_ui = view(model)
        self.key_map = {
            value: getattr(self, key)
            for key, value in kwargs.items()
        }

        self.listener = KeyListener()
        self.collect_keys()
        self.prepare_ui()

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

    def prepare_ui(self):
        for ui in self.render_ui:
            if hasattr(ui, 'content'):
                ui.setup_content()
            ui.attach_screen(self.screen)
        self.listener.attach_screen(self.screen)

    def collect_keys(self):
        """Collect key will find keys mapped to an action,
        these are then stored in the listener which responds
        to key presses.
        """
        self.visit(self.listener)
        for ui in self.render_ui:
            ui.visit(self.listener)

    def render(self):
        self.screen.clear()
        for ui in self.render_ui:
            ui.update()
            ui.draw()

    def show(self):
        """While an action has not been taken `action` will be False.
        If an action is taken `action` will be a ConsoleReturn object
        as a result the console closes and the action returns.
        """
        action = False
        while not action:
            self.render()
            action = self.listener.key_press()

        return action
