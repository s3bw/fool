from fool.windows import Window


def margin_view(screen, model):
    main = Window(w=30)
    main.left = Window(w=20)
    main.right = Window(w=20)
    return [main]
