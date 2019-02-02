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


class Input(BaseMixin):
    def __init__(self, **kwargs):
        self.key_map = {}
        for key, value in kwargs.items():
            self.key_map[value] = self.get_string(key)

    def get_string(self, text):
        def _return():
            return text
        return _return

    def draw(self):
        pass
