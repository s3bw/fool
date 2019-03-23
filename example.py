from datetime import datetime

from fool import console
from fool.console import ConsoleReturn
from examples.views import table_view

model = {
    'entities': [
        {
            'title': 'first item',
            'description': 'first item description',
            'more': False,
            'sub_items': [],
            'created': datetime(2019, 10, 26),
        },
        {
            'title': '2nd item',
            'description': '2nd item description',
            'more': False,
            'sub_items': [],
            'created': datetime(2019, 10, 26),
        },
        {
            'title':
            '3rd item',
            'description':
            '3rd item description',
            'more':
            True,
            'sub_items': [{
                'title': '13rd item',
                'description': '3rd item description',
            }],
            'created':
            datetime(2019, 10, 26),
        },
        {
            'title': '23rd item',
            'description': '3rd item description',
            'more': False,
            'sub_items': [],
            'created': datetime(2019, 10, 26),
        },
        {
            'title': '33rd item',
            'description': '3rd item description',
            'more': False,
            'sub_items': [],
            'created': datetime(2019, 10, 26),
        },
    ],
    'books': [
        'lists', 'general', 'general', 'general', 'talks', 'talks', 'talks',
        'general', 'general', 'general', 'general', 'general', 'general',
        'general', 'general', 'general', 'talks', 'general', 'general',
        'general', 'general', 'talks', 'design', 'talks', 'textbook', 'lists',
        'general', 'general', 'general', 'lists', 'general', 'general',
        'general', 'textbook', 'general', 'general', 'talks', 'general',
        'general', 'general', 'general', 'general', 'general', 'general',
        'general', 'talks', 'talks', 'general', 'general', 'textbook',
        'textbook', 'general', 'design', 'textbook', 'general', 'general',
        'talks', 'lists', 'general', 'general', 'general', 'general'
    ],
    'book':
    'general',
}

Actor = ConsoleReturn('running')
while Actor.action not in ['close', 'select']:
    Actor = console.display(table_view, model, close='q')
    if Actor.action in ['next', 'prev']:
        model['book'] = Actor.key

if Actor.action != 'close':
    print(model['entities'][Actor.value])
