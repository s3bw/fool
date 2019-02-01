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

Please see [example.py](./example.py) for working examples of the views found [here](./examples/views.py)

Accept user input

```python
from fool import console
from fool.bars import TextBar
from fool.usrip import Input


def view(screen, model):
    left, right = model['left_right']
    return [
        TextBar("Option 1 or 2?", 5, 5),
        Input(left=left, right=right),
    ]


def view_option_1(screen, model):
    return [TextBar("Option 1", 5, 5)]


def view_option_2(screen, model):
    return [TextBar("Option 2", 5, 5)]


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
    """In this example we see a scrollable table window."""
    main_items = model['main']
    main = TableWindow(w=40, items=main_items, scroll=('k', 'j'))
    content = [
        BooleanColumn(name='more', size=2, align='centre'),
        Column(name='title', size=10, align='left'),
        Column(name='description', size=32, align='left'),
    ]
    main.content = content
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
