"""Tests for @dispatch_parallel decorator."""

import time
import pytest
from agent_dispatcher import dispatch_parallel


def square(x):
    return x * x


def slow_double(x):
    time.sleep(0.05)
    return x * 2


def fail_on_zero(x):
    if x == 0:
        raise ValueError("zero not allowed")
    return x


class TestDispatchParallel:
    def test_basic_parallel(self):
        @dispatch_parallel(max_workers=4)
        def sq(x):
            return x * x

        results = sq([(1,), (2,), (3,), (4,)])
        assert results == [1, 4, 9, 16]

    def test_returns_list(self):
        @dispatch_parallel(max_workers=2)
        def identity(x):
            return x

        out = identity([("a",), ("b",), ("c",)])
        assert isinstance(out, list)
        assert len(out) == 3

    def test_parallel_speedup(self):
        @dispatch_parallel(max_workers=10)
        def slow(x):
            time.sleep(0.1)
            return x

        start = time.perf_counter()
        slow([(i,) for i in range(10)])
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0

    def test_raises_on_failure(self):
        @dispatch_parallel(max_workers=2)
        def maybe_fail(x):
            if x == 0:
                raise ValueError("zero!")
            return x

        with pytest.raises(RuntimeError, match="failed"):
            maybe_fail([(0,)])

    def test_functools_wraps_preserves_name(self):
        @dispatch_parallel(max_workers=2)
        def my_function(x):
            return x

        assert my_function.__name__ == "my_function"

    def test_single_arg_tuple(self):
        @dispatch_parallel(max_workers=1)
        def double(x):
            return x * 2

        result = double([(5,)])
        assert result == [10]
