import pytest

from fool.windows import assign_x
from fool.windows import assign_width


class MockNode:

    def __init__(self, max_w):
        self.max_w = max_w


@pytest.mark.parametrize("w, remaining, expected", [
    # w < remaining
    (10, 20, (10, 10)),
    # w > remaining
    (10, 0, (0, 0)),
    # w == remaining
    (30, 30, (0, 30)),
    # w > remaining and remaining != 0
    (20, 10, (0, 10)),
])
def test_assign_width(w, remaining, expected):
    expected_remaining, expected_width = expected
    node = MockNode(w)
    result = assign_width(node, remaining)
    assert result == expected_remaining
    assert node.width == expected_width


def test_assign_x():
    node = MockNode(10)
    node.width = 10
    result = assign_x(node, 0)
    assert result == 10
