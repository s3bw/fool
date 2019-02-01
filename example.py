from fool import console
from examples.views import table_view
from examples.views import text_view
from examples.views import basic_view
from examples.views import margin_view


model = {
    'main':
    [
        {'title': 'first item', 'description': 'first item description', 'more': True},
        {'title': '2nd item', 'description': '2nd item description', 'more': False},
        {'title': '3rd item', 'description': '3rd item description', 'more': True},
    ],
    'left_right': ('h', 'l'),
}

console.display(table_view, model, close='q')
console.display(text_view, model, close='q')
console.display(basic_view, model, close='q')
console.display(margin_view, model, close='q')
