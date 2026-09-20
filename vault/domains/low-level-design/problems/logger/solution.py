"""日志框架：分级过滤、多目的地、层级传播与异步写入。
设计：`Logger` 只决定"这条要不要记、交给谁"，`BaseHandler` 决定"写到哪"，`Formatter` 决定
"长什么样"，三者各自独立变化；`LogRecord`（冻结 dataclass）是它们之间唯一的事件对象。
`Logger` 按点分名字组成一棵树，记录沿祖先链向上交给沿途每一个 handler，级别可向上继承。
`AsyncHandler` 是包在任意 handler 外面的一层队列加工作线程，关闭时排空、汇合、再关内层。
"""

from __future__ import annotations

import json
import queue
import threading
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from types import MappingProxyType
from typing import Protocol, TextIO

# 时钟从外部注入（测试里换成固定时钟）；过滤器就是一个"看一眼记录、回答要不要"的函数——
# 只有一个方法的策略不值得一个类。
Clock = Callable[[], datetime]
Filter = Callable[["LogRecord"], bool]
EMPTY_CONTEXT: Mapping[str, object] = MappingProxyType({})


def utc_now() -> datetime:
    """默认时钟。带时区，避免日志时间在跨时区机器上无法比较。"""
    return datetime.now(timezone.utc)


class LoggingError(Exception):
    """本框架所有失败的共同基类，调用方可以只捕获这一个。"""


class InvalidLoggerNameError(LoggingError, ValueError):
    """点分名字不合法（空段、首尾有点）时抛出。"""


