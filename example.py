from fool import console
from fool.bars import Bar
from fool.usrip import Input


def view(model):
    left, right = model['left_right']
    return [
        Bar("Option 1 or 2?", 5, 5),
        Input(left=left, right=right),
    ]


def view_option_1(model):
    return [Bar("Option 1", 5, 5)]


def view_option_2(model):
    return [Bar("Option 2", 5, 5)]


model = {'left_right': ('h', 'l')}
action = console.display(view, model)
if action == 'left':
    console.display(view_option_1, model, close='q')
elif action == 'right':
    console.display(view_option_2, model, close='q')
