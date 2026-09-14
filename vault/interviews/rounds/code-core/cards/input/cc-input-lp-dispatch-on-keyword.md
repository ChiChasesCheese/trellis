---
id: cc-input-lp-dispatch-on-keyword
node: input.line-protocols
type: qa
---
## Q
One stream mixes `MERCHANT,...`, `THRESHOLD,...`, `CHARGE,...` and `DISPUTE,...` lines in any order, and a later part adds two more record types. Structure the reader.

## A
**Dispatch on the leading token into one handler per record type.**

```python
kind, *rest = (f.strip() for f in line.split(","))
handler = HANDLERS.get(kind)
if handler is not None:
    handler(rest)
```

Each handler owns its own arity check and field conversion, so the loop stays four lines and a new record type in Part 4 is a new function rather than another branch inside a forty-line `if`. Decide the unknown-keyword policy once, at the `if handler is None` line — ignore, count, or abort — instead of per record type.

## Q zh
一条流里以任意顺序混着 `MERCHANT,...`、`THRESHOLD,...`、`CHARGE,...`、`DISPUTE,...` 四种行，而后面的部分还会加两种。怎么组织读取？

## A zh
**按行首 token 分派到每种记录各自的 handler。**

```python
kind, *rest = (f.strip() for f in line.split(","))
handler = HANDLERS.get(kind)
if handler is not None:
    handler(rest)
```

每个 handler 自己负责参数个数检查和字段转换，于是主循环只有四行，Part 4 新增记录类型是加一个函数，而不是在四十行的 `if` 里再加一个分支。未知关键字的策略在 `if handler is None` 这一行统一决定 —— 忽略、计数或中止 —— 而不是每种记录各写一遍。
