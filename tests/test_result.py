"""Tests for DispatchResult."""

from agent_dispatcher import DispatchResult


class TestDispatchResult:
    def test_success_result(self):
        dr = DispatchResult(task_id="r1", success=True, result=99, duration_ms=5.5)
        assert dr.task_id == "r1"
        assert dr.success is True
        assert dr.result == 99
        assert dr.error is None
        assert dr.duration_ms == 5.5

    def test_failure_result(self):
        dr = DispatchResult(task_id="r2", success=False, error="boom", duration_ms=1.0)
        assert dr.success is False
        assert dr.result is None
        assert dr.error == "boom"

    def test_to_dict_keys(self):
        dr = DispatchResult(task_id="r3", success=True, result="hi", duration_ms=3.0)
        d = dr.to_dict()
        assert set(d.keys()) == {"task_id", "success", "result", "error", "duration_ms"}

    def test_to_dict_values(self):
        dr = DispatchResult(task_id="r4", success=True, result=[1, 2], duration_ms=10.0)
        d = dr.to_dict()
        assert d["task_id"] == "r4"
        assert d["result"] == [1, 2]
        assert d["duration_ms"] == 10.0

    def test_repr_ok(self):
        dr = DispatchResult(task_id="r5", success=True, duration_ms=2.0)
        assert "OK" in repr(dr)

    def test_repr_err(self):
        dr = DispatchResult(task_id="r6", success=False, error="oops", duration_ms=1.0)
        assert "ERR" in repr(dr)
