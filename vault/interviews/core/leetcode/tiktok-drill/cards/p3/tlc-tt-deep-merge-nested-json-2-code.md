---
id: tlc-tt-deep-merge-nested-json-2-code
node: p3.tt-deep-merge-nested-json
type: qa
step: 2
---
## Q
**深度合并两个嵌套 JSON**｜写出 Python 实现

写 `merge(a, b, on_conflict="later")`：`a`、`b` 是嵌套 JSON 值（字典、列表、标量），返回合并后的新结构，不修改输入。两个字典递归合并，两个列表拼接（`a` 在前），同类标量取 `b`；类型不同时 `"later"` 取 `b`、`"error"` 抛 `TypeError`。嵌套深度可达 `2 * 10^4`，总元素数不超过 `10^5`。

## A
**思路。** 用显式栈代替递归：栈元素是 `(结果字典, 左字典, 右字典)`。弹出一个后遍历两边键的并集：只在一边出现的直接放进结果，两边都是字典的建一个空子字典放进结果并压栈，其余交给 `_combine` 处理叶子情形。

```python
from typing import Any

Json = dict[str, Any] | list[Any] | str | int | float | bool | None


def merge(a: Json, b: Json, on_conflict: str = "later") -> Json:
    """合并两个嵌套 JSON，返回新结构，不修改 a、b。
    dict + dict 递归合并；list + list 拼接；类型不同按 on_conflict 处理（"later" 取 b，"error" 抛 TypeError）；
    同类型的标量取 b。显式栈，嵌套深度不受递归上限影响。"""
    if not (isinstance(a, dict) and isinstance(b, dict)):
        return _combine(a, b, on_conflict, "<root>")
    root: dict[str, Any] = {}
    stack = [(root, a, b)]                            # (结果字典, 左字典, 右字典)
    while stack:
        out, left, right = stack.pop()
        for key in {**left, **right}:                 # 先左后右的键序，只在一侧出现的键也在里面
            if key not in right:
                out[key] = left[key]
            elif key not in left:
                out[key] = right[key]
            elif isinstance(left[key], dict) and isinstance(right[key], dict):
                out[key] = child = {}
                stack.append((child, left[key], right[key]))     # 不递归，压栈等下一轮
            else:
                out[key] = _combine(left[key], right[key], on_conflict, key)
    return root


def _combine(x: Json, y: Json, on_conflict: str, where: str) -> Json:
    if isinstance(x, list) and isinstance(y, list):
        return x + y
    if type(x) is type(y) or on_conflict == "later":   # 同类标量，或者策略是后者为准
        return y
    raise TypeError(f"conflict at {where!r}: {type(x).__name__} vs {type(y).__name__}")
```

运行：`a = {"name": "x", "tags": [1, 2], "cfg": {"a": 1, "b": {"c": 2}}}`，`b = {"tags": [3], "cfg": {"b": {"d": 4}, "a": 9}, "new": None}` → `{'name': 'x', 'tags': [1, 2, 3], 'cfg': {'a': 9, 'b': {'c': 2, 'd': 4}}, 'new': None}`，`a` 保持不变；`merge({"k": {"x": 1}}, {"k": [1]})` → `{'k': [1]}`，加 `"error"` 抛 `TypeError: conflict at 'k': dict vs list`；`merge([1], [2])` → `[1, 2]`；两个深度 `20000` 的单链字典合并不报 `RecursionError`。

**复杂度。** 时间 `O(总元素数)`：每个键在每一层只处理一次，列表拼接 `O(长度)`；空间 `O(深度)` 的栈加新建的结果容器。

**写法要点。**
- `{**left, **right}` 合成一个新字典，只为了拿到「先左后右、去重」的键序；比 `left.keys() | right.keys()` 稳定，后者是集合，顺序不确定。
- `out[key] = child = {}` 链式赋值：同一个新字典既放进结果，又拿来压栈，稍后往 `child` 里写就是写进结果。
- `type(x) is type(y)`：严格同类型才算同类标量，`1` 与 `True` 是不同类型；用 `isinstance` 会因为 `bool` 是 `int` 的子类而放过它们。
- 叶子情形抽成 `_combine`：栈循环只负责遍历，策略改动只动这一处。
