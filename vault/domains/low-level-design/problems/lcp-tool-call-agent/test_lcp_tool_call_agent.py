import importlib
import os
import threading
import time

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
run_agent = impl.run_agent

WAIT = 5  # 屏障与事件的等待上限（秒）：只用来把测试的挂死变成失败，正确的实现从不等到它


def call(call_id, name="t", **arguments):
    return {"id": call_id, "name": name, "arguments": arguments}


def reply(text="", *calls):
    return {"text": text, "tool_calls": list(calls)}


def scripted(*responses):
    """按顺序给出响应的模型；`seen` 记下每次调用收到的消息快照。"""
    queue = iter(responses)
    seen = []

    def model(messages):
        seen.append(messages)
        return next(queue)

    return model, seen


def tool_contents(result):
    return [m["content"] for m in result["messages"] if m["role"] == "tool"]


READINGS = {"Oslo": -3, "Lima": 19}


def temp(city):
    return {"city": city, "celsius": READINGS[city]}


# ---- 对话记录与返回形状 ----

def test_worked_example_runs_two_tools_and_orders_results():
    model, _ = scripted(
        reply("Looking up both cities", call("x1", "temp", city="Oslo"), call("x2", "temp", city="Lima")),
        reply("Lima is warmer"),
    )
    result = run_agent("Which is warmer, Oslo or Lima?", model, {"temp": temp}, max_workers=2)
    assert result["answer"] == "Lima is warmer"
    assert (result["model_calls"], result["tool_calls"]) == (2, 2)
    assert [m["tool_call_id"] for m in result["messages"] if m["role"] == "tool"] == ["x1", "x2"]
    assert tool_contents(result) == [{"ok": True, "value": {"city": "Oslo", "celsius": -3}},
                                     {"ok": True, "value": {"city": "Lima", "celsius": 19}}]


def test_terminal_response_shape_and_empty_text_answer():
    model, seen = scripted(reply(""))
    result = run_agent("", model, {})
    assert result == {"answer": "", "model_calls": 1, "tool_calls": 0, "messages": [
        {"role": "user", "content": ""},
        {"role": "assistant", "content": "", "tool_calls": []}]}
    assert seen == [[{"role": "user", "content": ""}]]


def test_text_beside_calls_is_intermediate_and_messages_are_exact():
    model, _ = scripted(reply("thinking", call("x", "t", n=1)), reply("final"))
    result = run_agent("q", model, {"t": lambda n: n + 1})
    assert result["answer"] == "final"
    assert result["messages"] == [
        {"role": "user", "content": "q"},
        {"role": "assistant", "content": "thinking", "tool_calls": [call("x", "t", n=1)]},
        {"role": "tool", "tool_call_id": "x", "name": "t", "content": {"ok": True, "value": 2}},
        {"role": "assistant", "content": "final", "tool_calls": []}]


def test_model_sees_results_before_its_next_call_and_later_turns_depend_on_them():
    queue = iter([reply("", call("p", "temp", city="Lima")), None, reply("done")])
    seen = []

    def model(messages):
        seen.append(messages)
        response = next(queue)
        if response is None:
            tool_message = messages[-1]
            assert tool_message["role"] == "tool"
            assert messages[-2]["role"] == "assistant"
            return reply("", call("d", "diff", left=tool_message["content"]["value"]["celsius"], right=10))
        return response

    tools = {"temp": temp, "diff": lambda left, right: left - right}
    result = run_agent("q", model, tools)
    assert tool_contents(result)[-1] == {"ok": True, "value": 9}
    assert [len(s) for s in seen] == [1, 3, 5]
    assert result["tool_calls"] == 2 and result["model_calls"] == 3


# ---- 入口校验 ----

