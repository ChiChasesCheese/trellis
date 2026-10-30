---
id: tlc-tt-deep-merge-nested-json-0-whole
node: p3.tt-deep-merge-nested-json
type: qa
---
## Q
**深度合并两个嵌套 JSON**｜Medium · 近一年被问：美国 0 次、国内 4 次 · 最近 2026-10（国内面试记录）

实现 `merge(a, b)`，合并两个嵌套的 JSON 值（字典、列表、标量），返回新结构，不修改 `a` 和 `b`：两边都有的 key，若两个值都是字典，递归合并；只在一边出现的 key 直接保留；两个值都是列表时拼接（`a` 的元素在前）；两个同类型的标量取 `b`。类型不同（字典对列表、标量对字典等）按参数 `on_conflict` 处理：`"later"` 以 `b` 为准，`"error"` 抛 `TypeError`。键是字符串，嵌套深度可达 `2 * 10^4`，总元素数不超过 `10^5`。例：`a = {"name": "x", "tags": [1, 2], "cfg": {"a": 1, "b": {"c": 2}}}`，`b = {"tags": [3], "cfg": {"b": {"d": 4}, "a": 9}, "new": None}` → `{"name": "x", "tags": [1, 2, 3], "cfg": {"a": 9, "b": {"c": 2, "d": 4}}, "new": None}`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归：两边都是字典，就遍历键的并集——只在一边出现的直接取，两边都有的对两个值递归合并；其余叶子情形当场处理：列表拼接、同类标量取 `b`、类型冲突按策略。`O(总元素数)`。

**识别。** 「两棵嵌套结构按相同路径合并」是树的同步遍历：左右两棵树同时往下走。最直观的写法就是递归；「深度可能超过一万层」提醒要留意递归上限（见易错点），必要时改成显式栈（见追问）。「不修改输入」要求结果建新容器，沿着合并路径新建字典，没有被合并的子树可以直接共用。

**推导。** 暴力：`copy.deepcopy(a)` 之后递归地把 `b` 并进去——深拷贝本身就是递归的，`2 * 10^4` 层直接 `RecursionError`，而且把没有变化的部分也拷贝了。浪费：把没有变化的部分也拷贝了。洞察：结果和输入同构——合并两个字典，就是对每个键合并两边的子值；子值又是字典时是同一个问题的更小实例，直接递归；类型不同、列表拼接、标量覆盖是叶子情形，当场返回。只沿合并路径新建字典，没被合并的子树直接共用。

```python
from typing import Any

Json = dict[str, Any] | list[Any] | str | int | float | bool | None


def merge(a: Json, b: Json, on_conflict: str = "later") -> Json:
    """合并两个嵌套 JSON，返回新结构，不修改 a、b。
    dict + dict 递归合并；list + list 拼接；类型不同按 on_conflict 处理（"later" 取 b，"error" 抛 TypeError）；
    同类型的标量取 b。"""
    def walk(x: Json, y: Json, where: str) -> Json:
        if isinstance(x, dict) and isinstance(y, dict):       # 两边都是字典：按键合并，值继续递归
            out: dict[str, Any] = {}
            for key in {**x, **y}:                            # 先左后右的键序，只在一侧出现的键也在里面
                if key not in y:
                    out[key] = x[key]
                elif key not in x:
                    out[key] = y[key]
                else:
                    out[key] = walk(x[key], y[key], key)
            return out
        if isinstance(x, list) and isinstance(y, list):
            return x + y
        if type(x) is type(y) or on_conflict == "later":      # 同类标量，或者策略是后者为准
            return y
        raise TypeError(f"conflict at {where!r}: {type(x).__name__} vs {type(y).__name__}")

    return walk(a, b, "<root>")
```

运行：开头的例子 → `{'name': 'x', 'tags': [1, 2, 3], 'cfg': {'a': 9, 'b': {'c': 2, 'd': 4}}, 'new': None}`，`a` 保持不变；`merge({"k": {"x": 1}}, {"k": [1]})` → `{'k': [1]}`；同样的输入加 `"error"` → `TypeError: conflict at 'k': dict vs list`；`merge({"k": 1}, {"k": 2}, "error")` → `{'k': 2}`；`merge([1], [2])` → `[1, 2]`，`merge({"a": 1}, {})` → `{'a': 1}`；两个深度 `20000` 的单链字典合并，叶子处的列表 `[1]` 和 `[2]` 得到 `[1, 2]`（调大递归上限后）；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(总元素数)`：每个键在每一层只处理一次，列表拼接是 `O(长度)`；空间 `O(深度)` 的递归栈加上新建的结果容器。

**易错点。**
- 递归深度：深度 `2 * 10^4` 的单链输入，递归层数远超 CPython 默认上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）；`copy.deepcopy` 同样会爆。
- 原地修改 `a`：`a = {"x": {"y": 1}}`、`b = {"x": {"z": 2}}`，把 `b` 并进 `a`，之后 `a` 变成 `{'x': {'y': 1, 'z': 2}}`，违反「不修改输入」。
- 只检查左边是字典：右边是标量时，对它调用字典方法会出错；递归的条件必须是**两边**都是字典。
- 列表拼接顺序：`merge({"t": [1, 2]}, {"t": [3]})` 必须是 `[1, 2, 3]`，写成 `y + x` 得到 `[3, 1, 2]`。

**追问。**
- 类型冲突怎么选：可配置策略（`"later"` / `"error"`，也可以再加 `"earlier"`），冲突信息带上出错的 key 或路径；`type(x) is type(y)` 把 `1` 和 `True` 当成不同类型，若想放宽，改成 `isinstance` 的数值族判断。
- 结果和输入共用没被合并的子树：对结果的列表原地修改会改到输入，需要完全独立时再做一次迭代拷贝。
- 不想动递归上限：显式栈版，栈里放 `(结果字典, 左字典, 右字典)`，弹出一个就遍历键的并集，两边都是字典的建空子字典压栈，其余交给 `_combine`：
```python
from typing import Any

Json = dict[str, Any] | list[Any] | str | int | float | bool | None


def merge_iter(a: Json, b: Json, on_conflict: str = "later") -> Json:
    """显式栈版：栈里放 (结果字典, 左字典, 右字典)，嵌套深度不受递归上限影响。"""
    if not (isinstance(a, dict) and isinstance(b, dict)):
        return _combine(a, b, on_conflict, "<root>")
    root: dict[str, Any] = {}
    stack = [(root, a, b)]
    while stack:
        out, left, right = stack.pop()
        for key in {**left, **right}:
            if key not in right:
                out[key] = left[key]
            elif key not in left:
                out[key] = right[key]
            elif isinstance(left[key], dict) and isinstance(right[key], dict):
                out[key] = child = {}
                stack.append((child, left[key], right[key]))     # 压栈，等下一轮再填
            else:
                out[key] = _combine(left[key], right[key], on_conflict, key)
    return root


def _combine(x: Json, y: Json, on_conflict: str, where: str) -> Json:
    if isinstance(x, list) and isinstance(y, list):
        return x + y
    if type(x) is type(y) or on_conflict == "later":
        return y
    raise TypeError(f"conflict at {where!r}: {type(x).__name__} vs {type(y).__name__}")
```
- 全部重复键都取 `b` 的字典浅合并：`{**a, **b}` 一行；深度合并多出来的就是对字典值递归。

**同模式。** LC 1634 多项式链表相加、LC 21 合并两个有序链表、LC 617 合并二叉树、LC 138 随机链表的复制。
