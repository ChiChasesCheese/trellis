"""日志框架的验收测试：四关的行为、失败路径，以及并发下"一条都不能丢"的不变量。

所有断言都只看公开 API（`records`、`lines`、`dropped_count`、`rotation_count`、
`effective_level`），不碰任何下划线属性——学习者换一套内部表示也应该照样通过。
"""

from __future__ import annotations

import importlib
import io
import json
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FrozenClock:
    """固定时钟，测试自己推进；日志时间因此完全可预测。"""

    def __init__(self, start: float = 0.0) -> None:
        from datetime import datetime, timedelta, timezone

        self._base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._delta = timedelta(seconds=start)
        self._timedelta = timedelta

    def __call__(self):
        return self._base + self._delta

    def advance(self, seconds: float) -> None:
        self._delta += self._timedelta(seconds=seconds)


def make_manager(level=None, clock=None):
    """造一个隔离的框架实例——测试之间绝不共享全局状态。"""
    level = impl.LogLevel.INFO if level is None else level
    return impl.LoggerManager(root_level=level, clock=clock or FrozenClock())


# ---------------------------------------------------------------------------
# 第 1 关：级别、记录、多目的地、格式化器
# ---------------------------------------------------------------------------


def test_level_below_threshold_produces_no_record() -> None:
    manager = make_manager(impl.LogLevel.WARNING)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    assert manager.root.info("安静") is False
    assert sink.records == ()
    assert manager.root.warning("响") is True
    assert len(sink.records) == 1


def test_record_carries_level_message_name_and_injected_time() -> None:
    clock = FrozenClock()
    manager = make_manager(impl.LogLevel.DEBUG, clock)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    log.error("崩了")
    clock.advance(60)
    log.info("恢复")
    first, second = sink.records
    assert (first.logger_name, first.level, first.message) == ("svc", impl.LogLevel.ERROR, "崩了")
    assert second.message == "恢复"
    assert (second.created - first.created).total_seconds() == 60.0   # 时间来自注入的时钟
    assert first.thread_name == threading.current_thread().name


def test_context_is_merged_into_the_record() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    manager.get_logger("svc").info("下单", order_id=7, user="alice")
    record = sink.records[0]
    assert record.context["order_id"] == 7
    assert record.context["user"] == "alice"


def test_each_handler_has_its_own_threshold() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    everything = impl.MemoryHandler(level=impl.LogLevel.DEBUG)
    errors_only = impl.MemoryHandler(level=impl.LogLevel.ERROR)
    manager.root.add_handler(everything)
    manager.root.add_handler(errors_only)
    log = manager.get_logger("svc")
    log.debug("细节")
    log.error("出事")
    assert len(everything.records) == 2
    assert [r.message for r in errors_only.records] == ["出事"]


def test_each_handler_has_its_own_formatter() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    text = impl.MemoryHandler(formatter=impl.TextFormatter())
    as_json = impl.MemoryHandler(formatter=impl.JsonFormatter())
    manager.root.add_handler(text)
    manager.root.add_handler(as_json)
    manager.get_logger("svc").warning("磁盘将满", free_mb=12)
    assert "磁盘将满" in text.lines[0] and "free_mb=12" in text.lines[0]
    payload = json.loads(as_json.lines[0])
    assert payload["level"] == "WARNING"
    assert payload["logger"] == "svc"
    assert payload["free_mb"] == 12


def test_json_formatter_fixed_fields_win_over_context() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler(formatter=impl.JsonFormatter())
    manager.root.add_handler(sink)
    manager.get_logger("svc").info("冲突", level="不是级别", message="不是正文")
    payload = json.loads(sink.lines[0])
    assert payload["level"] == "INFO"
    assert payload["message"] == "冲突"


def test_stream_handler_routes_errors_to_the_error_stream() -> None:
    out, err = io.StringIO(), io.StringIO()
    manager = make_manager(impl.LogLevel.DEBUG)
    manager.root.add_handler(impl.StreamHandler(out, error_stream=err))
    log = manager.get_logger("svc")
    log.info("普通")
    log.critical("致命")
    assert "普通" in out.getvalue() and "致命" not in out.getvalue()
    assert "致命" in err.getvalue()


def test_memory_handler_capacity_must_be_positive() -> None:
    with pytest.raises(ValueError):
        impl.MemoryHandler(capacity=0)


def test_memory_handler_is_bounded_and_drops_the_oldest() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler(capacity=3)
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    for i in range(10):
        log.info(f"第{i}条")
    assert len(sink.records) == 3
    assert [r.message for r in sink.records] == ["第7条", "第8条", "第9条"]


def test_handlers_property_is_a_snapshot_not_the_internal_list() -> None:
    manager = make_manager()
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    snapshot = manager.root.handlers
    manager.root.remove_handler(sink)
    assert snapshot == (sink,)
    assert manager.root.handlers == ()


