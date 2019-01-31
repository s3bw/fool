
"""
main = Window(name='main (2)', w=10)
main.left = Window(name='1st left margin (1)', w=10)
main.right = Window(name='1st right margin (4)', w=10)
main.right.left = Window(name='3nd left margin (3)', w=10)
main.right.right = Window(name='2nd right margin (5)', w=10)
main.left.left = Window(name='2nd left margin (0)', w=10)

     (2)
    /   \
  (1)   (4)
  /     / \
(0)   (3) (5)

| 0 | 1 | 2 | 3 | 4 | 5 |
          ^
         main
"""
from fool.console import Screen
from fool.windows import Window, TableWindow
from fool.content import Column, BooleanColumn

root_screen = Screen(100, 60, 0, 0)
console = root_screen.subwin(0, 0)

model = {'main':
    [
        {'title': 'first item', 'description': 'first item description', 'more': True},
        {'title': '2nd item', 'description': '2nd item description', 'more': False},
        {'title': '3rd item', 'description': '3rd item description', 'more': True},
    ]
}

main_items = model['main']
main = TableWindow(w=120, items=main_items)
content = [
    BooleanColumn(name='more', size=2, align='centre'),
    Column(name='title', size=20, align='left'),
    Column(name='description', size=32, align='left'),
]

main.content = content



# r_margin = Window(w=20)
# header = Window(y=5)


# Console responsibilities
main.setup_content()
main.attach_screen(console)
main.draw()

# main.update()
