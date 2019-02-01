from fool.content import Column, BooleanColumn, TextBlob
from fool.windows import TableWindow, Window, TextWindow
from fool.bars import TextBar
from fool.usrip import Input


def table_view(screen, model):
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


def text_view(screen, model):
    """In this example we load text into a window."""
    main = TextWindow(w=70)
    main.content = [
        TextBlob(path='example_text.txt')
    ]
    return [main]


def basic_view(screen, model):
    left, right = model['left_right']
    return [
        TextBar("Option 1 or 2?", 5, 5),
        Input(left=left, right=right),
    ]


def margin_view(screen, model):
    main = Window(w=30)
    main.left = Window(w=20)
    main.right = Window(w=20)
    return [main]
