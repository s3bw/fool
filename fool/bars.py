from curses import A_NORMAL as NORMAL
from curses import A_REVERSE as REVERSE

from fool.console import ConsoleReturn


class BaseMixin:
    def update_screen(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_y = self.max_y - 1
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


class TextBar(BaseMixin):
    def __init__(self, display_text, x, y):
        self.display_text = display_text
        self.x = x
        self.y = y

    def draw(self):
        self.screen.addstr(self.y, self.x, self.display_text)


class ToggleBar(BaseMixin):
    def __init__(self, options, x, y, toggle):
        self.options = options
        self.active = 0
        self.x = x
        self.y = y
        self.key_map = {toggle: self.toggle}

    def toggle(self):
        self.active += 1
        if self.active == len(self.options):
            self.active = 0

    def draw(self):
        self.screen.addstr(self.y, self.x, self.options[self.active])


#: Left Separator Normal
LSN = ('', NORMAL)
#: Left Separator Reverse
LSR = ('', REVERSE)
#: Alternative Left Separator Normal
ALSN = ('', NORMAL)
#: Alternative Left Separator Reverse
ALSR = ('', REVERSE)


class TabBar(BaseMixin):
    """Draws a tabs bar on the screen."""

    def __init__(self, book, books, **kwargs):
        """
        :param book: (str) contains the name of the current tab.
        :param books: List[str] contains a list of all tabs.
        """
        self.control_keys = {
            'next': self.next_tab,
            'prev': self.prev_tab,
        }
        self.set_keys(kwargs)

        self.tabs = [book]
        # If 'book' appears in available 'books' construct the tabs
        # else we only need a single tab which will be used as a
        # heading.
        if book in books:
            self.tabs = ['general']
            books = set(books)
            # Ensures that 'general' always appears first.
            books.remove('general')
            self.tabs.extend(sorted(books))
            # Highlight the active tab.
            self.highlight_index = self.tabs.index(book)
        else:
            self.highlight_index = 0

        # I think this is the starting point of drawing the tabs
        self.start_x = 5
        #: Top line is the y axis of the tabs bar
        self.top_line = 0

    def set_keys(self, keys):
        """Set the keys to the values defined in the kwargs.

        A valid control for this objects comes from the keys
        defined in `self.control_keys`.
        """
        self.key_map = {}
        for key, value in keys.items():
            if key in self.control_keys:
                self.key_map[value] = self.control_keys[key]

    def next_tab(self):
        """Go to the next tab.

        This bumps the highlighted tab by one and returns
        the name of the highlighted tab. If it extends
        beyond the index of available tabs set tab to 0.
        """
        self.highlight_index += 1
        if self.highlight_index == len(self.tabs):
            self.highlight_index = 0
        return ConsoleReturn(
            action='next', key=self.tabs[self.highlight_index])

    def prev_tab(self):
        """Go to previous tab. Like `next_tab` but reversed."""
        self.highlight_index -= 1
        if self.highlight_index < 0:
            self.highlight_index = len(self.tabs) - 1
        return ConsoleReturn(
            action='prev', key=self.tabs[self.highlight_index])

    def _draw_separator(self, x, separator):
        character, colour = separator
        self.screen.addstr(self.top_line, x, character, colour)

    def draw_first_separator(self):
        if self.highlight_index == 0:
            self._draw_separator(self.start_x, LSR)
        else:
            self._draw_separator(self.start_x, ALSN)

    def draw_last_separator(self, x_pos):
        if len(self.tabs) == self.highlight_index + 1:
            self._draw_separator(x_pos, LSN)
        else:
            self._draw_separator(x_pos, ALSN)

    def draw_separator(self, index, x_pos):
        if index == 0:
            self.draw_first_separator()
        elif index - 1 == self.highlight_index:
            self._draw_separator(x_pos, LSN)
        elif index == self.highlight_index:
            self._draw_separator(x_pos, LSR)
        else:
            self._draw_separator(x_pos, ALSN)

    def draw(self):
        draw_x = self.start_x
        for index, tab_name in enumerate(self.tabs):
            self.draw_separator(index, draw_x)
            write = ' {} '.format(tab_name)
            line_colour = NORMAL
            if index == self.highlight_index:
                line_colour = REVERSE
            self.screen.addstr(self.top_line, draw_x + 1, write, line_colour)
            draw_x += len(write) + 1
        self.draw_last_separator(draw_x)
