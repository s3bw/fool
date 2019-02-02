
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
