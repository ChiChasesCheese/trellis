"""DAG 执行器：依赖安装顺序 -> 带结果传递的步骤执行 -> 线程池并行与失败传播。

设计五行：
1. `Graph` 是不可变的依赖图：只负责去重边、拓扑序、找环、求后代，不知道"执行"。
2. `install_order` 是第 1 关的纯函数；环用 `CycleError` 报出具体的环（a -> b -> a）。
3. `Workflow` 持有 `Step`（函数 + 依赖），按拓扑序执行，把依赖的结果当作入参传给下游（第 3 关）。
4. `run_parallel` 由调用线程独占调度状态，worker 线程只跑 `fn`；一个步骤失败只让它的后代 SKIPPED（第 4 关）。
5. 顺序全部确定：同一时刻可执行的节点按"首次出现"的先后排，测试不依赖线程时序。
"""
from __future__ import annotations

import heapq
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from typing import Any


class DagError(Exception):
    """本模块所有失败的基类。"""


class CycleError(DagError):
    """依赖里有环。`cycle` 按"前一个依赖后一个"的顺序给出，最后一个再依赖第一个。"""

    def __init__(self, cycle: tuple[str, ...]) -> None:
        self.cycle = cycle
        super().__init__(" -> ".join((*cycle, cycle[0])))


class DuplicateStepError(DagError):
    """同名步骤被重复登记。"""


class StepError(DagError):
    """顺序执行时某一步抛了异常；`step` 是出错的步骤名，原始异常在 `__cause__`。"""

    def __init__(self, step: str) -> None:
        self.step = step
        super().__init__(f"step {step!r} failed")


class Graph:
    """依赖图。`deps[x]` 是 x 的前置依赖（必须先于 x）；只出现在依赖里的名字也算节点。"""

    def __init__(self, deps: Mapping[str, Iterable[str]]) -> None:
        index: dict[str, int] = {}  # 名字 -> 首次出现的序号，用来稳定地排序
        prereqs: dict[str, set[str]] = {}
        for node, ds in deps.items():
            index.setdefault(node, len(index))
            prereqs.setdefault(node, set())
            for d in ds:
                index.setdefault(d, len(index))
                prereqs.setdefault(d, set())
                prereqs[node].add(d)  # set：重复声明同一条依赖只算一条边
        self._index = index
        self._prereqs = prereqs
        self._dependents: dict[str, set[str]] = {n: set() for n in index}
        for node, ds in prereqs.items():
            for d in ds:
                self._dependents[d].add(node)

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(self._index)

    def prerequisites(self, node: str) -> tuple[str, ...]:
        return tuple(sorted(self._prereqs[node], key=self._index.__getitem__))

    def descendants(self, node: str) -> frozenset[str]:
        """所有直接或间接依赖 node 的节点（不含自己）。"""
        seen: set[str] = set()
        stack = [node]
        while stack:
            for nxt in self._dependents[stack.pop()]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return frozenset(seen)

    def order(self) -> list[str]:
        """Kahn 算法。有环抛 CycleError。同时可选的节点按首次出现的先后。"""
        waiting = {n: len(p) for n, p in self._prereqs.items()}  # 入度按去重后的边数
        ready = [self._index[n] for n, c in waiting.items() if c == 0]
        heapq.heapify(ready)
        names = self.nodes
        out: list[str] = []
        while ready:
            node = names[heapq.heappop(ready)]
            out.append(node)
            for nxt in self._dependents[node]:
                waiting[nxt] -= 1
                if waiting[nxt] == 0:
                    heapq.heappush(ready, self._index[nxt])
        if len(out) != len(names):  # 没排完 = 剩下的里一定有环
            stuck = {n for n, c in waiting.items() if c > 0}
            raise CycleError(self._find_cycle(stuck))
        return out

    def _find_cycle(self, stuck: set[str]) -> tuple[str, ...]:
        """stuck 里的每个节点至少还有一个 stuck 前置依赖：沿它一直走，必然撞上走过的点。"""
        node = min(stuck, key=self._index.__getitem__)
        path: list[str] = []
        pos: dict[str, int] = {}
        while node not in pos:
            pos[node] = len(path)
            path.append(node)
            node = next(d for d in self.prerequisites(node) if d in stuck)
        return tuple(path[pos[node]:])


