"""Window class to split the console into parts."""
import curses

from fool._base import Base
from fool._debug import travel, counter
from fool._interactions import Scrollable

from fool.text import Alignments
from fool.registry import Registry
from fool.trees import in_order_traversal
from fool.trees import breadth_first_traversal

from fool.content import ListItem, ListItems


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE


class Window(Base):

    # Margins (would be instances of Window)
    left = None
    right = None

    def __init__(self, name=None, h=None, w=None):
        self.name = next(counter) if not name else name
        self.h = h
        self.max_w = w

    def attach_screen(self, screen):
        """Attach screens to window objects."""
        _, max_x = screen.getmaxyx()

        # Calculating the width of each window
        self.calculate_width(max_x)

        # Give each window an x co-ordinate
        in_order_traversal(self, 0, assign_x)

        # Build each screen for the windows
        self.build_screen(screen)

        # NOTE:(foxyblue): travel used for debugging
        travel(self)

    def build_screen(self, screen):
        max_y, _ = screen.getmaxyx()
        if self.width:
            self.screen = screen.subwin(max_y, self.width, 0, self.start_x)
            self.bottom_line = max_y - 1
            if self.left:
                self.left.build_screen(screen)
            if self.right:
                self.right.build_screen(screen)

    def calculate_width(self, max_x):
        self.width = 0
        add = breadth_first_traversal(self, max_x, assign_width)
        self.width += add

    def resize(self, dimensions):
        h, w, y, x = dimensions
        self.screen.mvderwin(y, x)
        # Resize h, w
        self.screen.resize(h, w)

    def update(self):
        super(Window, self).update()

    def draw(self):
        if self.width:
            self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
            if self.left:
                self.left.draw()
            if self.right:
                self.right.draw()


class TextWindow(Window):

    def draw(self):
        if self.width:
            for content in self.content:
                content.draw(0, self.start_x, self.width, self.screen)
        super(TextWindow, self).draw()

    def setup_content(self):
        """Text doesn't need to be setup."""
        pass


class TableWindow(Window, Scrollable, Alignments):

    def __init__(self, w, items, scroll=None):
        self.items = ListItems(items)
        super().__init__(w=w)
        self.line_colouring = _set_colour
        if scroll:
            up, down = scroll
            self.key_map = {
                up: self.move_up,
                down: self.move_down,
            }
            self.max_pos = len(self.items)
            self.line_colouring = _set_scroll_colour

    def setup_content(self):
        self.register_columns()

    def update(self):
        self.reduction = self.list_top
        self.cursor = self.position
        super().update()

    def register_columns(self):
        self.registry = Registry()
        for column in self.content:
            self.registry.register_object(column.name, column)

    def draw_line(self, item, line, line_colour):
        align = {'left': self.left_align,
                 'right': self.right_align,
                 'centre': self.centre_align}

        left_x = self.start_x + 2
        for column in self.registry.get_objects():
            cln_setting = self.registry.get_object(column)
            size = cln_setting.size
            if left_x + size + 2 < (self.start_x + self.width):
                pline = getattr(item, column)
                pline = display_text(pline)

                alignment = cln_setting.align
                pline = align[alignment](pline, size)
                self.screen.addstr(line, left_x, pline, line_colour)
                left_x += size + 2
                if left_x < self.max_x:
                    self.screen.addstr(line, left_x, '|', line_colour)
                    left_x += 2
            else:
                break

    def draw_item(self, item):
        """Draw an item."""
        if self.reduction > 0:
            self.reduction -= 1
        else:
            self.drawing_line += 1
            if self.drawing_line < self.bottom_line - 1:
                line = self.drawing_line
                line_colour = self.line_colouring(line, self.cursor)
                self.draw_line(item, line, line_colour)

    def draw(self):
        """Draw all viewable items."""
        self.drawing_line = 0
        for item in self.items.iter_viewable():
            self.draw_item(item)
        super(TableWindow, self).draw()


def _set_colour(line, cursor):
    return NORMAL_LINE_COLOUR


def _set_scroll_colour(line, cursor):
    if line == cursor:
        return REVERSE_LINE_COLOUR
    if line % 2 == 0:
        return DIM_LINE_COLOUR
    return NORMAL_LINE_COLOUR


def display_text(x):
    return str(x)


def assign_width(obj, remaining_width):
    """Assign width provides a window their width.

    All remaining width after each window has been assigned
    is added to the root window width.
    """
    if 0 < remaining_width:
        if obj.max_w <= remaining_width:
            obj.width = obj.max_w
        else:
            obj.width = remaining_width
        remaining_width -= obj.width
    else:
        obj.width = 0
    return remaining_width


def assign_x(obj, next_x):
    """Assign next x to the object's starting x, the next x
    will be the object's start_x + object's width.
    """
    obj.start_x = next_x
    return obj.width + next_x
