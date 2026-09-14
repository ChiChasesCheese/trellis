---
id: cc-chrono-parsing-strict-validation
node: chrono.parsing
type: qa
---
## Q
One row carries the date `2024-2-3`, another `2024-02-30`. What does `datetime.strptime(s, "%Y-%m-%d")` do with each — and how do you reject both when the spec demands the exact zero-padded form?

## A
**`strptime` is lenient about width and strict about the calendar.** `2024-2-3` parses happily (and renders as `2024-02-03`); `2024-02-30` raises `ValueError`.

- To demand the exact literal shape, round-trip it:

```python
def valid(s, f="%Y-%m-%dT%H:%M:%S"):
    try: return datetime.strptime(s, f).strftime(f) == s
    except ValueError: return False
```

- Wrap parse-and-validate in **one** predicate returning the value or `None`; a corrupted row is then a return value, not a `try` block at every use site.
- Decide per field whether "lenient" is wanted — accepting `2024-2-3` and printing it normalized is a legitimate rule, but it must be a decision, not an accident.

## Q zh
一行的日期是 `2024-2-3`，另一行是 `2024-02-30`。`datetime.strptime(s, "%Y-%m-%d")` 对它们分别做什么 —— 当 spec 要求严格的补零形式时，怎么把两者都拒掉？

## A zh
**`strptime` 对宽度宽松、对日历严格。** `2024-2-3` 能正常解析（并渲染成 `2024-02-03`）；`2024-02-30` 抛 `ValueError`。

- 要求字面形式完全一致，就做一次往返比对：

```python
def valid(s, f="%Y-%m-%dT%H:%M:%S"):
    try: return datetime.strptime(s, f).strftime(f) == s
    except ValueError: return False
```

- 把解析加校验包进**一个**谓词，返回值或 `None`；这样损坏的行是一个返回值，而不是散落在各处的 `try`。
- 逐字段决定是否要宽松 —— 接受 `2024-2-3` 再归一化输出是合法规则，但必须是决定，而不是意外。
