<h1 align='center'>
    Fool
</h1>

<h4 align='center'>
    Text-based User Interface Components
</h4>

The goal is to create tui displays quickly, and to encapsulate the interaction logic with each component at instantiation.

## Install

For latest

```
pip install git+ssh://git@github.com/foxyblue/fool.git@master
```

## Fool Projects

- [foolgit](https://github.com/foxyblue/foolgit)
- [foolscap](https://github.com/foxyblue/foolscap) (Not integrated yet)

## Examples

Accept user input

```python
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
```

### Display content

Display text in a window

```python
from fool import console
from fool.content import TextBlob
from fool.windows import TextWindow

def view(screen, model):
    main = TextWindow(w=70)
    main.content = [
        TextBlob(path='example_text.txt')
    ]
    return [main]

model = {}

console.display(view, model, close='q')
```

### Columns

Populate a table.

```python
from fool import console

from fool.content import Column, BooleanColumn
from fool.windows import TableWindow


def view(screen, model):
    main_items = model['main']
    main = TableWindow(w=120, items=main_items)
    columns = [
        BooleanColumn(name='more', size=2, align='centre'),
        Column(name='title', size=20, align='left'),
        Column(name='description', size=32, align='left'),
    ]
    main.columns = columns
    return [main]

model = {'main':
    [
        {'title': 'first item', 'description': 'first item description', 'more': True},
        {'title': '2nd item', 'description': '2nd item description', 'more': False},
        {'title': '3rd item', 'description': '3rd item description', 'more': True},
    ]
}

console.display(view, model, close='q')
```
