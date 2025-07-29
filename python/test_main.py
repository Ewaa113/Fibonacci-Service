import pytest
from main import fibonacci


def test_fibonacci_zero():
    assert fibonacci(0) == []


def test_fibonacci_one():
    assert fibonacci(1) == [0]


def test_fibonacci_two():
    assert fibonacci(2) == [0, 1]


def test_fibonacci_five():
    assert fibonacci(5) == [0, 1, 1, 2, 3]


def test_fibonacci_ten():
    assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        fibonacci(-1)


def test_fibonacci_too_large():
    with pytest.raises(ValueError):
        fibonacci(1001)


def test_fibonacci_edge_limit():
    result = fibonacci(1000)
    assert len(result) == 1000
    assert result[0] == 0
    assert result[1] == 1


def test_prometheus_metrics_import():
    """Test that prometheus_client metrics are defined and importable."""
    from main import REQUEST_COUNT, REQUEST_LATENCY, REQUEST_ERRORS
    # Check that metrics are instances of the correct prometheus_client classes
    from prometheus_client import Counter, Histogram
    assert isinstance(REQUEST_COUNT, Counter)
    assert isinstance(REQUEST_LATENCY, Histogram)
