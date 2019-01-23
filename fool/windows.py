import debug
import logging

from fool._base import Base


class Split:

    def __init__(self, win1, win2, axis='vertical'):
        # Can't both have a pin_max.
        # win1 must always have a pin_min.
        #   The default win1 should be the centre.
        # pin_min can't be larger than pin_max.
        self.left = win1
        self.right = win2
        self.axis = axis

    def determine_sizes(self):
        """
        """
        y, x = self.screen.getparyx()
        #print("Parscreen: {}, {}y {}x".format(self.screen.parscreen.name, y, x))
        max_y, max_x = self.screen.getmaxyx()
        print("Max: {}y {}x".format(max_y, max_x))
        max_y, max_x = max_y - y, max_x - x
        # print("Name: {}".format(self.screen.name))
        print("Total allocation: {}y {}x".format(max_y, max_x))
        centre_y, centre_x = int(max_y / 2), int(max_x / 2)

        if self.axis == 'vertical':
            # If Max X and the Max x is less than centre.
            if self.left.pin_max_x and self.left.pin_max_x < centre_x:
                left_h, left_w = max_y, self.left.pin_max_x
                y2, x2 = y, left_w + x
                right_h, right_w = max_y, max_x - left_w
                right_w += 10
                x2 -= 10
                # left_w += 20
            # After checking win1 check win2
            elif self.right.pin_max_x and self.right.pin_max_x < centre_x:
                left_h, left_w = max_y, max_x - self.right.pin_max_x
                y2, x2 = y, left_w + x
                right_h, right_w = max_y, self.right.pin_max_x
                # left_w -= 10
                # right_w -= 4
                # x -= 10
                # x2 -= 10
                # print("Yes")
            # If Min X is greater than or equal to centre.
            elif self.left.pin_min_x >= centre_x:
                left_h, left_w = max_y, self.left.pin_min_x
                y2, x2 = y, left_w + x
                right_h, right_w = max_y, max_x - left_w
            elif self.left.pin_min_x >= max_x:
                left_h, left_w = max_y, max_x
                # Don't render win2.
                y2, x2 = y, left_w + x
                right_h, right_w = max_y, max_x - left_w
            return (left_h, left_w, y, x), (right_h, right_w, y2, x2)

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
        self.left.attach_screen(screen_1)
        self.right.attach_screen(screen_2)

    def update(self):
        # self.update_screen()
        # Resize the windows and splits.
        dimension1, dimension2 = self.determine_sizes()
        self.left.resize(dimension1)
        # h, w, y, x = dimension2
        self.right.resize(dimension2)
        self.left.update()
        self.right.update()

    def resize(self, dimensions):
        h, w, y, x = dimensions
        # Move y, x
        self.screen.mvderwin(y, x)
        # Resize h, w
        self.screen.resize(h, w)

    def draw(self):
        self.left.draw()
        self.right.draw()

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