def install_order(deps: Mapping[str, Iterable[str]]) -> list[str]:
    """第 1 关：返回一个合法安装顺序；有环抛 CycleError。"""
    return Graph(deps).order()


@dataclass(frozen=True, slots=True)
class Step:
    name: str
    fn: Callable[[dict[str, Any]], Any]  # 入参：{依赖名: 依赖的结果}
    needs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RunReport:
    """一次并行运行的结局：每个步骤恰好在 results / failed / skipped 之一。"""

    results: Mapping[str, Any] = field(default_factory=dict)
    failed: Mapping[str, BaseException] = field(default_factory=dict)
    skipped: frozenset[str] = frozenset()

    @property
    def ok(self) -> bool:
        return not self.failed


class Workflow:
    """步骤集合。登记时不检查环，运行前由 Graph 统一检查。"""

    def __init__(self) -> None:
        self._steps: dict[str, Step] = {}

    def add(self, name: str, fn: Callable[[dict[str, Any]], Any], needs: Iterable[str] = ()) -> None:
        if name in self._steps:
            raise DuplicateStepError(name)
        self._steps[name] = Step(name, fn, tuple(needs))

    def _graph(self) -> Graph:
        graph = Graph({s.name: s.needs for s in self._steps.values()})
        missing = [n for n in graph.nodes if n not in self._steps]
        if missing:
            raise KeyError(f"unknown step(s): {', '.join(missing)}")
        return graph

    def order(self) -> list[str]:
        return self._graph().order()

    def run(self) -> dict[str, Any]:
        """第 3 关：按拓扑序顺序执行，依赖的结果传给下游；任一步失败就停（fail-fast）。"""
        results: dict[str, Any] = {}
        for name in self._graph().order():
            step = self._steps[name]
            try:
                results[name] = step.fn({d: results[d] for d in step.needs})
            except Exception as exc:
                raise StepError(name) from exc
        return results

    def run_parallel(self, max_workers: int = 4) -> RunReport:
        """第 4 关：互不依赖的步骤同时跑；失败只让后代 SKIPPED，别的分支照常完成。"""
        graph = self._graph()
        order = graph.order()  # 先检查环：有环直接抛，不启动任何线程
        waiting = {n: len(graph.prerequisites(n)) for n in order}
        results: dict[str, Any] = {}
        failed: dict[str, BaseException] = {}
        skipped: set[str] = set()
        running: dict[Future[Any], str] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            def submit(name: str) -> None:
                step = self._steps[name]
                inputs = {d: results[d] for d in step.needs}  # 此刻依赖都已完成，快照入参
                running[pool.submit(step.fn, inputs)] = name

            for name in order:
                if waiting[name] == 0:
                    submit(name)
            while running:
                done, _ = wait(running, return_when=FIRST_COMPLETED)
                for fut in sorted(done, key=lambda f: order.index(running[f])):
                    name = running.pop(fut)
                    exc = fut.exception()
                    if exc is not None:
                        failed[name] = exc
                        skipped |= graph.descendants(name)
                        continue
                    results[name] = fut.result()
                    for nxt in sorted(graph._dependents[name], key=order.index):
                        waiting[nxt] -= 1
                        if waiting[nxt] == 0 and nxt not in skipped:
                            submit(nxt)
        return RunReport(results, failed, frozenset(skipped))


if __name__ == "__main__":
    print(install_order({"app": ["web", "db"], "web": ["lib"], "db": ["lib"]}))
    try:
        install_order({"a": ["b"], "b": ["c"], "c": ["a"]})
    except CycleError as err:
        print("cycle:", err)
