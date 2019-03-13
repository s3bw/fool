from fool.console import ConsoleReturn

LOOP_RULE = 4


class Scrollable:
    """Allows a list in a window to be scrollable.

    :param list_pointer: (int) note being actioned upon
    :param cursor_position: (int) cursor position
    :param top_reduction: (int) index of note at 1st line
    :param max_pos: (int) maximum number of cursor_positions
    """

    cursor_position = 1
    top_reduction = 0
    top_line = 0
    list_pointer = 0

    def __init__(self):
        self.control_keys = {
            'up': self.move_up,
            'down': self.move_down,
            'select': self.select,
            'expand': self.expand,
        }

    def expand(self):
        """ Expand the selected item."""
        for index, item in enumerate(self.items.iter_viewable()):
            if index == self.list_pointer:
                if hasattr(item, 'subItems'):
                    item.toggle_expand()

    def select(self):
        """ Selects and returns an index.

        This function won't know what parameters the item holds,
        we should make this more configurable when creating the
        view.
        Until this is fixed, foolscap will fail to call 'view'.
        """
        for index, item in enumerate(self.items.iter_viewable()):
            if index == self.list_pointer and item.isRoot():
                return ConsoleReturn(
                    'select',
                    value=self.list_pointer,
                    key=item.title,
                )

    def move_to_cursor_position(self, cursor_position):
        while self.cursor_position != cursor_position:
            if self.cursor_position > cursor_position:
                self.move_up()
            else:
                self.move_down()

    def move_up(self):
        # list pointer at 0 and up is pressed
        if self.list_pointer <= 0:
            if not self.max_pos - 1 < LOOP_RULE:
                self.list_pointer = self.max_pos - 1
                # cursor_position for small/large terminal max_y
                if self.max_pos < self.bottom_line - 1:
                    self.cursor_position = self.max_pos
                else:
                    self.cursor_position = self.bottom_line - 2
                # top note pointer for small/large terminal max_y
                if self.max_pos < self.bottom_line - 1:
                    self.top_reduction = 0
                else:
                    dy = (self.bottom_line - 1 - self.top_line - 1)
                    self.top_reduction = self.max_pos - dy
        # cursor_position at top line and when list_pointer hasn't reached 0
        elif self.cursor_position == self.top_line + 1:
            self.list_pointer -= 1
            if self.max_pos > self.bottom_line - 1:
                self.top_reduction -= 1
        # cursor_position not at top
        else:
            self.cursor_position -= 1
            self.list_pointer -= 1

    def move_down(self):
        # reached last note
        if self.list_pointer == self.max_pos - 1:
            if not self.max_pos - 1 < LOOP_RULE:
                self.list_pointer = 0
                self.cursor_position = 1
                self.top_reduction = 0
        # reached bottom line
        elif self.cursor_position == self.bottom_line - 2:
            self.list_pointer += 1
            self.top_reduction += 1
        # in the middle
        else:
            self.cursor_position += 1
            self.list_pointer += 1
