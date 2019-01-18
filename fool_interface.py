"""
Tweaking the Full Vision
"""

from fool import Console
from fool import KeyListener

from fool.bars import TabBar
from fool.bars import TextBar
from fool.bars import StatusBar
"""
Status bar is a dynamic TextBar
"""
from fool.windows import TableWindow
"""
Table doesn't have to have a cursor
"""
from fool.windows import Window


def main_table(data):

    items = data['items']
    columns = [
        Column('book', size=10, align='centre'),
        Column('length', size=5, align='left'),
        Column('views', size=5, align='right'),
    ]
    table = TableWindow(items, columns, cursor=True, x=1, y=1, h=10,
                        scroll_keys=['j', 'k'], select='i', toggle='e')
    table.x = 1
    table.y = 1


def detail_table(data):
    items = transpose_items(data['items'])
    columns = [
        Column('book', size=5, align='centre'),
        Column('length', size=5, align='left'),
    ]
    return TableWindow(items, columns, x=1, y='y/2'),


def preview_window(data):
    paths = find_paths(data['paths'])
    return Window(paths, x='x/2', y='y/2',
        func=draw_window(lambda x: open(x).read()))


def main_view(data):

    # Define an interaction.
    detail_t.active = main_t.selected

    pane = Pane([main_table, [detail_table, preview]], ('h', ('v')))

    return [
        TextBar('path'),
        StatusBar(options=['help', 'exit'], toggle='p'),
        TabBar(active, tabs, tab_keys=['h', 'l']),
        main_table(data),
        detail_table(data),
        preview_window(data),
        TextBar('Foolscap', x=1, y='y/2'),
    ]


# I can inherit things from a base view like the title and help
# This is quite similar to components.
default = default_view(data)
tags = tags_view(data).extends(default)
