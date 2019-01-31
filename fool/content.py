"""Content objects can be used inside screens."""


class TextBlob:

    def __init__(self, text=None, path=None):
        """Textblob accepts str or file paths."""
        if text:
            self.text = text
        else:
            self.read_file(path)

    def read_file(self, path):
        with open(path, 'r') as f:
            self.text = f.read()

    def draw(self, y, x, width, screen):
        i = 0
        while i < len(self.text):
            y += 1
            screen.addstr(y, x + 1, self.text[i:i+width-1])
            i += (width - 1)
