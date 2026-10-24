---
id: tlc-python-idioms-3-comprehensions
node: python.idioms
type: qa
step: 3
---
## Q
**Python 工具箱｜推导式、生成器表达式与 `any` / `all` / `max(key=)`**

计数、判断存在、取最值时，为什么用生成器表达式而不是先建一个列表？`max` / `min` 的 `key` 和 `default` 参数怎么用？

## A
列表推导式用方括号，立刻建出整个列表；生成器表达式用圆括号，逐个产出，不占 `O(n)` 额外内存，`any` / `all` 还能**短路**。

```python
nums = [1, -2, 3]
print(sum(1 for x in nums if x > 0))      # 2：计数，不建列表
print(any(x < 0 for x in nums))           # True：遇到第一个就停
print(all(x != 0 for x in nums))          # True
print(max([], default=0))                 # 0：空序列有默认值，不抛 ValueError
print(max(nums, key=abs), min(["bb", "a", "ccc"], key=len))   # 3 a
print({c: i for i, c in enumerate("abc")}, {x % 3 for x in range(10)})
```

- `max(iterable, key=f)` 返回使 `f` 最大的**元素本身**；`key` 相同取第一个遇到的。LC 2456 这类「按某个量取最大」直接用。
- `sum(1 for ...)` 比 `len([...])` 省内存；`sum(x > 0 for x in nums)` 也行，`True` 当 `1`，但前者更直白。
- 字典推导式 `{c: i ...}`、集合推导式 `{...}` 同理；二维数组用 `[[0] * n for _ in range(m)]`（不要用 `[[0]*n]*m`，见陷阱一组）。
- 推导式里别写副作用（`[print(x) for x in a]`）；也别把三层嵌套 + 条件写在一行，面试官读不懂就是扣分。
- **坑**：生成器是一次性的，`g = (x for x in a)` 遍历一次后再用是空的；`any([])` 为 `False`，`all([])` 为 `True`（空真）。
