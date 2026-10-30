---
id: tlc-tt-deep-merge-nested-json-4-followup
node: p3.tt-deep-merge-nested-json
type: qa
step: 4
---
## Q
**深度合并两个嵌套 JSON**｜追问

已有 `merge(a, b, on_conflict)`：递归、不修改输入、字典递归合并、列表拼接。面试官接着问：（1）同一个 key 两边类型不同怎么处理？（2）结果和输入共用了没被合并的子树，会有什么问题？（3）列表想按元素去重或按 `id` 合并？（4）怎么测？（5）嵌套深度 `2 * 10^4`，递归超过默认上限怎么办？

## A
1. **类型冲突**：做成可配置策略。`"later"` 以 `b` 为准，`"earlier"` 以 `a` 为准，`"error"` 抛 `TypeError` 并带上出错的 key。严格同类型才算同类标量：`1` 和 `True` 视为冲突，`type(x) is type(y)`；想把 `int` 与 `float` 当同类，就改成数值族判断。
2. **共用子树**：没被合并的值（如只在 `a` 里出现的列表）在结果里是同一个对象，对结果原地修改会改到输入：`r = merge({"a": [1]}, {"b": 2}); r["a"].append(9)` 之后输入的 `a` 也变成 `[1, 9]`。要完全独立，就在取值时拷贝；`copy.deepcopy` 会在深层结构上 `RecursionError`，需要自己写迭代拷贝。
3. **列表元素合并**：先问清是去重（用 `dict.fromkeys(x + y)` 保持顺序去重，元素要可哈希）还是按 `id` 对齐（建 `{item["id"]: item}` 再递归合并同 `id` 的元素）；这会让「列表」也成为需要递归合并的类型。
4. **测试**：空字典、只一边有 key、三层嵌套、列表拼接顺序、类型冲突两种策略、输入不被修改（合并前后对输入做深拷贝比较）、深度 `2 * 10^4` 的链；结构随机的小输入与一个显式栈的参考实现比较。
5. **递归超限**：`sys.setrecursionlimit` 调大即可；不想动上限就用显式栈，栈里放 `(结果字典, 左字典, 右字典)`：
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

**Python 提醒**：`{**a, **b}` 和 `dict | dict`（3.9+）都只做浅合并，同名 key 直接被后者覆盖，不会递归；`json.dumps` 对超深结构同样会 `RecursionError`，序列化前先确认深度。
