"""模板 1 · 多 part 题的骨架 —— 92 道题里 90 道长这样。

**先把这个骨架敲出来，再想题目本身。** 骨架敲完只要 3 分钟，但它决定了
part 2、part 3 加需求时你要不要重写——`skills_matrix.md` 的 S19 说的就是这件事。

四段分层，每段只干一件事：

    parse  →  model  →  compute  →  render
    原始行     记录      业务逻辑     输出字符串

为什么必须分开：Stripe 的题是**做完一个 part 才给下一个 part**，而下一个 part
通常只动其中一段。揉在一起 = 每加一个 part 重写一次。

用法：`cp skeleton.py starter.py`，然后从上往下填。
"""
from __future__ import annotations

import sys
from dataclasses import dataclass


# ---------------------------------------------------------------- model
# 先定形状。想不清楚有哪些字段，就说明题还没读懂——回去读题，别硬写。
@dataclass
class Record:
    id: str
    amount: int          # 整数最小单位（分）。永远不要 float。
    kind: str


# ---------------------------------------------------------------- parse
def parse_records(lines: list[str]) -> list[Record]:
    """只管把文本变成 Record，不做任何业务判断。

    脏行怎么办？**先问面试官**：跳过、报错、还是计入统计？三种做法结果完全不同。
    这里默认跳过，并且把这个决定写在注释里——面试官会看你有没有意识到这是个决定。
    """
    out: list[Record] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 3:          # 字段不足：不要无脑解包，会 ValueError
            continue
        rid, amount, kind = parts[0], parts[1], parts[2]
        try:
            out.append(Record(id=rid.strip(), amount=int(amount), kind=kind.strip()))
        except ValueError:          # amount 不是整数
            continue
    return out


# ---------------------------------------------------------------- compute
def part1(lines: list[str]) -> list[str]:
    records = parse_records(lines)
    rows = [(r.id, r.amount) for r in records]
    return [_format(rid, amt) for rid, amt in rows]


def part2(lines: list[str]) -> list[str]:
    """part 2 复用 part 1 的 parse 和 _format，只换中间那段。

    如果你发现 part 2 要改 parse_records 才能做——停下来，多半是 part 1 的
    模型建窄了（比如少存了一个字段）。改模型，别在 compute 里打补丁。
    """
    records = parse_records(lines)
    rows = sorted(((r.id, r.amount) for r in records), key=lambda t: (-t[1], t[0]))
    return [_format(rid, amt) for rid, amt in rows]


# ---------------------------------------------------------------- render
def _format(rid: str, amount: int) -> str:
    """输出格式**集中在一处**。part 3 说"改成两位小数"时，你只改这一个函数。

    Stripe 逐字节比对：多一个逗号、行尾多个空格、少一个换行，都算错。
    """
    return f"{rid},{amount}"


# ---------------------------------------------------------------- main
def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """多 part 题的标准入口：第一行是 `PART n`，按它分发。

    调试输出一律走 **stderr**——stdout 是要被逐字节比对的答案。
        print(f"{records=}", file=sys.stderr)
    """
    lines = stdin.read().splitlines()
    part = 1
    if lines and lines[0].strip().upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]

    dispatch = {1: part1, 2: part2}
    fn = dispatch.get(part)
    if fn is None:
        raise SystemExit(f"unknown part: {part}")
    for line in fn(lines):
        print(line, file=stdout)


if __name__ == "__main__":
    main()
