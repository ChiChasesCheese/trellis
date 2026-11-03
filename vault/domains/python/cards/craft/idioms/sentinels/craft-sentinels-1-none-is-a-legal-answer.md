---
id: craft-sentinels-1-none-is-a-legal-answer
node: craft.idioms.sentinels
type: qa
step: 1
---
## Q
**哨兵 · 当 None 本身是合法答案时用什么表示「没有」**｜写法

图像变换流水线要合并相邻步骤：连续两次左右翻转可以抵消，函数返回 `None` 表示「抵消，两步都删掉」。那「这两步合并不了」怎么表示？如果也返回 `None` 会出什么问题？同样的问题在 `dict.get` 里长什么样？

## A
**要点。** 哨兵（sentinel）是一个专门用来表示「没有这个值」的特殊对象。当 `None` 已经是合法结果时，需要另一个谁也造不出来的对象，通常是模块级的 `object()`，用 `is` 判断。`is` 比较的是身份而不是内容，所以不会被某个恰好 `==` 它的值骗过。

```python
_NO_MERGE = object()          # 模块级单例：谁也造不出第二个相同的对象

def merge(a: str, b: str):
    """能合并返回结果；互相抵消返回 None；不能合并返回 _NO_MERGE。"""
    if {a, b} == {"rot90", "rot270"}:
        return None                              # 抵消：这是合法结果
    if a == b == "flipx":
        return None
    if a == b == "rot90":
        return "rot180"
    return _NO_MERGE

def merge_naive(a, b):
    r = merge(a, b)
    return None if r is _NO_MERGE else r         # 朴素版：两种情况压成同一个 None

for a, b in [("rot90", "rot90"), ("flipx", "flipx"), ("rot90", "flipx")]:
    r = merge(a, b)
    kind = "不能合并" if r is _NO_MERGE else ("抵消" if r is None else f"合并成 {r}")
    print(a, b, kind, "| 朴素:", merge_naive(a, b))

cfg = {"timeout": None}                         # None 表示「不超时」，是用户明确设的
print(cfg.get("timeout", 30), cfg.get("retries", 30))
_MISSING = object()
v = cfg.get("timeout", _MISSING)
print("设为 None" if v is None else "没设" if v is _MISSING else v)
```

实际输出：

```
rot90 rot90 合并成 rot180 | 朴素: rot180
flipx flipx 抵消 | 朴素: None
rot90 flipx 不能合并 | 朴素: None
None 30
设为 None
```

**为什么。** 朴素版里第二行和第三行都是 `None`：一个要删掉两步，一个要原样保留，混在一起就会错误地丢弃步骤。`dict.get(k, 30)` 同理：用户显式设置了 `None`（不超时）时返回的是 `None`，没设置才返回 30，要区分就得用哨兵当默认值。

**易错。** 不需要区分时不用哨兵：如果 `None` 只表示「没有」，`x is None` 最清楚，不要为了显得讲究引入 `object()`。