# ---------------------------------------------------------------------------
# 第 2 关：层级、有效级别、传播
# ---------------------------------------------------------------------------


def test_get_logger_is_idempotent_and_creates_missing_ancestors() -> None:
    manager = make_manager()
    deep = manager.get_logger("a.b.c")
    assert manager.get_logger("a.b.c") is deep
    assert manager.logger_count == 3            # a、a.b、a.b.c 都被建了出来
    assert deep.parent is manager.get_logger("a.b")
    assert manager.get_logger("a").parent is manager.root


def test_invalid_dotted_name_is_rejected() -> None:
    manager = make_manager()
    with pytest.raises(impl.InvalidLoggerNameError):
        manager.get_logger("a..b")
    with pytest.raises(impl.LoggingError):
        manager.get_logger(".a")


def test_effective_level_is_inherited_until_someone_sets_one() -> None:
    manager = make_manager(impl.LogLevel.WARNING)
    deep = manager.get_logger("a.b.c")
    assert deep.level is None
    assert deep.effective_level == impl.LogLevel.WARNING
    manager.get_logger("a").level = impl.LogLevel.DEBUG
    assert deep.effective_level == impl.LogLevel.DEBUG
    deep.level = impl.LogLevel.ERROR
    assert deep.effective_level == impl.LogLevel.ERROR


def test_record_reaches_handlers_of_every_ancestor() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    at_root, at_a = impl.MemoryHandler(), impl.MemoryHandler()
    manager.root.add_handler(at_root)
    manager.get_logger("a").add_handler(at_a)
    manager.get_logger("a.b").info("往上走")
    assert len(at_a.records) == 1
    assert len(at_root.records) == 1


def test_ancestor_logger_level_is_not_consulted_during_propagation() -> None:
    """这是最容易记错的一条：级别只在起点判一次，向上走只看各 handler 自己的阈值。"""
    manager = make_manager(impl.LogLevel.DEBUG)
    at_root = impl.MemoryHandler(level=impl.LogLevel.DEBUG)
    manager.root.add_handler(at_root)
    parent = manager.get_logger("a")
    parent.level = impl.LogLevel.CRITICAL       # 父级只肯自己发 CRITICAL
    child = manager.get_logger("a.b")
    child.level = impl.LogLevel.DEBUG
    assert child.debug("我照样到得了根") is True
    assert len(at_root.records) == 1


def test_propagate_false_stops_the_walk_at_that_logger() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    at_root, at_a = impl.MemoryHandler(), impl.MemoryHandler()
    manager.root.add_handler(at_root)
    a = manager.get_logger("a")
    a.add_handler(at_a)
    a.propagate = False
    manager.get_logger("a.b").info("到 a 为止")
    assert len(at_a.records) == 1
    assert at_root.records == ()


def test_bind_adds_context_and_still_reaches_ancestor_handlers() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    request = log.bind(request_id="req-1")
    request.info("开始")
    request.bind(step=2).info("第二步")
    log.info("无关")
    assert sink.records[0].context["request_id"] == "req-1"
    assert sink.records[1].context == {"request_id": "req-1", "step": 2}
    assert sink.records[2].context == {}
    assert request.name == "svc"


def test_bound_view_inherits_the_effective_level() -> None:
    manager = make_manager(impl.LogLevel.WARNING)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    bound = log.bind(request_id="req-2")
    assert bound.info("被拦住") is False
    log.level = impl.LogLevel.INFO
    assert bound.info("现在过得去") is True


# ---------------------------------------------------------------------------
# 第 3 关：线程安全与异步 handler
# ---------------------------------------------------------------------------


def test_synchronous_handler_records_every_line_under_contention() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler(capacity=4000)
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    barrier = threading.Barrier(8)

    def worker(worker_id: int) -> None:
        barrier.wait()
        for i in range(100):
            log.info(f"w{worker_id}-{i}")

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(sink.records) == 800
    assert len({r.message for r in sink.records}) == 800


def test_async_handler_loses_nothing_when_closed_after_a_burst() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler(capacity=4000)
    asynchronous = impl.AsyncHandler(sink, max_queue=16)   # 队列故意比负载小得多
    manager.root.add_handler(asynchronous)
    log = manager.get_logger("svc")
    barrier = threading.Barrier(8)

    def worker(worker_id: int) -> None:
        barrier.wait()
        for i in range(100):
            log.info(f"w{worker_id}-{i}")

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    asynchronous.close()                                    # 排空、汇合、再关内层
    assert asynchronous.dropped_count == 0
    assert len(sink.records) == 800
    assert asynchronous.is_running is False


