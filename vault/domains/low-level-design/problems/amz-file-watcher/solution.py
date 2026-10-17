"""文件监听器（File Watcher）参考解。

设计五句话：
1. 监听 = 反复「拍快照 + 比对」：快照是 `路径 -> Stat(mtime_ns, size)` 的字典，比对是一个纯函数 `diff`，产出 CREATED / MODIFIED / DELETED 事件。
2. 读磁盘被藏在 `FileSystem` 协议后面（只有一个方法 `scan`）：真实实现 `DiskFileSystem` 用 os.scandir，测试换成内存里的假实现，不碰真实磁盘和真实时间。
3. `Watcher.poll()` 是唯一的推进动作：谁调用（手动、后台线程）都一样，所以几乎所有行为都能不开线程地测。
4. 去抖（debounce）不用时钟：一个路径的变化必须在连续两次轮询里「看到同一个状态」才算数，写到一半的文件不会报半截事件。
5. 订阅者在轮询线程上被回调，但永远在锁外；一个回调抛异常只被记录、不影响别人；`stop()` 靠 `threading.Event`，在回调里调用也不会死锁。
"""

from __future__ import annotations

import os
import threading
from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class WatchError(Exception):
    """本模块所有异常的根。"""


class RootNotFoundError(WatchError, FileNotFoundError):
    """被监听的根目录不存在。"""


@dataclass(frozen=True, slots=True)
class Stat:
    """一个文件在某一刻的指纹。只用 mtime 会漏掉同一时间粒度内的第二次修改，所以再加 size。"""

    mtime_ns: int
    size: int


Snapshot = dict[str, Stat]  # 相对根目录、用 "/" 分隔的路径 -> 指纹


