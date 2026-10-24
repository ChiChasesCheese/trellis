---
id: tlc-python-pitfalls-6-truthy-is
node: python.pitfalls
type: qa
step: 6
---
## Q
**Python 陷阱｜`if not x`、`is None` 与 `==`**

节点值可能为 `0`，为什么 `if not node.val` 会写错？什么时候该用 `is`，什么时候该用 `==`？

## A
`0`、`0.0`、`""`、`[]`、`{}`、`set()`、`None` 在布尔判断里都是假值。

```python
x = 0
print(not x, x is None, x == None)      # True False False：0 是假值，但它不是 None
```

- 区分「没有值」与「值为 0 / 空」时，用 `is None` / `is not None`；`if not x` 会把 `0` 也当成没有。
  - 二叉树里用 `if not root:` 判空没问题（节点对象总是真值），但判断 `root.val` 是否存在要写 `is None`。
  - `memo.get(k)` 返回 `0` 是合法答案时，`if memo.get(k):` 会把它当成缺失；写 `if (v := memo.get(k)) is not None:`。
  - LC 53、152 里 `best = 0` 当初值会让全负数组出错，应取 `-math.inf` 或 `nums[0]`。
- `==` 比较值，`is` 比较**是不是同一个对象**。比较 `None`、`True`、`False` 用 `is`；比较数字、字符串、列表用 `==`。
- 小整数缓存会让 `a = 256; b = 256; a is b` 为 `True`，换成大数就是 `False`，结果取决于实现，不要用 `is` 比较数字。
- 链表题判断「两个节点是同一个节点」（LC 160 相交、LC 141 环）必须用 `is`，不能比较 `val`。
- 空容器判断：`if not stack:` 比 `if len(stack) == 0:` 更地道。
- **坑**：自己定义了 `__eq__` 的类，`==` 可能被改写；`__hash__` 也要同步，否则放进 `set` / `dict` 行为异常。