@pytest.mark.parametrize("kwargs", [
    {"max_turns": 0}, {"max_turns": -1}, {"max_turns": True}, {"max_turns": 2.0}, {"max_turns": "2"},
    {"max_tool_calls": -1}, {"max_tool_calls": False}, {"max_tool_calls": 1.0}, {"max_tool_calls": None},
    {"max_workers": 0}, {"max_workers": True}, {"max_workers": 1.0}, {"max_workers": -3},
])
def test_invalid_budgets_raise_before_any_model_call(kwargs):
    calls = []
    with pytest.raises(ValueError):
        run_agent("q", lambda messages: calls.append(messages) or reply("x"), {}, **kwargs)
    assert calls == []


@pytest.mark.parametrize("question", [None, 3, b"q", ["q"]])
def test_non_string_question_raises_before_the_model(question):
    calls = []
    with pytest.raises(ValueError):
        run_agent(question, lambda messages: calls.append(1) or reply("x"), {})
    assert calls == []


@pytest.mark.parametrize("tools", [None, [], {"": print}, {"t": 5}, {3: print}])
def test_invalid_tool_registry_raises_before_the_model(tools):
    calls = []
    with pytest.raises(ValueError):
        run_agent("q", lambda messages: calls.append(1) or reply("x"), tools)
    assert calls == []


def test_boundary_budgets_are_accepted():
    model, _ = scripted(reply("done"))
    result = run_agent("q", model, {}, max_turns=1, max_tool_calls=0, max_workers=1)
    assert result["answer"] == "done"


# ---- 工具错误 ----

def test_unknown_tool_and_tool_exception_become_fixed_error_results():
    def boom():
        raise RuntimeError("secret detail")

    model, _ = scripted(reply("", call("u", "missing"), call("b", "boom"), call("ok", "fine")), reply("end"))
    result = run_agent("q", model, {"boom": boom, "fine": lambda: 7})
    assert tool_contents(result) == [{"ok": False, "error": "unknown_tool"},
                                     {"ok": False, "error": "tool_error"},
                                     {"ok": True, "value": 7}]
    assert "secret" not in repr(result["messages"])
    assert result["tool_calls"] == 3


def test_argument_binding_errors_are_tool_errors():
    model, _ = scripted(reply("", call("a", "t", wrong=1), call("b", "t")), reply("end"))
    result = run_agent("q", model, {"t": lambda city: city})
    assert tool_contents(result) == [{"ok": False, "error": "tool_error"}] * 2


@pytest.mark.parametrize("make", [
    lambda: (1, 2), lambda: {1, 2}, lambda: object(), lambda: float("nan"), lambda: float("inf"),
    lambda: {1: "x"}, lambda: b"raw", lambda: [1, (2,)], lambda: print,
])
def test_non_json_tool_results_are_tool_errors(make):
    model, _ = scripted(reply("", call("a", "t")), reply("end"))
    result = run_agent("q", model, {"t": make})
    assert tool_contents(result) == [{"ok": False, "error": "tool_error"}]


@pytest.mark.parametrize("value", [None, 0, "", [], {}, False, 1.5, {"k": [1, {"z": None}]}])
def test_json_tool_results_are_kept_as_they_are(value):
    model, _ = scripted(reply("", call("a", "t")), reply("end"))
    result = run_agent("q", model, {"t": lambda: value})
    assert tool_contents(result) == [{"ok": True, "value": value}]


def test_provider_exception_propagates_unchanged():
    error = KeyError("provider down")

    def model(messages):
        raise error

    with pytest.raises(KeyError) as caught:
        run_agent("q", model, {})
    assert caught.value is error


def test_base_exception_propagates_after_started_calls_finish():
    class Halt(BaseException):
        pass

    gate = threading.Barrier(2, timeout=WAIT)
    finished = threading.Event()

    def boom():
        gate.wait()
        raise Halt()

    def slow():
        gate.wait()
        time.sleep(0.05)
        finished.set()
        return 1

    model, _ = scripted(reply("", call("a", "boom"), call("b", "slow")), reply("never"))
    with pytest.raises(Halt):
        run_agent("q", model, {"boom": boom, "slow": slow}, max_workers=2)
    assert finished.is_set()


# ---- 协议校验 ----

