import itertools


counter = itertools.count()


def travel(ob):
    """Used for debugging.
    Prints the dimensions of mocked screen objects.
    """
    queue = [ob]
    while queue:
        ob = queue.pop(0)
        print(next(counter), ob.width, ob.name, ob.start_x)
        if ob.left:
            queue.append(ob.left)
        if ob.right:
            queue.append(ob.right)
