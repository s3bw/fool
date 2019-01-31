from collections import OrderedDict


class Registry:

    def __init__(self):
        self._objects = OrderedDict()

    def get_object(self, name):
        """Get single item from the registry."""
        return self._objects[name]

    def get_objects(self):
        """Yield all objects."""
        for obj in self._objects:
            yield obj

    def register_object(self, name, obj):
        """Register an object."""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object."""
        del self._objects[name]
