import itertools

from fool._base import Base


counter = itertools.count()


def travel(ob):
    """Used for debugging.
    Prints the dimensions of mocked screen objects.
    """
    queue = [ob]
    while queue:
        ob = queue.pop(0)
        print(next(counter), ob.win_w, ob.name, ob.start_x)
        if ob.left:
            queue.append(ob.left)
        if ob.right:
            queue.append(ob.right)


def width_visit(obj, max_value):
    if 0 < max_value:
        if obj.w <= max_value:
            obj.win_w = obj.w
        else:
            obj.win_w = max_value
        max_value -= obj.win_w
    return max_value


def margin_width(obj, max_value):
    """BF application of width to left and right nodes."""
    queue = [obj]
    while queue:
        obj = queue.pop(0)
        max_value = width_visit(obj, max_value)
        if obj.left:
            queue.append(obj.left)
        if obj.right:
            queue.append(obj.right)
    return max_value


def x_visit(obj, previous_x):
    obj.start_x = previous_x
    return obj.win_w + previous_x


def margin_x(obj, previous_x):
    """Provide x for screens."""
    if obj:
        previous_x = margin_x(obj.left, previous_x)
        previous_x = x_visit(obj, previous_x)
        previous_x = margin_x(obj.right, previous_x)
    return previous_x


class Window(Base):

    # Margins (would be instances of Window)
    left = None
    right = None

    def __init__(self, name=None, h=None, w=None):
        self.name = next(name) if name else name
        self.h = h
        self.w = w

    def attach_screen(self, screen):
        """Attach screens to window objects."""
        _, max_x = screen.getmaxyx()

        # Calculating the width of each window
        self.calculate_width(max_x)

        # Assigning the starting x for each window
        # Assert margin_x return should == max_x
        # SUM(w) == Console_w
        assert margin_x(self, 0) == max_x

        # Build each screen for the windows
        self.build_screen(screen)

        # NOTE:(foxyblue): travel used for debugging
        travel(self)

    def build_screen(self, screen):
        max_y, _ = screen.getmaxyx()
        self.screen = screen.subwin(max_y, self.win_w, 0, self.start_x)
        if self.left:
            self.left.build_screen(screen)
        if self.right:
            self.right.build_screen(screen)

    def calculate_width(self, max_x):
        self.win_w = 0
        add = margin_width(self, max_x)
        self.win_w += add

    def resize(self, dimensions):
        h, w, y, x = dimensions
        self.screen.mvderwin(y, x)
        # Resize h, w
        self.screen.resize(h, w)

    def update(self):
        super(Window, self).update()

    def draw(self):
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
        if self.left:
            self.left.draw()
        if self.right:
            self.right.draw()
