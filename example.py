from fool import console
from fool.usrip import Input
from fool.bars import TextBar
from fool.bars import ToggleBar
from fool.windows import Split
from fool.windows import Window


def view(screen, model):
    left, right = model['left_right']

    win = Window()
    margin = Window(pin_max_x=20)
    split = Split(win, margin, axis='vertical')

    margin = Window(pin_max_x=10)
    split = Split(margin, split, axis='vertical')
    return [
        split,
        # TextBar("Option 1 or 2?", 40, 5),
        # Input(left=left, right=right),
        # ToggleBar(['Show', 'This', 'can', 'toggle'], 40, 10, toggle='H'),
    ]


def view_option_1(screen, model):
    return [TextBar("Option 1", 5, 5)]


def view_option_2(screen, model):
    return [TextBar("Option 2", 5, 5)]


model = {'left_right': ('h', 'l')}
action = console.display(view, model, close='q')
if action == 'left':
    console.display(view_option_1, model, close='q')
elif action == 'right':
    console.display(view_option_2, model, close='q')
