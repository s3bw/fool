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


class Column:

    def __init__(self, name, size, align='left'):
        self.name = name
        self.size = size
        self.align = align


class BooleanColumn(Column):
    pass


class ListItem:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


class ListItems:

    def __init__(self, items):
        self.menu = [
            ListItem(**attrs)
            for attrs in items
        ]

    def __len__(self):
        return len(self.menu)

    def iter_viewable(self):
        for item in self.menu:
            yield item
            if hasattr(item, 'expand') and item.expand:
                for subitem in item.subitems:
                    yield subitem
