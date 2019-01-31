"""Window class to split the console into parts."""
from fool._base import Base
from fool._debug import travel, counter

from fool.text import Alignments
from fool.registry import Registry
from fool.trees import in_order_traversal
from fool.trees import breadth_first_traversal

from fool.content import ListItem, ListItems


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



class TableWindow(Window, Alignments):

    def __init__(self, w, items):
        self.items = ListItems(items)
        print([item.more for item in self.items.iter_viewable()])
        super().__init__(w=w)

    def setup_content(self):
        self.register_columns()

    def register_columns(self):
        self.registry = Registry()
        for column in self.content:
            self.registry.register_object(column.name, column)

    def draw_line(self, item, line):
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
                self.screen.addstr(line, left_x, pline)
                left_x += size + 2
                if left_x < self.max_x:
                    self.screen.addstr(line, left_x, '|')
                    left_x += 2
            else:
                break

    def draw_item(self, item):
        """Draw an item."""
        self.drawing_line += 1
        line = self.drawing_line
        self.draw_line(item, line)

    def draw(self):
        """Draw all viewable items."""
        self.drawing_line = 0
        for item in self.items.iter_viewable():
            self.draw_item(item)
        super(TableWindow, self).draw()


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
