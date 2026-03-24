"""Tests for Task."""

import pytest
from agent_dispatcher import Task


def dummy():
    return 42


class TestTaskInit:
    def test_required_fields(self):
        t = Task(id="t1", func=dummy)
        assert t.id == "t1"
        assert t.func is dummy

    def test_defaults(self):
        t = Task(id="t1", func=dummy)
        assert t.args == ()
        assert t.kwargs == {}
        assert t.priority == 0
        assert t.status == "pending"
        assert t.result is None
        assert t.error is None
        assert t.duration_ms is None

    def test_custom_args_kwargs(self):
        t = Task(id="t2", func=dummy, args=(1, 2), kwargs={"x": 3}, priority=5)
        assert t.args == (1, 2)
        assert t.kwargs == {"x": 3}
        assert t.priority == 5

    def test_kwargs_none_becomes_empty_dict(self):
        t = Task(id="t3", func=dummy, kwargs=None)
        assert t.kwargs == {}


class TestTaskToDict:
    def test_to_dict_keys(self):
        t = Task(id="t4", func=dummy, args=(7,), priority=2)
        d = t.to_dict()
        assert set(d.keys()) == {
            "id", "func", "args", "kwargs", "priority",
            "status", "result", "error", "duration_ms",
        }

    def test_to_dict_func_name(self):
        t = Task(id="t5", func=dummy)
        assert t.to_dict()["func"] == "dummy"

    def test_to_dict_values(self):
        t = Task(id="t6", func=dummy, args=(1,), kwargs={"k": "v"})
        d = t.to_dict()
        assert d["id"] == "t6"
        assert d["args"] == (1,)
        assert d["kwargs"] == {"k": "v"}

    def test_repr(self):
        t = Task(id="t7", func=dummy)
        assert "t7" in repr(t)
        assert "pending" in repr(t)