def test_async_handler_counts_what_it_drops_when_the_queue_is_full() -> None:
    released = threading.Event()

    class BlockingHandler(impl.MemoryHandler):
        def emit(self, line: str, record) -> None:
            released.wait(5)
            super().emit(line, record)

    sink = BlockingHandler(capacity=100)
    asynchronous = impl.AsyncHandler(sink, max_queue=2, drop_when_full=True)
    manager = make_manager(impl.LogLevel.DEBUG)
    manager.root.add_handler(asynchronous)
    log = manager.get_logger("svc")
    for i in range(20):
        log.info(f"第{i}条")
    assert asynchronous.dropped_count >= 17                 # 最多 1 条在工作线程手上 + 2 条在队列里
    released.set()
    asynchronous.close()
    assert len(sink.records) + asynchronous.dropped_count == 20


def test_async_handler_refuses_records_after_close() -> None:
    sink = impl.MemoryHandler()
    asynchronous = impl.AsyncHandler(sink)
    assert asynchronous.handle(impl.LogRecord("svc", impl.LogLevel.INFO, "关闭前", FrozenClock()(), "main")) is True
    asynchronous.close()
    assert asynchronous.handle(impl.LogRecord("svc", impl.LogLevel.INFO, "关闭后", FrozenClock()(), "main")) is False
    assert asynchronous.dropped_count == 1
    assert [r.message for r in sink.records] == ["关闭前"]


def test_a_failing_handler_does_not_kill_the_worker_thread() -> None:
    class ExplodingHandler(impl.MemoryHandler):
        def emit(self, line: str, record) -> None:
            if "毒" in record.message:
                raise OSError("磁盘满了")
            super().emit(line, record)

    sink = ExplodingHandler()
    asynchronous = impl.AsyncHandler(sink)
    manager = make_manager(impl.LogLevel.DEBUG)
    manager.root.add_handler(asynchronous)
    log = manager.get_logger("svc")
    log.info("毒药")
    log.info("后面这条必须还能写出去")
    asynchronous.close()
    assert asynchronous.error_count == 1
    assert [r.message for r in sink.records] == ["后面这条必须还能写出去"]


def test_async_handler_rejects_a_non_positive_queue_size() -> None:
    with pytest.raises(ValueError):
        impl.AsyncHandler(impl.MemoryHandler(), max_queue=0)


# ---------------------------------------------------------------------------
# 第 4 关：滚动文件与过滤器
# ---------------------------------------------------------------------------


def test_rotating_file_handler_rotates_and_keeps_only_backup_count_files(tmp_path) -> None:
    path = tmp_path / "app.log"
    handler = impl.RotatingFileHandler(path, max_bytes=120, backup_count=2, formatter=impl.TextFormatter(template="{message}"))
    manager = make_manager(impl.LogLevel.DEBUG)
    manager.root.add_handler(handler)
    log = manager.get_logger("svc")
    for i in range(40):
        log.info(f"line-{i:03d}-padding-padding")
    handler.close()
    assert handler.rotation_count > 0
    assert len(handler.backup_paths) == 2                   # 不是 3、不是 40
    assert not (tmp_path / "app.log.3").exists()
    assert path.stat().st_size <= 120 + 64


def test_rotating_file_handler_rejects_bad_sizes(tmp_path) -> None:
    with pytest.raises(ValueError):
        impl.RotatingFileHandler(tmp_path / "a.log", max_bytes=0)
    with pytest.raises(ValueError):
        impl.RotatingFileHandler(tmp_path / "a.log", backup_count=-1)


def test_a_filter_is_added_to_a_handler_without_touching_the_logger() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    log = manager.get_logger("svc")
    log.info("健康检查", path="/healthz")
    sink.add_filter(lambda record: record.context.get("path") != "/healthz")
    log.info("健康检查", path="/healthz")
    log.info("真实请求", path="/orders")
    assert [r.message for r in sink.records] == ["健康检查", "真实请求"]
    assert len(sink.filters) == 1


def test_two_filters_both_have_to_agree() -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler()
    manager.root.add_handler(sink)
    sink.add_filter(lambda record: record.context.get("tenant") == "acme")
    sink.add_filter(lambda record: record.level >= impl.LogLevel.WARNING)
    log = manager.get_logger("svc")
    log.info("acme 的 info", tenant="acme")
    log.warning("别家的 warning", tenant="other")
    log.warning("acme 的 warning", tenant="acme")
    assert [r.message for r in sink.records] == ["acme 的 warning"]


def test_manager_close_closes_every_handler_in_the_tree(tmp_path) -> None:
    manager = make_manager(impl.LogLevel.DEBUG)
    sink = impl.MemoryHandler(capacity=10)
    asynchronous = impl.AsyncHandler(sink)
    manager.get_logger("a.b").add_handler(asynchronous)
    manager.get_logger("a.b").info("最后一条")
    manager.close()
    assert asynchronous.is_running is False
    assert [r.message for r in sink.records] == ["最后一条"]
