from fool._base import Base


class TextBar(Base):

    def __init__(self, display_text, x, y):
        self.display_text = display_text
        self.x = x
        self.y = y

    def draw(self):
        self.screen.addstr(self.y, self.x, self.display_text)


class ToggleBar(Base):

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
