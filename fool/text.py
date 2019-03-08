class Alignments:
    def left_align(self, text, size):
        """Left align the column contents."""
        text_size = len(text)
        if text_size > size:
            text = text[:size]
            text_size = len(text)
        text = text + (' ' * (size - text_size + 1))
        return text

    def centre_align(self, text, size):
        """Centre align the column contents."""
        text_size = len(text)
        buffer_size = (size) - (text_size) + 1
        column_buffer = (int(buffer_size / 2)) * ' '

        return column_buffer + text + column_buffer

    def right_align(self, text, size):
        """Left align the column contents."""
        text_size = len(text)
        if text_size > size:
            text = text[:size]
            text_size = len(text)
        text = (' ' * (size - text_size + 1)) + text
        return text


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
        # This is text wrapping logic
        # it should move to fool/text.py
        i = 0
        while i < len(self.text):
            y += 1
            screen.addstr(y, x + 1, self.text[i:i + width - 1])
            i += (width - 1)