class EventKind(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"


@dataclass(frozen=True, slots=True)
class Event:
    """发生了什么：订阅者只靠它就能更新自己。"""

    kind: EventKind
    path: str


class FileSystem(Protocol):
    """监听器需要从文件系统得到的唯一能力：给我这个目录下所有文件的指纹。"""

    def scan(self, root: str, recursive: bool) -> Snapshot: ...


class DiskFileSystem:
    """真实磁盘：os.scandir 遍历，不跟随符号链接（避免目录环），遍历中途消失的文件直接跳过。"""

    def scan(self, root: str, recursive: bool) -> Snapshot:
        if not os.path.isdir(root):
            raise RootNotFoundError(root)
        found: Snapshot = {}
        pending = [""]
        while pending:
            rel_dir = pending.pop()
            try:
                entries = list(os.scandir(os.path.join(root, rel_dir)))
            except FileNotFoundError:  # 目录在遍历途中被删了
                continue
            for entry in entries:
                rel = f"{rel_dir}/{entry.name}" if rel_dir else entry.name
                try:
                    if entry.is_dir(follow_symlinks=False):
                        if recursive:
                            pending.append(rel)
                    elif entry.is_file(follow_symlinks=False):
                        st = entry.stat(follow_symlinks=False)
                        found[rel] = Stat(st.st_mtime_ns, st.st_size)
                except FileNotFoundError:  # 文件在 scandir 与 stat 之间消失
                    continue
        return found


def diff(old: Snapshot, new: Snapshot) -> list[Event]:
    """两张快照的差：新增、变化、消失。按路径排序，结果是确定的。"""
    events = [Event(EventKind.CREATED, p) for p in new.keys() - old.keys()]
    events += [Event(EventKind.DELETED, p) for p in old.keys() - new.keys()]
    events += [Event(EventKind.MODIFIED, p) for p in old.keys() & new.keys() if old[p] != new[p]]
    return sorted(events, key=lambda e: (e.path, e.kind.value))


Callback = Callable[[Event], None]


@dataclass(frozen=True, slots=True)
class CallbackFailure:
    """一次回调失败的记录：哪个事件、什么异常。"""

    event: Event
    error: Exception


class Watcher:
    """监听一个目录。`poll()` 推进一次；`start()` 再开一条后台线程按间隔反复调用它。"""

    def __init__(
        self,
        fs: FileSystem,
        root: str,
        *,
        recursive: bool = True,
        include: Callable[[str], bool] = lambda path: True,
        settle: bool = False,
    ) -> None:
        self._fs, self._root, self._recursive = fs, root, recursive
        self._include = include
        self._settle = settle
        self._committed: Snapshot | None = None  # 订阅者已经知道的世界；None = 还没拍过基线
        self._last: Snapshot = {}  # 上一次轮询看到的原始世界，去抖用
        self._subs: dict[int, tuple[Callback, frozenset[EventKind] | None]] = {}
        self._next_sub = 0
        self._failures: deque[CallbackFailure] = deque(maxlen=100)
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    # ---- 订阅 ----
    def subscribe(self, callback: Callback, kinds: Iterable[EventKind] | None = None) -> Callable[[], None]:
        """登记回调；返回一个取消订阅的函数。kinds 为 None 表示三种事件都要。"""
        with self._lock:
            token = self._next_sub
            self._next_sub += 1
            self._subs[token] = (callback, None if kinds is None else frozenset(kinds))

        def unsubscribe() -> None:
            with self._lock:
                self._subs.pop(token, None)

        return unsubscribe

    @property
    def failures(self) -> tuple[CallbackFailure, ...]:
        with self._lock:
            return tuple(self._failures)

    @property
    def running(self) -> bool:
        thread = self._thread
        return thread is not None and thread.is_alive()

    # ---- 推进 ----
    def poll(self) -> list[Event]:
        """拍一次快照，和已提交的世界比对，把事件交给订阅者，并返回这些事件。

        第一次调用只建立基线（监听开始前就存在的文件不算「新建」），返回空列表。"""
        raw = {p: s for p, s in self._fs.scan(self._root, self._recursive).items() if self._include(p)}
        with self._lock:
            if self._committed is None:
                self._committed, self._last = raw, raw
                return []
            view = self._settled_view(raw) if self._settle else raw
            events = diff(self._committed, view)
            self._committed, self._last = view, raw
            targets = list(self._subs.values())
        self._dispatch(events, targets)
        return events

    def _settled_view(self, raw: Snapshot) -> Snapshot:
        """一个路径的状态只有在连续两次轮询里相同才被采纳；否则沿用订阅者已知的旧状态。"""
        assert self._committed is not None
        view: Snapshot = {}
        for path in raw.keys() | self._committed.keys():
            now = raw.get(path)
            state = now if now == self._last.get(path) else self._committed.get(path)
            if state is not None:
                view[path] = state
        return view

    def _dispatch(self, events: list[Event], targets: list[tuple[Callback, frozenset[EventKind] | None]]) -> None:
        """在锁外调用回调：回调里可以订阅、取消订阅甚至 stop() 而不死锁；一个回调出错不影响别人。"""
        for event in events:
            for callback, kinds in targets:
                if kinds is not None and event.kind not in kinds:
                    continue
                try:
                    callback(event)
                except Exception as exc:
                    with self._lock:
                        self._failures.append(CallbackFailure(event, exc))

    # ---- 后台线程 ----
    def start(self, interval: float) -> None:
        """开一条守护线程，每隔 interval 秒 poll() 一次；已在运行则忽略。"""
        with self._lock:
            if self.running:
                return
            self._stop.clear()
            self._thread = threading.Thread(target=self._loop, args=(interval,), name="file-watcher", daemon=True)
            self._thread.start()

    def _loop(self, interval: float) -> None:
        while not self._stop.is_set():
            try:
                self.poll()
            except OSError:  # 根目录暂时不见等：这一轮跳过，下一轮再试
                pass
            if self._stop.wait(interval):
                return

    def stop(self, timeout: float | None = 5.0) -> None:
        """请求停止并等待线程退出。在回调（即轮询线程自己）里调用时不 join，否则会等自己。"""
        self._stop.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout)


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        watcher = Watcher(DiskFileSystem(), tmp)
        watcher.subscribe(print)
        watcher.poll()  # 基线
        with open(os.path.join(tmp, "a.txt"), "w") as f:
            f.write("hello")
        watcher.poll()