class MyInt(int):
    pass


BAD_RESPONSES = [
    "text", None, [], {"text": "x"}, {"tool_calls": []}, {"text": "x", "tool_calls": [], "extra": 1},
    {"text": 1, "tool_calls": []}, {"text": "x", "tool_calls": ()}, {"text": "x", "tool_calls": None},
    reply("", "not a dict"), reply("", {"id": "a", "name": "t"}),
    reply("", {"id": "a", "name": "t", "arguments": {}, "extra": 1}),
    reply("", call("", "t")), reply("", call("a", "")), reply("", {"id": 1, "name": "t", "arguments": {}}),
    reply("", {"id": "a", "name": 2, "arguments": {}}),
    reply("", {"id": "a", "name": "t", "arguments": []}), reply("", {"id": "a", "name": "t", "arguments": None}),
    reply("", call("a", "t", v=(1, 2))), reply("", call("a", "t", v={1, 2})),
    reply("", call("a", "t", v=float("nan"))), reply("", call("a", "t", v=float("-inf"))),
    reply("", call("a", "t", v=object())), reply("", call("a", "t", v=b"x")),
    reply("", call("a", "t", v=MyInt(3))), reply("", call("a", "t", v=[1, [2, (3,)]])),
    reply("", {"id": "a", "name": "t", "arguments": {"v": {1: 2}}}),
    reply("", {"id": "a", "name": "t", "arguments": {1: 2}}),
]


@pytest.mark.parametrize("response", BAD_RESPONSES)
def test_malformed_model_output_raises_value_error(response):
    with pytest.raises(ValueError):
        run_agent("q", lambda messages: response, {"t": lambda **kw: 1})


def test_whole_response_is_validated_before_any_tool_runs():
    ran = []
    model, _ = scripted(reply("", call("a", "t", n=1), call("b", "t", n=float("nan"))))
    with pytest.raises(ValueError):
        run_agent("q", model, {"t": lambda n: ran.append(n)})
    assert ran == []


def test_every_json_value_kind_is_accepted_as_an_argument():
    arguments = {"a": None, "b": True, "c": 1, "d": 1.5, "e": "你好 é", "f": [1, [2], {"g": None}], "h": {}}
    model, _ = scripted(reply("", call("x", "echo", **arguments)), reply("end"))
    result = run_agent("q", model, {"echo": lambda **kw: kw})
    assert tool_contents(result) == [{"ok": True, "value": arguments}]


# ---- 重放缓存与冲突 ----

def test_duplicate_ids_in_one_response_share_one_execution():
    runs = []
    model, _ = scripted(reply("", call("x", "t", n=1), call("y", "t", n=2), call("x", "t", n=1)), reply("end"))
    result = run_agent("q", model, {"t": lambda n: runs.append(n) or n * 10})
    assert sorted(runs) == [1, 2]
    assert tool_contents(result) == [{"ok": True, "value": 10}, {"ok": True, "value": 20}, {"ok": True, "value": 10}]
    assert result["tool_calls"] == 2


def test_replay_across_responses_ignores_key_order_and_does_not_count_again():
    runs = []

    def t(**kw):
        runs.append(kw)
        return len(runs)

    model, _ = scripted(reply("", call("x", "t", b=1, a=[1, 2], c="你")),
                        reply("", {"id": "x", "name": "t", "arguments": {"c": "你", "a": [1, 2], "b": 1}}),
                        reply("end"))
    result = run_agent("q", model, {"t": t}, max_tool_calls=1)
    assert len(runs) == 1
    assert tool_contents(result) == [{"ok": True, "value": 1}] * 2
    assert result["tool_calls"] == 1


def test_error_results_are_replayed_too():
    runs = []

    def boom():
        runs.append(1)
        raise ValueError("x")

    model, _ = scripted(reply("", call("x", "boom")), reply("", call("x", "boom")), reply("end"))
    result = run_agent("q", model, {"boom": boom})
    assert len(runs) == 1
    assert tool_contents(result) == [{"ok": False, "error": "tool_error"}] * 2


