"""DAG 执行器（学习者版）：补全每个方法体，接口与 solution.py 完全一致。"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
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
    """顺序执行时某一步抛了异常；`step` 是出错的步骤名。"""

    def __init__(self, step: str) -> None:
        self.step = step
        super().__init__(f"step {step!r} failed")


class Graph:
    """依赖图。`deps[x]` 是 x 的前置依赖；只出现在依赖里的名字也算节点。"""

    def __init__(self, deps: Mapping[str, Iterable[str]]) -> None:
        raise NotImplementedError

    @property
    def nodes(self) -> tuple[str, ...]:
        raise NotImplementedError

    def prerequisites(self, node: str) -> tuple[str, ...]:
        raise NotImplementedError

    def descendants(self, node: str) -> frozenset[str]:
        raise NotImplementedError

    def order(self) -> list[str]:
        raise NotImplementedError


def install_order(deps: Mapping[str, Iterable[str]]) -> list[str]:
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Step:
    name: str
    fn: Callable[[dict[str, Any]], Any]
    needs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RunReport:
    results: Mapping[str, Any] = field(default_factory=dict)
    failed: Mapping[str, BaseException] = field(default_factory=dict)
    skipped: frozenset[str] = frozenset()

    @property
    def ok(self) -> bool:
        raise NotImplementedError


class Workflow:
    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, name: str, fn: Callable[[dict[str, Any]], Any], needs: Iterable[str] = ()) -> None:
        raise NotImplementedError

    def order(self) -> list[str]:
        raise NotImplementedError

    def run(self) -> dict[str, Any]:
        raise NotImplementedError

    def run_parallel(self, max_workers: int = 4) -> RunReport:
        raise NotImplementedError
