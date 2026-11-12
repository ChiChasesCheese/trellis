---
slug: tt-deep-merge-nested-json
---
## Q
**深度合并两个嵌套 JSON**｜Medium

实现 `merge(a, b, on_conflict="later")`，返回合并后的新结构，不修改 `a`、`b`：两边都是字典则按键递归合并，只在一边出现的键保留，列表拼接（`a` 在前），同类标量取 `b`；类型不同时 `"later"` 取 `b`，`"error"` 抛 `TypeError`。

## A
**一句话。** 递归：两边都是字典就遍历键的并集，单侧键直接取，双侧键递归；其余叶子情形当场处理。

```python
def merge(a, b, on_conflict="later"):
    def walk(x, y, where):
        if isinstance(x, dict) and isinstance(y, dict):
            out = {}
            for key in {**x, **y}:         # 键的并集，先左后右
                if key not in y:
                    out[key] = x[key]
                elif key not in x:
                    out[key] = y[key]
                else:
                    out[key] = walk(x[key], y[key], key)
            return out
        if isinstance(x, list) and isinstance(y, list):
            return x + y                   # a 的元素在前
        if type(x) is type(y) or on_conflict == "later":
            return y
        raise TypeError(f"conflict at {where!r}")

    return walk(a, b, "<root>")
```

**复杂度。** 时间 `O(总元素数)`，空间 `O(深度)` 加结果。

**易错点。**
- 深度 `2×10^4` 的链：递归超过 CPython 默认上限约 `1000`，抛 `RecursionError`，要调大 `setrecursionlimit` 或改显式栈。
- 原地改 `a`：`{"x":{"y":1}}` 并入 `{"x":{"z":2}}` 后 `a` 被改写，违反不修改输入。
- 只检查左边是字典：右边是标量时出错，条件必须是两边都是字典。
- 列表拼成 `y + x`：`merge({"t":[1,2]}, {"t":[3]})` 得 `[3,1,2]`，应为 `[1,2,3]`。

**追问。**
- 深层输入不想动递归上限？：显式栈，栈里放 `(结果字典, 左字典, 右字典)`，两边都是字典的键建空子字典压栈。
- 只要浅合并？：`{**a, **b}` 一行，深度合并多出来的就是对字典值递归。

**同模式。** LC 1634 多项式链表相加、LC 21 合并两个有序链表、LC 617 合并二叉树、LC 138 随机链表的复制