@pytest.mark.parametrize("second", [
    call("x", "other", n=1), call("x", "t", n=2), call("x", "t", n=1.0), call("x", "t", n=True),
    call("x", "t", n=1, extra=0), call("x", "t", n="1"),
])
def test_id_reuse_with_different_name_or_arguments_is_rejected(second):
    ran = []
    model, _ = scripted(reply("", call("x", "t", n=1)), reply("", call("n", "t", n=9), second))
    with pytest.raises(ValueError):
        run_agent("q", model, {"t": lambda n=0, extra=0: ran.append(n), "other": lambda n: n})
    assert ran == [1]  # 冲突的响应里，连不冲突的 n 也没有执行


def test_array_order_and_numeric_form_are_part_of_the_signature():
    model, _ = scripted(reply("", call("x", "t", v=[1, 2])), reply("", call("x", "t", v=[2, 1])))
    with pytest.raises(ValueError):
        run_agent("q", model, {"t": lambda v: v})
    model, _ = scripted(reply("", call("x", "t", v=1.0)), reply("", call("x", "t", v=1.00)), reply("end"))
    assert run_agent("q", model, {"t": lambda v: v})["tool_calls"] == 1


def test_conflict_inside_one_response_is_rejected_before_execution():
    ran = []
    model, _ = scripted(reply("", call("x", "t", n=1), call("x", "t", n=2)))
    with pytest.raises(ValueError):
        run_agent("q", model, {"t": lambda n: ran.append(n)})
    assert ran == []


def test_each_run_has_its_own_cache_and_counters():
    ran = []
    tools = {"t": lambda: ran.append(1)}
    for _ in range(2):
        model, _ = scripted(reply("", call("x", "t")), reply("end"))
        assert run_agent("q", model, tools, max_tool_calls=1)["tool_calls"] == 1
    assert len(ran) == 2


# ---- 预算 ----

def test_tool_budget_is_reserved_for_the_whole_response_before_anything_runs():
    ran = []
    t = lambda n: ran.append(n)
    model, _ = scripted(reply("", call("a", "t", n=1)), reply("", call("b", "t", n=2), call("c", "t", n=3)))
    with pytest.raises(RuntimeError, match="tool budget exceeded"):
        run_agent("q", model, {"t": t}, max_tool_calls=2)
    assert ran == [1]  # 之前批次不回滚；超额的批次一个也不执行


def test_zero_tool_budget_rejects_any_new_call_but_allows_a_plain_answer():
    model, _ = scripted(reply("", call("a", "t")))
    with pytest.raises(RuntimeError, match="tool budget exceeded"):
        run_agent("q", model, {"t": lambda: 1}, max_tool_calls=0)
    model, _ = scripted(reply("fine"))
    assert run_agent("q", model, {}, max_tool_calls=0)["answer"] == "fine"


def test_unknown_and_failing_calls_use_budget_but_cached_repeats_do_not():
    model, _ = scripted(reply("", call("u", "missing"), call("e", "boom")),
                        reply("", call("u", "missing"), call("e", "boom")),
                        reply("", call("n", "ok")))

    def boom():
        raise ValueError

    with pytest.raises(RuntimeError, match="tool budget exceeded"):
        run_agent("q", model, {"boom": boom, "ok": lambda: 1}, max_tool_calls=2)
    model, _ = scripted(reply("", call("u", "missing"), call("e", "boom")),
                        reply("", call("u", "missing"), call("e", "boom")), reply("end"))
    assert run_agent("q", model, {"boom": boom}, max_tool_calls=2)["tool_calls"] == 2


