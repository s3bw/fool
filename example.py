from fool import console

from fool.content import Column, BooleanColumn
from fool.windows import TableWindow, Window


def view(screen, model):
    main_items = model['main']
    main = TableWindow(w=40, items=main_items)
    content = [
        BooleanColumn(name='more', size=2, align='centre'),
        Column(name='title', size=10, align='left'),
        Column(name='description', size=32, align='left'),
    ]
    main.content = content

    main.right = Window(w=50)
    return [main]


model = {'main':
    [
        {'title': 'first item', 'description': 'first item description', 'more': True},
        {'title': '2nd item', 'description': '2nd item description', 'more': False},
        {'title': '3rd item', 'description': '3rd item description', 'more': True},
    ]
}

console.display(view, model, close='q')
