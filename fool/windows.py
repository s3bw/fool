"""Window class to split the console into parts."""
import itertools

from fool._base import Base


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


def breadth_first_traversal(obj, value, visit_func):
    """breadth first traversal of windows."""
    queue = [obj]
    while queue:
        obj = queue.pop(0)
        value = visit_func(obj, value)
        if obj.left:
            queue.append(obj.left)
        if obj.right:
            queue.append(obj.right)
    return value


def assign_x(obj, next_x):
    """Assign next x to the object's starting x, the next x
    will be the object's start_x + object's width.
    """
    obj.start_x = next_x
    return obj.width + next_x


def in_order_traversal(obj, value, visit_func):
    """In order traversal of windows."""
    if obj:
        value = in_order_traversal(obj.left, value, visit_func)
        value = visit_func(obj, value)
        value = in_order_traversal(obj.right, value, visit_func)
    return value


counter = itertools.count()


def travel(ob):
    """Used for debugging.
    Prints the dimensions of mocked screen objects.
    """
    queue = [ob]
    while queue:
        ob = queue.pop(0)
        print(next(counter), ob.width, ob.name, ob.start_x)
        if ob.left:
            queue.append(ob.left)
        if ob.right:
            queue.append(ob.right)
