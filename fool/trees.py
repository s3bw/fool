"""Tree operations."""


def breadth_first_traversal(obj, value, visit_func):
    """breadth first traversal of windows."""
    queue = [obj]
    while queue:
        obj = queue.pop(0)
        value = visit_func(obj, value)
        if obj.left:
            queue.append(obj.left)
        if obj.right:
            queue.append(obj.right)
    return value


def in_order_traversal(obj, value, visit_func):
    """In order traversal of windows."""
    if obj:
        value = in_order_traversal(obj.left, value, visit_func)
        value = visit_func(obj, value)
        value = in_order_traversal(obj.right, value, visit_func)
    return value
