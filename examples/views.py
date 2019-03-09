from fool.tables import ColumnRegistry, TableItem
from fool.windows import TableWindow
from fool.bars import TabBar

column_registry = ColumnRegistry()

column_registry.setBoolean('more', size=2, align='centre')
column_registry.setColumn('title', size=10, align='left')
column_registry.setColumn('description', size=32, align='left')


def table_view(screen, model):
    """In this example we see a scrollable table window."""
    items = [
        TableItem(expansion=('more', 'sub_items'), **kwargs)
        for kwargs in model['entities']
    ]

    main = TableWindow(
        registry=column_registry,
        items=items,
        w=50,
        down='j',
        up='k',
        select='p',
        expand='e')
    # NOTE(foxyblue): How would the table handle doing 'delete' if I
    # only have one 'select' function?

    # If the Tab bar uses an index instead of a string
    # does it make the logic simpler?
    tab = TabBar(model['book'], model['books'], next='l', prev='h')

    return [main, tab]
