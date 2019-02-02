import itertools


counter = itertools.count()


def _travel(ob):
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


class Screen:

    iditer = itertools.count()

    def __init__(self, h, w, y, x):
        self.name = next(Screen.iditer)
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.parscreen = None

    def subwin(self, *args):
        if len(args) == 2:
            y, x = args
            h, w = self.h, self.w
        elif len(args) == 4:
            h, w, y, x = args

        screen = Screen(h, w, y, x)
        screen.parscreen = self
        print("Subwin {}; h: {}, w: {}, y: {}, x: {}".format(screen.name, h, w, y, x))
        return screen

    def getparyx(self):
        return self.y - self.parscreen.y, self.x - self.parscreen.x

    def getmaxyx(self):
        return self.y + self.h, self.x + self.w

    def clear(self):
        print("Clear")

    def keypad(self, num):
        print("Keypad")

    def mvderwin(self, y, x):
        print("Move {} to y: {}, x: {}".format(self.name, y, x))

    def resize(self, h, w):
        print("Resize {} to h: {}, w: {}".format(self.name, h, w))
