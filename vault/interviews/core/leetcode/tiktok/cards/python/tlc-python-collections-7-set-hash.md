---
id: tlc-python-collections-7-set-hash
node: python.collections
type: qa
step: 7
---
## Q
**Python 工具箱｜`set` 与可哈希性**

访问标记（visited）、去重、求交并差，用 `set` 的复杂度是多少？为什么 `{[1, 2]}` 报错，网格坐标应该怎样放进 `set`？

## A
`set` 的 `in`、`add`、`remove` 平均 `O(1)`；`a & b` 是 `O(min(|a|, |b|))`，`a | b` 是 `O(|a| + |b|)`。

```python
s, t = {1, 2, 3}, {2, 3, 4}
print(s & t, s | t, s - t, s ^ t, s <= {1, 2, 3, 4})  # {2, 3} {1,2,3,4} {1} {1, 4} True
print({(1, 2), (1, 2)})      # {(1, 2)}：元组可哈希，坐标放进 set 当 visited
# {[1, 2]}                   # TypeError: cannot use 'list' as a set element (unhashable type: 'list')
```

- 只有**不可变**且可哈希的对象能做集合元素或字典键：`int`、`str`、`tuple`（元素也得可哈希）、`frozenset`；`list`、`dict`、`set` 不行。
- 把列表当键时转成 `tuple(lst)`；把一组元素当键且与顺序无关时用 `frozenset`，或排序后转 `tuple`（LC 49 的签名）。
- 网格 BFS / DFS 的 visited 用 `set[tuple[int, int]]`，或者 `r * cols + c` 压成一个整数，更省内存、哈希更快。
- 比较是否有交集：`not a.isdisjoint(b)` 不构造新集合，比 `bool(a & b)` 省空间。
- **坑**：`{}` 是空字典，空集合必须写 `set()`；`set` 无序，不能下标访问，`pop()` 随机弹一个。
