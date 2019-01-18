from fool._base import Base


class Input(Base):
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
