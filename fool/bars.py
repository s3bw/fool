from fool._base import Base


class Bar(Base):

    def __init__(self, display_text, x, y):
        self.display_text = display_text
        self.x = x
        self.y = y

    def draw(self):
        self.screen.addstr(self.y, self.x, self.display_text)
