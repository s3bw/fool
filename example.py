from fool import console
from examples.views import table_view

model = {
    'entities': [
        {
            'title': 'first item',
            'description': 'first item description',
            'more': True
        },
        {
            'title': '2nd item',
            'description': '2nd item description',
            'more': False
        },
        {
            'title': '3rd item',
            'description': '3rd item description',
            'more': True
        },
        {
            'title': '13rd item',
            'description': '3rd item description',
            'more': True
        },
        {
            'title': '23rd item',
            'description': '3rd item description',
            'more': True
        },
        {
            'title': '33rd item',
            'description': '3rd item description',
            'more': True
        },
    ],
}

y = console.display(table_view, model, close='q')
print(model['entities'][y])

# TabTransition(
#     right='h',
#     left='l',
#     tabs={
#         'general': console.display(table_view, model, close='q'),
#         'books': console.display(table_view, model, close='q'),
#         'talks': console.display(table_view, model, close='q'),
#     })
