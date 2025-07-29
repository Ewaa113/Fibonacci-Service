from app.utils import fibonacci
import pytest


def test_fibonacci_basic():
    assert fibonacci(0) == []
    assert fibonacci(1) == [0]
    assert fibonacci(5) == [0, 1, 1, 2, 3]


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        fibonacci(-1)


def test_fibonacci_too_large():
    with pytest.raises(ValueError):
        fibonacci(1001)