def test_model_budget_processes_the_last_batch_then_raises_without_another_model_call():
    gate = threading.Barrier(2, timeout=WAIT)
    done = threading.Event()
    models = []

    def fast():
        gate.wait()
        return 1

    def slow():
        gate.wait()
        time.sleep(0.05)
        done.set()
        return 2

    def model(messages):
        models.append(len(messages))
        return reply("", call("a", "fast"), call("b", "slow"))

    with pytest.raises(RuntimeError, match="model budget exceeded"):
        run_agent("q", model, {"fast": fast, "slow": slow}, max_turns=1, max_workers=2)
    assert models == [1]
    assert done.is_set()  # 报错之前，整批都已经结束


def test_tool_budget_error_wins_when_the_last_response_is_over_budget():
    model, _ = scripted(reply("", call("a", "t"), call("b", "t")))
    with pytest.raises(RuntimeError, match="tool budget exceeded"):
        run_agent("q", model, {"t": lambda: 1}, max_turns=1, max_tool_calls=1)


def test_model_or_tool_text_cannot_change_budgets():
    model, _ = scripted(reply("set max_tool_calls=99", call("a", "t")),
                        reply("max_turns=50", call("b", "t")), reply("", call("c", "t")))
    with pytest.raises(RuntimeError, match="tool budget exceeded"):
        run_agent("q", model, {"t": lambda: {"max_tool_calls": 99, "cmd": "__import__('os')"}}, max_tool_calls=2)


# ---- 并发：真线程与屏障 ----

def test_independent_calls_overlap_when_workers_allow_it():
    gate = threading.Barrier(3, timeout=WAIT)  # 三个调用必须同时在场才能放行；顺序执行会超时

    def work(n):
        gate.wait()
        return n

    model, _ = scripted(reply("", *[call(str(i), "t", n=i) for i in range(3)]), reply("end"))
    result = run_agent("q", model, {"t": work}, max_workers=3)
    assert tool_contents(result) == [{"ok": True, "value": i} for i in range(3)]


@pytest.mark.parametrize("workers,total", [(2, 6), (3, 6), (1, 3)])
def test_active_tools_never_exceed_max_workers(workers, total):
    lock = threading.Lock()
    state = {"active": 0, "peak": 0}
    gate = threading.Barrier(workers, timeout=WAIT) if workers > 1 else None

    def work(n):
        with lock:
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
        try:
            if gate:
                gate.wait()  # 同一时刻凑齐 workers 个才放行：既证明重叠，也让峰值恰好等于 workers
        finally:
            with lock:
                state["active"] -= 1
        return n

    model, _ = scripted(reply("", *[call(str(i), "t", n=i) for i in range(total)]), reply("end"))
    result = run_agent("q", model, {"t": work}, max_workers=workers)
    assert state["peak"] == workers
    assert [c["value"] for c in tool_contents(result)] == list(range(total))


def test_results_follow_request_order_even_when_completion_order_is_reversed():
    n = 4
    done = [threading.Event() for _ in range(n)]
    finished = []

    def work(i):
        if i < n - 1:
            assert done[i + 1].wait(WAIT)  # 等后一个先完成
        finished.append(i)
        done[i].set()
        return i

    model, _ = scripted(reply("", *[call(str(i), "t", i=i) for i in range(n)]), reply("end"))
    result = run_agent("q", model, {"t": work}, max_workers=n)
    assert finished == [3, 2, 1, 0]
    assert [c["value"] for c in tool_contents(result)] == [0, 1, 2, 3]
    assert [m["tool_call_id"] for m in result["messages"] if m["role"] == "tool"] == ["0", "1", "2", "3"]


def test_single_worker_runs_calls_in_first_occurrence_order():
    order = []
    model, _ = scripted(reply("", call("c", "t", n=3), call("a", "t", n=1), call("c", "t", n=3), call("b", "t", n=2)),
                        reply("end"))
    result = run_agent("q", model, {"t": lambda n: order.append(n) or n}, max_workers=1)
    assert order == [3, 1, 2]
    assert [c["value"] for c in tool_contents(result)] == [3, 1, 3, 2]


