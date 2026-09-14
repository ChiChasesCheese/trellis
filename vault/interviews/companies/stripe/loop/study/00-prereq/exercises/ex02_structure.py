"""ex02 · 程序结构 —— 你的作答文件。运行：python -m pytest test_ex02.py -q"""
from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Event:
    ts: int
    kind: str
    amount: int


def parse_events(lines: list[str]) -> list[Event]:
    """每行 `ts,kind,amount`；跳过空行 / 只有空白的行；amount 转 int。"""
    # TODO
    return []


class Counter2:
    """计数器：add(kind) 记一次；top() 返回出现最多的 kind，并列取字典序最小；没有数据返回 None。"""

    def __init__(self) -> None:
        # TODO：初始化你的状态
        pass

    def add(self, kind: str) -> None:
        # TODO
        pass

    def top(self) -> str | None:
        # TODO
        return None


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """读全部输入，输出每种 kind 的总额：`kind,total` 每行一个，kind 字典序。"""
    # TODO
    pass


if __name__ == "__main__":
    main()
