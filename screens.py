from fool._debug import Screen
from fool.windows import Window, TableWindow
from fool.content import Column, BooleanColumn

root_screen = Screen(100, 60, 0, 0)
console = root_screen.subwin(0, 0)

main = Window(name='main (2)', w=10)
main.left = Window(name='1st left margin (1)', w=10)
main.right = Window(name='1st right margin (4)', w=10)
main.right.left = Window(name='3nd left margin (3)', w=10)
main.right.right = Window(name='2nd right margin (5)', w=10)
main.left.left = Window(name='2nd left margin (0)', w=10)



# Console responsibilities
main.attach_screen(console)
# main.draw()

# main.update()