class LogLevel(IntEnum):
    """级别之间要能比大小，所以是 `IntEnum` 而不是 `Enum`；数值留出间隔以便日后插入新级别。

    这里**故意没有** `NOTSET = 0`：标准库用 0 同时表示"没设过"和一个级别值，本框架用
    `level=None` 表示"向上继承"，见题解"关键设计决策"。
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass(frozen=True, slots=True)
class LogRecord:
    """一次日志事件的完整快照：冻结，因此可以安全地交给任意多个 handler、跨线程传递。

    观察者模式里"事件对象携带发生了什么"的直接体现——handler 永远不需要回头去问 `Logger`
    任何事，也就不需要和 `Logger` 争同一把锁。
    """

    logger_name: str
    level: LogLevel
    message: str
    created: datetime
    thread_name: str
    context: Mapping[str, object] = field(default_factory=lambda: EMPTY_CONTEXT)


class Formatter(Protocol):
    """格式化器只有一个职责：把记录变成一行字符串。它带配置（模板、时间格式），所以是类。"""

    def format(self, record: LogRecord) -> str: ...


@dataclass(frozen=True, slots=True)
class TextFormatter:
    """人读的一行文本。模板用 `str.format` 的占位符，可用字段见 `format` 的实现。"""

    template: str = "{time} [{level}] {name}: {message}{context}"
    time_format: str = "%Y-%m-%d %H:%M:%S"

    def format(self, record: LogRecord) -> str:
        context = ""
        if record.context:
            context = " " + " ".join(f"{k}={v!r}" for k, v in sorted(record.context.items()))
        return self.template.format(
            time=record.created.strftime(self.time_format),
            level=record.level.name,
            name=record.logger_name or "root",
            message=record.message,
            context=context,
            thread=record.thread_name,
        )


@dataclass(frozen=True, slots=True)
class JsonFormatter:
    """机器读的一行 JSON。上下文被摊平到顶层，但固定字段后写，保证不会被上下文顶掉。"""

    time_format: str = "%Y-%m-%dT%H:%M:%S%z"

    def format(self, record: LogRecord) -> str:
        payload: dict[str, object] = {
            **record.context,
            "time": record.created.strftime(self.time_format),
            "level": record.level.name,
            "logger": record.logger_name,
            "message": record.message,
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)


class Handler(Protocol):
    """`Logger` 眼里的 handler 只有这三个方法——`AsyncHandler` 正是靠只实现这个协议、
    而不继承 `BaseHandler`，才能把任意 handler 包起来。"""

    def handle(self, record: LogRecord) -> bool: ...

    def flush(self) -> None: ...

    def close(self) -> None: ...


class BaseHandler(ABC):
    """同步 handler 的公共骨架：自己的阈值、自己的格式化器、自己的过滤器、自己的一把锁。

    `handle` 是模板方法，子类只实现 `emit`。格式化放在锁**外面**（记录是冻结的，纯计算），
    只有真正写出去的那一步在锁内——锁保护的是"一行不被另一行插进来"，不是 CPU 时间。
    """

    def __init__(self, level: LogLevel = LogLevel.DEBUG, formatter: Formatter | None = None) -> None:
        self.level = level
        self.formatter: Formatter = formatter if formatter is not None else TextFormatter()
        self._filters: tuple[Filter, ...] = ()
        self._lock = threading.RLock()

    @property
    def filters(self) -> tuple[Filter, ...]:
        """快照。内部用元组存，读的时候不用加锁，也不可能被调用方改坏。"""
        return self._filters

    def add_filter(self, predicate: Filter) -> None:
        """加一个过滤器：整体换掉元组，读者要么看到旧的、要么看到新的，不会看到半个。"""
        with self._lock:
            self._filters = (*self._filters, predicate)

    def handle(self, record: LogRecord) -> bool:
        """返回这条记录是否真的被写出去了——测试据此断言阈值和过滤器生效。"""
        if record.level < self.level:
            return False
        if not all(predicate(record) for predicate in self._filters):
            return False
        line = self.formatter.format(record)
        with self._lock:
            self.emit(line, record)
        return True

    @abstractmethod
    def emit(self, line: str, record: LogRecord) -> None:
        """把格式化好的一行写出去。调用时已持有本 handler 的锁。

        同时收下 `record`，是为了让子类能按级别分流（比如 ERROR 走 stderr）而不必把自己
        刚生成的那行字符串再解析回来——那种写法一换成 JSON 格式化器就悄悄失效了。
        """

    def flush(self) -> None:
        """默认无事可做；有缓冲的子类覆盖它。"""

    def close(self) -> None:
        self.flush()


class StreamHandler(BaseHandler):
    """写到任意文本流。`error_stream` 非空时，达到 `split_at` 的记录改走它（典型是 stderr）。"""

    def __init__(self, stream: TextIO, level: LogLevel = LogLevel.DEBUG, formatter: Formatter | None = None,
                 error_stream: TextIO | None = None, split_at: LogLevel = LogLevel.ERROR) -> None:
        super().__init__(level, formatter)
        self._stream = stream
        self._error_stream = error_stream
        self._split_at = split_at

    def emit(self, line: str, record: LogRecord) -> None:
        target = self._error_stream if (self._error_stream is not None and record.level >= self._split_at) else self._stream
        target.write(line + "\n")

    def flush(self) -> None:
        with self._lock:
            self._stream.flush()
            if self._error_stream is not None:
                self._error_stream.flush()


class MemoryHandler(BaseHandler):
    """把记录留在内存里，给测试和"最近 N 条"面板用。**有上限**：这是一个日志组件，
    任何一个会随运行时间无界增长的容器都是事故。超出容量时丢最旧的。"""

    def __init__(self, capacity: int = 256, level: LogLevel = LogLevel.DEBUG, formatter: Formatter | None = None) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        super().__init__(level, formatter)
        self._capacity = capacity
        self._records: list[LogRecord] = []
        self._lines: list[str] = []

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def records(self) -> tuple[LogRecord, ...]:
        """快照，不是内部列表本身——调用方拿到手的东西不该能改写 handler 的状态。"""
        with self._lock:
            return tuple(self._records)

    @property
    def lines(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._lines)

    def emit(self, line: str, record: LogRecord) -> None:
        self._records.append(record)
        self._lines.append(line)
        if len(self._records) > self._capacity:
            del self._records[0]
            del self._lines[0]


class RotatingFileHandler(BaseHandler):
    """按字节数滚动的文件 handler：写满 `max_bytes` 就把 `app.log` 改名成 `app.log.1`，
    旧的依次后移，超过 `backup_count` 的直接删掉——否则"滚动"只是把磁盘填满得慢一点。"""

    def __init__(self, path: Path | str, max_bytes: int = 1024, backup_count: int = 3,
                 level: LogLevel = LogLevel.DEBUG, formatter: Formatter | None = None,
                 encoding: str = "utf-8") -> None:
        if max_bytes <= 0:
            raise ValueError(f"max_bytes must be positive, got {max_bytes}")
        if backup_count < 0:
            raise ValueError(f"backup_count must not be negative, got {backup_count}")
        super().__init__(level, formatter)
        self._path = Path(path)
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._encoding = encoding
        self._size = self._path.stat().st_size if self._path.exists() else 0
        self._stream: TextIO | None = self._path.open("a", encoding=encoding)
        self._rotations = 0

    @property
    def path(self) -> Path:
        return self._path

    @property
    def rotation_count(self) -> int:
        """已经滚动过多少次——把"到底有没有滚"变成一个可以断言的公开状态。"""
        return self._rotations

    @property
    def backup_paths(self) -> tuple[Path, ...]:
        """当前磁盘上真实存在的备份文件，从最新到最旧。"""
        candidates = (Path(f"{self._path}.{i}") for i in range(1, self._backup_count + 1))
        return tuple(p for p in candidates if p.exists())

    def emit(self, line: str, record: LogRecord) -> None:
        data = line + "\n"
        size = len(data.encode(self._encoding))
        if self._size > 0 and self._size + size > self._max_bytes:
            self._rotate()
        assert self._stream is not None
        self._stream.write(data)
        self._stream.flush()
        self._size += size

    def _rotate(self) -> None:
        """把 .{n} 依次改名成 .{n+1}，最旧的一个删掉，再把当前文件变成 .1 并重开。"""
        if self._stream is not None:
            self._stream.close()
            self._stream = None
        if self._backup_count == 0:
            self._path.unlink(missing_ok=True)
        else:
            for i in range(self._backup_count - 1, 0, -1):
                src, dst = Path(f"{self._path}.{i}"), Path(f"{self._path}.{i + 1}")
                if src.exists():
                    dst.unlink(missing_ok=True)
                    src.rename(dst)
            first = Path(f"{self._path}.1")
            first.unlink(missing_ok=True)
            self._path.rename(first)
        self._stream = self._path.open("a", encoding=self._encoding)
        self._size = 0
        self._rotations += 1

    def flush(self) -> None:
        with self._lock:
            if self._stream is not None:
                self._stream.flush()

    def close(self) -> None:
        with self._lock:
            if self._stream is not None:
                self._stream.close()
                self._stream = None


class AsyncHandler:
    """把任意 handler 变成异步的一层装饰：一条有界队列 + 一个工作线程。

    它只实现 `Handler` 协议、不继承 `BaseHandler`——因为它没有自己的格式化器和阈值，
    这两件事属于被包住的那个 handler。队列满时的行为是一个必须当场讲清楚的取舍：
    默认阻塞（业务线程变慢，但一条不丢），`drop_when_full=True` 则丢弃并计数
    （业务线程不受影响，代价是日志出现无声的空洞——所以必须有 `dropped_count` 可观测）。

    关闭契约：`close()` 保证在它之前**已经入队**的记录全部写出（排空、汇合、再关内层），
    之后再来的记录一律拒收并计入 `dropped_count`；它不承诺和仍在运行的生产者线程赛跑。
    """

    def __init__(self, target: Handler, max_queue: int = 1024, drop_when_full: bool = False, name: str = "log-worker") -> None:
        if max_queue <= 0:
            raise ValueError(f"max_queue must be positive, got {max_queue}")
        self._target = target
        self._queue: queue.Queue[LogRecord | None] = queue.Queue(maxsize=max_queue)
        self._drop_when_full = drop_when_full
        self._dropped = 0
        self._errors = 0
        self._closed = False
        self._state_lock = threading.RLock()
        self._worker = threading.Thread(target=self._run, name=name, daemon=True)
        self._worker.start()

    @property
    def dropped_count(self) -> int:
        with self._state_lock:
            return self._dropped

    @property
    def error_count(self) -> int:
        """内层 handler 抛出异常的次数。写日志失败绝不能杀掉业务线程，但也不能静悄悄。"""
        with self._state_lock:
            return self._errors

    @property
    def pending(self) -> int:
        return self._queue.qsize()

    @property
    def is_running(self) -> bool:
        return self._worker.is_alive()

    def handle(self, record: LogRecord) -> bool:
        """入队即返回。整段放在 `_state_lock` 里，是为了让"关闭"和"入队"不会交错：
        要么这条记录已经排在哨兵之前，要么它被明确拒收，不存在"入了队却没人消费"。"""
        with self._state_lock:
            if self._closed:
                self._dropped += 1
                return False
            if self._drop_when_full:
                try:
                    self._queue.put_nowait(record)
                except queue.Full:
                    self._dropped += 1
                    return False
            else:
                self._queue.put(record)
            return True

    def _run(self) -> None:
        while True:
            record = self._queue.get()
            try:
                if record is None:
                    return
                self._target.handle(record)
            except Exception:
                with self._state_lock:
                    self._errors += 1
            finally:
                self._queue.task_done()

    def flush(self) -> None:
        """等队列里已有的记录全部被消费，再让内层把缓冲刷出去。"""
        self._queue.join()
        self._target.flush()

    def close(self) -> None:
        with self._state_lock:
            if self._closed:
                return
            self._closed = True
            self._queue.put(None)
        self._worker.join()
        self._target.close()


class Logger:
    """一个命名的日志入口。职责只有两件：按有效级别决定要不要造记录；把记录沿祖先链分发。

    `level=None` 表示"我没有意见，问我的祖先"；根 logger 必须有具体级别，递归才有底。
    `handlers` 用元组存，`add_handler` 整体替换——于是分发路径上一把锁都不用加。
    """

    def __init__(self, name: str, parent: Logger | None = None, level: LogLevel | None = None,
                 clock: Clock = utc_now, context: Mapping[str, object] | None = None) -> None:
        self._name = name
        self._parent = parent
        self.level = level
        self.propagate = True
        self._clock = clock
        self._context: Mapping[str, object] = MappingProxyType(dict(context or {}))
        self._handlers: tuple[Handler, ...] = ()
        self._lock = threading.RLock()

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Logger | None:
        return self._parent

    @property
    def context(self) -> Mapping[str, object]:
        """只读视图：绑定上的上下文谁都能看，但谁都改不了。"""
        return self._context

    @property
    def handlers(self) -> tuple[Handler, ...]:
        return self._handlers

    @property
    def effective_level(self) -> LogLevel:
        """自己没设级别就一路问祖先。这是整棵树里唯一一处"继承"，也是配置只需写在根上的原因。"""
        node: Logger | None = self
        while node is not None:
            if node.level is not None:
                return node.level
            node = node._parent
        return LogLevel.WARNING

    def add_handler(self, handler: Handler) -> None:
        with self._lock:
            if handler not in self._handlers:
                self._handlers = (*self._handlers, handler)

    def remove_handler(self, handler: Handler) -> None:
        with self._lock:
            self._handlers = tuple(h for h in self._handlers if h is not handler)

    def bind(self, /, **context: object) -> Logger:
        """返回一个带额外上下文的视图：它以本 logger 为父、自己不挂 handler，
        于是记录照样流经本 logger 和所有祖先的 handler，级别也照样继承。
        不需要为"绑定"再发明一个类——树和传播机制已经把这件事做完了。"""
        merged = {**self._context, **context}
        view = Logger(self._name, parent=self, clock=self._clock, context=merged)
        return view

    def is_enabled_for(self, level: LogLevel) -> bool:
        """廉价闸门：一次整数比较。被关掉的 DEBUG 调用不该产生任何对象。"""
        return level >= self.effective_level

    def log(self, level: LogLevel, message: str, /, **context: object) -> bool:
        """返回这条记录是否至少被一个 handler 写出去了，方便测试和自检。

        `/` 把 `level` 和 `message` 声明为仅位置参数：否则调用方想记一个名叫 `message`
        或 `level` 的业务字段（`log.info("冲突", level="P1")`）就会和形参撞名报 TypeError。
        凡是尾随 `**kwargs` 收用户数据的 API，前面的形参都应该是仅位置的。
        """
        if not self.is_enabled_for(level):
            return False
        record = LogRecord(
            logger_name=self._name,
            level=level,
            message=message,
            created=self._clock(),
            thread_name=threading.current_thread().name,
            context=MappingProxyType({**self._context, **context}),
        )
        return self._dispatch(record) > 0

    def _dispatch(self, record: LogRecord) -> int:
        """沿祖先链向上，把记录交给沿途每一个 handler。

        关键且常被记错的一点：**向上走时不再看祖先 logger 的级别**，只看各个 handler
        自己的阈值。级别只在起点那一次 `is_enabled_for` 里起作用。标准库 `logging`
        的 `callHandlers` 就是这个语义，本框架与它一致。
        """
        delivered = 0
        node: Logger | None = self
        while node is not None:
            for handler in node.handlers:
                if handler.handle(record):
                    delivered += 1
            if not node.propagate:
                break
            node = node._parent
        return delivered

    def debug(self, message: str, /, **context: object) -> bool:
        return self.log(LogLevel.DEBUG, message, **context)

    def info(self, message: str, /, **context: object) -> bool:
        return self.log(LogLevel.INFO, message, **context)

    def warning(self, message: str, /, **context: object) -> bool:
        return self.log(LogLevel.WARNING, message, **context)

    def error(self, message: str, /, **context: object) -> bool:
        return self.log(LogLevel.ERROR, message, **context)

    def critical(self, message: str, /, **context: object) -> bool:
        return self.log(LogLevel.CRITICAL, message, **context)

    def __repr__(self) -> str:
        return f"Logger({self._name!r}, level={self.level}, effective={self.effective_level.name})"


class LoggerManager:
    """按名字登记 logger，并把点分名字接成一棵树。

    不是用 `__new__` 做的单例——那种写法把"全局只要一个"和"这个类本身"焊死，测试再也
    拿不到干净的实例。这里 `LoggerManager` 是一个普通类，模块底部放一个默认实例，
    需要隔离的场合（测试、插件）各自 `LoggerManager()` 一个就是了。
    """

    def __init__(self, root_level: LogLevel = LogLevel.WARNING, clock: Clock = utc_now) -> None:
        self._clock = clock
        self._root = Logger("", parent=None, level=root_level, clock=clock)
        self._loggers: dict[str, Logger] = {}
        self._lock = threading.RLock()

    @property
    def root(self) -> Logger:
        return self._root

    @property
    def logger_count(self) -> int:
        """已登记的具名 logger 个数（不含根）——用来断言中间祖先确实被补齐了。"""
        with self._lock:
            return len(self._loggers)

    def get_logger(self, name: str = "") -> Logger:
        """同名永远返回同一个对象；缺失的中间祖先按需补齐，这样 `a.b.c` 一定挂在 `a.b` 下面。"""
        if name == "":
            return self._root
        if name.startswith(".") or name.endswith(".") or ".." in name:
            raise InvalidLoggerNameError(f"invalid logger name: {name!r}")
        with self._lock:
            existing = self._loggers.get(name)
            if existing is not None:
                return existing
            parent = self._root
            path: list[str] = []
            for part in name.split("."):
                path.append(part)
                key = ".".join(path)
                node = self._loggers.get(key)
                if node is None:
                    node = Logger(key, parent=parent, clock=self._clock)
                    self._loggers[key] = node
                parent = node
            return parent

    def close(self) -> None:
        """进程退出前调用：关掉每一个 handler（异步的那些会在这里排空并汇合）。"""
        with self._lock:
            nodes = [self._root, *self._loggers.values()]
        for node in nodes:
            for handler in node.handlers:
                handler.close()


_DEFAULT_MANAGER: LoggerManager | None = None
_DEFAULT_LOCK = threading.Lock()


def default_manager() -> LoggerManager:
    """进程级默认实例，第一次用到时才建。模块级的一个对象就是 Python 的单例写法——
    比 `__new__` 单例简单，也不在 import 阶段做事。"""
    global _DEFAULT_MANAGER
    with _DEFAULT_LOCK:
        if _DEFAULT_MANAGER is None:
            _DEFAULT_MANAGER = LoggerManager()
        return _DEFAULT_MANAGER


def get_logger(name: str = "") -> Logger:
    """默认入口。需要隔离（测试、插件）就自己造一个 `LoggerManager`，不要来动这个。"""
    return default_manager().get_logger(name)


def _demo() -> None:
    import sys

    manager = LoggerManager(root_level=LogLevel.INFO)
    audit = MemoryHandler(capacity=64, level=LogLevel.ERROR, formatter=JsonFormatter())
    manager.root.add_handler(StreamHandler(sys.stdout, level=LogLevel.INFO))
    app, db = manager.get_logger("app"), manager.get_logger("app.db")
    db.add_handler(audit)
    db.level = LogLevel.DEBUG
    app.info("服务启动", version="1.4.2")
    db.debug("连接池预热", size=8)          # app.db 自己放行 DEBUG，级别不看祖先
    db.error("查询超时", query_ms=1200)     # 同时进 console（继承自根）和 audit
    app.bind(request_id="req-8814").error("上游 504")   # 上下文自动带上，不必逐层传参
    print("audit:", audit.lines[-1])


if __name__ == "__main__":
    _demo()
