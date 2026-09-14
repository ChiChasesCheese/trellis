---
id: cc-python-idioms-unpacking-enumerate-zip
node: python.idioms
type: qa
---
## Q
A record line has a fixed head and a variable-length tail; the output needs 1-based indices; and you must walk two sequences in lockstep. Write the three idioms and name the trap in each.

## A
```python
kind, ident, *rest = line.split(",")     # *rest is always a list, possibly empty
for i, row in enumerate(rows, start=1):  # 1-based, no i + 1 anywhere
for a, b in zip(xs, ys, strict=True):    # 3.10+: raises on length mismatch
a, b = b, a                              # swap, no temporary
```

- `*rest` handles optional trailing fields by itself — no `len(parts) > 3` checks.
- `enumerate(..., start=1)` deletes every `i + 1` from the output code, which is exactly where off-by-one errors live.
- Plain `zip` stops at the shortest input **silently**; `strict=True` turns a data bug into an exception.

## Q zh
一行记录有固定的头部和变长的尾部；输出需要 1 起始的下标；你还要并行遍历两个序列。写出这三个惯用法，并指出各自的陷阱。

## A zh
```python
kind, ident, *rest = line.split(",")     # *rest 永远是 list，可能为空
for i, row in enumerate(rows, start=1):  # 1 起始，代码里不再出现 i + 1
for a, b in zip(xs, ys, strict=True):    # 3.10+：长度不等时抛异常
a, b = b, a                              # 交换，不需要临时变量
```

- `*rest` 自己就处理了可选的尾部字段 —— 不需要 `len(parts) > 3` 之类的判断。
- `enumerate(..., start=1)` 把输出代码里的每一个 `i + 1` 都删掉，而差一错误正是住在那里。
- 普通 `zip` 会在最短的输入处**静默**停止；`strict=True` 把数据 bug 变成异常。
