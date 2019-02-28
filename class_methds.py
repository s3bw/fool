class NotThis:

    key = "This is also key"

    def __init__(self, write=None):
        if write:
            self.write = write

    def write(self):
        print(self.key)


def assign_write(cls):
    def new_write():
        print("<s>" + cls.key + "</s>")
    return new_write


if __name__ == '__main__':
    this = NotThis()
    this.write()

    this.write = assign_write(this)
    this.write()
