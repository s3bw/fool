from fool.console import Screen
from fool.windows import Window, Split

root_screen = Screen(100, 100, 0, 0)
console = root_screen.subwin(0, 0)

# 2nd
win = Window()
margin = Window(pin_max_x=10)
split = Split(win, margin, axis='vertical')

# 1st
margin = Window(pin_max_x=15)
split = Split(margin, split, axis='vertical')


# Console responsibilities
split.attach_screen(console)

split.update()
# split.draw()
