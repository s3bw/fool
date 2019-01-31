
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
