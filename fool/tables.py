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
        column = BooleanColumn(title, size, align)
        self.registry.set(title, column)

    def getColumn(self, name):
        return self.registry.get(name)

    def getColumns(self):
        for obj in self.registry.iterGet():
            yield obj


class Column:
    def __init__(self, name, size, align='left'):
        self.name = name
        self.size = size
        self.align = align


class BooleanColumn(Column):
    pass


class TableItem:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


class TableItems:
    def __init__(self, items):
        self.menu = items

    def __len__(self):
        return len(self.menu)

    def iter_viewable(self):
        for item in self.menu:
            yield item
            if hasattr(item, 'expand') and item.expand:
                for subitem in item.subitems:
                    yield subitem
