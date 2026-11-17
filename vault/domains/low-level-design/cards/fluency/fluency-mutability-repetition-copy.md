---
id: fluency-mutability-repetition-copy
node: fluency.mutability
type: qa
step: 4
---
## Q
`grid = [[0] * 3] * 3` 之后 `grid[0][0] = 1`，为什么三行都变成了 `[1, 0, 0]`？`list(a)`、`a[:]`、`a.copy()` 能解决吗？

## A
**`*` 复制引用，三种拷贝都是浅的**

- **`[x] * n` 是 n 个指向同一个 `x` 的引用**：不是 n 份副本；对数字、字符串没问题，对列表、字典就是别名；
- **用推导式每次新建**：写成 `[[0] * 3 for _ in range(3)]`，每一行都是新对象；内层的 `[0] * 3` 没问题，因为里面装的是不可变的整数，共享也改不了；
- **`list(a)`、`a[:]`、`a.copy()`、`dict(d)`、`d.copy()`**：只复制最外层容器，里面的元素仍是同一批对象，改内层两边都看得见；
- **复制到不可变值为止**：`[list(row) for row in a]`、`{k: list(v) for k, v in d.items()}`；形状复杂才考虑 `copy.deepcopy`；
- **同类的坑**：字典推导式 `{k: [] for k in keys}` 每个键各得一个新列表，没有问题；`dict.fromkeys(keys, [])` 却让所有键共用同一个列表，写完要读一遍确认。

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)                          # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)                          # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]

a = [[1], [2]]
print(a[:][0] is a[0], list(a)[0] is a[0], a.copy()[0] is a[0])   # True True True
d = dict.fromkeys("xy", [])
print(d["x"] is d["y"])              # True：所有键共用同一个列表
```

**知识点：**可变性与别名（Mutability & Aliasing）
