import debug
import logging

from fool._base import Base


class Split:

    def __init__(self, win1, win2, axis='vertical'):
        # Can't both have a pin_max.
        # win1 must always have a pin_min.
        #   The default win1 should be the centre.
        # pin_min can't be larger than pin_max.
        self.win1 = win1
        self.win2 = win2
        self.pin_max_x = self.win1.pin_max_x if self.win1.pin_max_x else None
        self.axis = axis

    def determine_sizes(self):
        """
        """
        y, x = self.screen.getparyx()
        max_y, max_x = self.screen.getmaxyx()
        max_y, max_x = max_y - y, max_x - x
        centre_y, centre_x = int(max_y / 2), int(max_x / 2)

        if self.axis == 'vertical':
            # If Max X and the Max x is less than centre.
            if self.win1.pin_max_x and self.win1.pin_max_x < centre_x:
                win1_h, win1_w = max_y, self.win1.pin_max_x
                y2, x2 = y, win1_w + x
                win2_h, win2_w = max_y, max_x - win1_w
                x2 = 5
            # After checking win1 check win2
            elif self.win2.pin_max_x and self.win2.pin_max_x < centre_x:
                win1_h, win1_w = max_y, max_x - self.win2.pin_max_x
                y2, x2 = y, win1_w + x
                win2_h, win2_w = max_y, self.win2.pin_max_x
                win1_w += 5
                x += 5
                print(max_x, self.win2.pin_max_x, x, x2)
            # If Min X is greater than or equal to centre.
            elif self.win1.pin_min_x >= centre_x:
                win1_h, win1_w = max_y, self.win1.pin_min_x
                y2, x2 = y, win1_w + x
                win2_h, win2_w = max_y, max_x - win1_w
            elif self.win1.pin_min_x >= max_x:
                win1_h, win1_w = max_y, max_x
                # Don't render win2.
                y2, x2 = y, win1_w + x
                win2_h, win2_w = max_y, max_x - win1_w
            # logging.info((win1_h, win1_w, y, x), (win2_h, win2_w, y2, x2))
            return (win1_h, win1_w, y, x), (win2_h, win2_w, y2, x2)
            # return (win1_h, win1_w, y, x), (y2, x2)

    def attach_screen(self, screen):
        self.screen = screen
        # y, x = screen.getyx()
        # max_y, max_x = screen.getmaxyx()
        # self.win1.paryx = (max_y, max_x)
        # self.win2.paryx = (max_y, max_x)
        # self.screen = screen.subwin(max_y, max_x, y, x)
        # logging.info((max_y, max_x, y, x))
        dimension1, dimension2 = self.determine_sizes()
        screen_1 = self.screen.subwin(*dimension1)
        screen_2 = self.screen.subwin(*dimension2)
        # import logging
        # logging.info(screen_1.getparyx())
        # logging.info(screen_2.getparyx())
        self.win1.attach_screen(screen_1)
        self.win2.attach_screen(screen_2)

    def update(self):
        # self.update_screen()
        # Resize the windows and splits.
        dimension1, dimension2 = self.determine_sizes()
        logging.info(("dim1", dimension1, self.screen.getmaxyx()))
        self.win1.resize(dimension1)
        # h, w, y, x = dimension2
        logging.info(("dim2", dimension2, self.screen.getmaxyx()))
        self.win2.resize(dimension2)
        self.win1.update()
        self.win2.update()

    def resize(self, dimensions):
        h, w, y, x = dimensions
        # Move y, x
        self.screen.mvderwin(y, x)
        # Resize h, w
        self.screen.resize(h, w)

    def draw(self):
        self.win1.draw()
        self.win2.draw()

    def visit(self, listener):
        """These could be adjust split keys."""
        pass


class Window(Base):

    # def __init__(self, h, w, y, x, screen):
    #     self.screen = self.screen.subwin(h, w, y, x)

    #     self.text = text
    #     self.x = x
    #     self.y = y
    #     self.hr = hr
    #     self.wr = wr
    def __init__(self, pin_max_x=None, pin_min_x=None):
        self.pin_max_x = pin_max_x
        self.pin_min_x = pin_min_x if pin_min_x else pin_max_x

    def resize(self, dimensions):
        h, w, y, x = dimensions
        self.screen.mvderwin(y, x)
        # Resize h, w
        self.screen.resize(h, w)

    def update(self):
        super(Window, self).update()
        # self.window = self.screen.subwin(self.h, self.w, self.y, self.x)

    def draw(self):
        # if self.x <= self.max_x and self.y <= self.max_y:
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
