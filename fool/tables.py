"""table.py contains the objects used in rendering a table."""

from collections import OrderedDict


class Registry:
    """Registry is used as a key value storage object."""

    def __init__(self):
        self._objects = OrderedDict()

    def get(self, name):
        """Get single item from the registry."""
        return self._objects[name]

    def iterGet(self):
        """Yield all objects."""
        for obj in self._objects:
            yield obj

    def set(self, name, obj):
        """Register an object."""
        self._objects[name] = obj

    def unset(self, name):
        """Unregister an object."""
        del self._objects[name]


class ColumnRegistry:
    def __init__(self):
        self.registry = Registry()

    def setColumn(self, title, *, size, align):
        column = Column(title, size, align)
        self.registry.set(title, column)

    def setBoolean(self, title, *, size, align):
        """Register a boolean column, These will have default values."""
        column = BooleanColumn(title, size, align)
        self.registry.set(title, column)

    def setDatetime(self, title, *, size, align, fmt='{:%Y-%m-%d}'):
        """Register a datetime column."""
        column = DatetimeColumn(title, size, align, fmt)
        self.registry.set(title, column)

    def getColumn(self, name):
        return self.registry.get(name)

    def getColumns(self):
        for obj in self.registry.iterGet():
            yield obj


class Column:
    def __init__(self, name, size, align, fmt='{}'):
        self.name = name
        self.size = size
        self.align = align
        self.fmt = fmt

    def default(self):
        return ' '


class DatetimeColumn(Column):
    def default(self):
        return '<->'


class BooleanColumn(Column):
    def default(self):
        return 'nil'


class TableItem:
    def __init__(self, expansion=None, **attrs):
        """We should make the expanding indicators customisable here.

        To include sub_items both `sub_title` and `expand_title`
        need to be set.
        """
        self.is_root = True
        if expansion:
            expand_title, sub_title = expansion
            # The `sub_title` should be an available key in attrs
            # even if it's empty
            self.subItems = [
                TableItem(**kwargs) for kwargs in attrs.pop(sub_title)
            ]
            for item in self.subItems:
                item.is_root = False
                setattr(item, expand_title, '>')
            self.expand = False
            attrs.pop(expand_title)
            # Gets name of expandable column and sets value to indicator
            setattr(self, 'expand_title', expand_title)
            setattr(self, expand_title, self.set_indicator())
        self.__dict__.update(attrs)

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            return None

    def isRoot(self):
        return self.is_root

    def set_indicator(self):
        """Indicating if the item can be expanded, and if so
        it will indicate if it has been expanded.
        """
        if self.subItems and self.expand:
            return '▾'
        elif self.subItems:
            return '▸'
        else:
            return ' '

    def toggle_expand(self):
        if self.expand:
            self.expand = False
        else:
            self.expand = True
        setattr(self, self.expand_title, self.set_indicator())


class TableItems:
    def __init__(self, items):
        self.menu = items

    def __len__(self):
        """Length returns the length of all items which are viewable."""
        return sum(1 for _ in self.iter_viewable())

    def iter_viewable(self):
        for item in self.menu:
            yield item
            if hasattr(item, 'expand') and item.expand:
                for subitem in item.subItems:
                    yield subitem
