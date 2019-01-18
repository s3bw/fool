from fool import console
from fool.usrip import Input
from fool.bars import TextBar
from fool.bars import ToggleBar


def view(model):
    left, right = model['left_right']
    return [
        TextBar("Option 1 or 2?", 5, 5),
        Input(left=left, right=right),
        ToggleBar(['Show', 'This', 'can', 'toggle'], 5, 10, toggle='H'),
    ]


def view_option_1(model):
    return [TextBar("Option 1", 5, 5)]


def view_option_2(model):
    return [TextBar("Option 2", 5, 5)]


model = {'left_right': ('h', 'l')}
action = console.display(view, model)
if action == 'left':
    console.display(view_option_1, model, close='q')
elif action == 'right':
    console.display(view_option_2, model, close='q')
