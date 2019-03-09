from fool.tables import ColumnRegistry, TableItem
from fool.windows import TableWindow
from fool.bars import TabBar

column_registry = ColumnRegistry()

column_registry.setBoolean('more', size=2, align='centre')
column_registry.setColumn('title', size=10, align='left')
column_registry.setColumn('description', size=32, align='left')


def table_view(screen, model):
    """In this example we see a scrollable table window."""
    entities = model['entities']
    books = model['books']
    book = model['book']

    table_items = [TableItem(**kwargs) for kwargs in entities]
    main = TableWindow(
        registry=column_registry,
        items=table_items,
        w=50,
        down='j',
        up='k',
        select='p')

    tab = TabBar(book, books, next='l', prev='h')

    return [main, tab]