def test_no_worker_thread_survives_the_run_on_success_or_error():
    before = set(threading.enumerate())
    model, _ = scripted(reply("", call("a", "t"), call("b", "t")), reply("end"))
    run_agent("q", model, {"t": lambda: 1}, max_workers=2)
    model, _ = scripted(reply("", call("a", "t"), call("b", "t")))
    with pytest.raises(RuntimeError):
        run_agent("q", model, {"t": lambda: 1}, max_turns=1, max_workers=2)
    assert set(threading.enumerate()) <= before


def test_huge_worker_limit_is_fine_for_a_small_batch():
    model, _ = scripted(reply("", call("a", "t"), call("b", "t")), reply("end"))
    assert run_agent("q", model, {"t": lambda: 1}, max_workers=10**6)["tool_calls"] == 2


def test_parallel_runs_do_not_share_state():
    results = {}
    start = threading.Barrier(6, timeout=WAIT)

    def run(i):
        model, _ = scripted(reply("", call("x", "t", n=i)), reply(f"answer {i}"))
        start.wait()
        results[i] = run_agent(f"q{i}", model, {"t": lambda n: n * 2}, max_workers=2)

    threads = [threading.Thread(target=run, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(WAIT)
    for i in range(6):
        assert results[i]["answer"] == f"answer {i}"
        assert tool_contents(results[i]) == [{"ok": True, "value": i * 2}]
        assert results[i]["messages"][0]["content"] == f"q{i}"


# ---- 数据所有权 ----

def test_model_cannot_change_history_through_its_snapshot_or_its_old_response():
    first = reply("one", call("x", "t", items=[1]))

    def model(messages):
        if len(messages) == 1:
            return first
        messages[0]["content"] = "hacked"
        messages.append({"role": "user", "content": "extra"})
        first["text"] = "mutated"
        first["tool_calls"][0]["arguments"]["items"].append(99)
        return reply("end")

    result = run_agent("q", model, {"t": lambda items: items})
    assert result["messages"][0]["content"] == "q"
    assert result["messages"][1] == {"role": "assistant", "content": "one",
                                     "tool_calls": [call("x", "t", items=[1])]}
    assert len(result["messages"]) == 4
    assert tool_contents(result) == [{"ok": True, "value": [1]}]


def test_tool_cannot_change_recorded_arguments_or_cache_by_mutating_its_inputs():
    def t(items):
        items.append(9)
        return items

    model, _ = scripted(reply("", call("x", "t", items=[1])),
                        reply("", call("x", "t", items=[1])), reply("end"))
    result = run_agent("q", model, {"t": t})
    assert result["messages"][1]["tool_calls"] == [call("x", "t", items=[1])]
    assert tool_contents(result) == [{"ok": True, "value": [1, 9]}] * 2


def test_tool_cannot_change_recorded_results_by_keeping_a_reference():
    kept = []

    def t(n):
        value = {"n": n, "log": []}
        kept.append(value)
        return value

    model, _ = scripted(reply("", call("a", "t", n=1)), reply("", call("b", "t", n=2)), reply("end"))
    result = run_agent("q", model, {"t": t})
    kept[0]["log"].append("late write")
    assert tool_contents(result)[0] == {"ok": True, "value": {"n": 1, "log": []}}


def test_each_occurrence_of_a_cached_result_is_an_independent_copy():
    model, _ = scripted(reply("", call("x", "t"), call("x", "t")), reply("", call("x", "t")), reply("end"))
    result = run_agent("q", model, {"t": lambda: {"v": [1]}})
    contents = tool_contents(result)
    contents[0]["value"]["v"].append(2)
    assert contents[1]["value"] == {"v": [1]} and contents[2]["value"] == {"v": [1]}


def test_tool_registry_is_copied_at_run_start():
    tools = {"t": lambda: 1}

    def model(messages):
        if len(messages) == 1:
            return reply("", call("a", "t"))
        if len(messages) == 3:
            tools.clear()  # 运行中途改外部字典
            return reply("", call("b", "t"))
        return reply("end")

    result = run_agent("q", model, tools)
    assert tool_contents(result) == [{"ok": True, "value": 1}] * 2
