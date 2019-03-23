"""
The Window class acts as content containers for the fool
display. An initial root window is defined and left and
right margins can be instantiated to extend the
functionality of that single window as shown below:

main = Window(w=10)
main.left = Window(w=10)
main.right = Window(w=10)
main.right.left = Window(w=10)
main.right.right = Window(w=10)
main.left.left = Window(w=10)

Determination of width:
Width is determined using a breadth first traversal
of the windows starting at the root. The width remaining
is given to the root window. This allows the root to
remain the dominant window on the screen and allows the
margins to be used just as extensions.
(Utilising additional screen space if it is available).

     (0)
    /   \
  (1)   (2)
  /     / \
(3)   (4) (5)

Determination of left-most x co-ordinate:
The x co-ordinate of the windows need then to be
determined from left to right. For which an in-order
traversal is required.

     (2)
    /   \
  (1)   (4)
  /     / \
(0)   (3) (5)

| 0 | 1 | 2 | 3 | 4 | 5 |
          ^
         root
"""
import curses

from fool._debug import _travel, counter
from fool._interactions import Scrollable

from fool.text import Alignments
from fool.trees import in_order_traversal
from fool.trees import breadth_first_traversal

from fool.tables import TableItems

NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE


class BaseMixin:
    def update_screen(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_y = self.max_y - 1
        self.right_x = self.max_x - 1
        self.centre_x = int(self.max_x / 2)

    def update(self):
        self.update_screen()

    @property
    def has_keys(self):
        return (hasattr(self, 'key_map') and self.key_map)

    def visit(self, listener):
        if self.has_keys:
            listener.keys.update(self.key_map)
        if self.left:
            self.left.visit(listener)
        if self.right:
            self.right.visit(listener)


class Window(BaseMixin):

    # Margins (would be instances of Window)
    left = None
    right = None

    def __init__(self, name=None, h=None, w=None):
        super().__init__()
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
        self.update_screen()

        # NOTE:(foxyblue): travel used for debugging
        _travel(self)

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
    def __init__(self, registry, items, w, **kwargs):
        #: control_keys are the available key presses for the table window
        self.items = TableItems(items)
        self.registry = registry
        # self.line_colouring = _set_colour
        #: Always set line colouring as alternating
        self.line_colouring = _set_scroll_colour
        super().__init__(w=w)
        self.set_keys(kwargs)
        self.max_pos = len(self.items)

    def set_keys(self, keys):
        """Set the keys to the values defined in the kwargs.

        A valid control for this objects comes from the keys
        defined in `self.control_keys`.
        """
        self.key_map = {}
        for key, value in keys.items():
            if key in self.control_keys:
                self.key_map[value] = self.control_keys[key]

    def update(self):
        self.max_pos = len(self.items)
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_line = self.max_y - 1
        self.centre_x = int(self.max_x / 2)
        super().update()

    def draw_line(self, item, line, line_colour):
        align = {
            'left': self.left_align,
            'right': self.right_align,
            'centre': self.centre_align
        }

        left_x = self.start_x + 2
        for column in self.registry.getColumns():
            cln_setting = self.registry.getColumn(column)
            size = cln_setting.size
            # Draw columns until we run out of 'x' space
            if left_x + size + 2 < (self.start_x + self.width):
                pline = getattr(item, column)
                if not pline:
                    pline = cln_setting.default()
                else:
                    fmt = cln_setting.fmt
                    pline = fmt.format(pline)

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
        """Draw an item.

        `top_reduction` handles lists with more items than height.
        """
        if self.top_reduction > 0:
            self.top_reduction -= 1
        else:
            self.drawing_line += 1
            if self.drawing_line < self.bottom_line - 1:
                line = self.drawing_line
                line_colour = self.line_colouring(line, self.cursor_position)
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
