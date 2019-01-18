class KeyListener:

    def __init__(self):
        self.keys = {}

    def attach_screen(self, screen):
        self.screen = screen

    def key_press(self):
        key = self.screen.getch()
        if chr(key) in self.keys:
            return self.keys[chr(key)]()
        return False
