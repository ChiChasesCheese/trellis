---
id: tlc-patterns-hashing-6-pitfalls
node: patterns.hashing
type: qa
step: 6
---
## Q
**哈希（Hashing）｜常见陷阱**

哈希类题最容易在哪些地方出错？

## A
1. **键不可哈希**：`list`、`dict`、`set` 当键报 `TypeError`；转 `tuple` 或 `frozenset`。
2. **签名拼接碰撞**：把数字列表用 `"".join(map(str, ...))` 做键，`[1, 23]` 和 `[12, 3]` 都变成 `"123"`，会误判为同一组。要加分隔符 `","`，或直接用 `tuple`。
3. **排序签名与计数签名的代价**：`"".join(sorted(s))` 是 `O(k log k)`；字母表固定时计数向量的 `tuple` 是 `O(k)`。`k <= 100` 时两者都过。
4. **边遍历边改字典**：`RuntimeError: dictionary changed size during iteration`；遍历 `list(d)` 的拷贝。
5. **先存后查还是先查后存**：决定是否允许用同一元素两次；LC 1 要先查后存。
6. **`defaultdict` 读取也会插入**：用 `d[k]` 判断是否存在，会悄悄加一个键，使 `len(d)` 变大；用 `k in d` 或 `d.get(k)`。
7. **用浮点数当键**：`0.1 + 0.2` 与 `0.3` 不同；用整数或 `Fraction` 做键。
8. **字符串哈希的复杂度**：键是长字符串时，每次哈希是 `O(len)`，不是 `O(1)`；LC 49 的复杂度要写成 `O(N * k)`，不是 `O(N)`。
9. **空输入**：`[]`、`""` 要有正确返回（LC 128 的 `nums = []` → `0`）。

- 用 `Counter` 做窗口时，次数减到 `0` 的键会残留：`len(c)` 把它也算进去；3.10 起 `Counter(a=1, b=0) == Counter(a=1)` 为 `True`，旧版本为 `False`，所以要么及时 `del`，要么别依赖 `len` 与 `==`。
