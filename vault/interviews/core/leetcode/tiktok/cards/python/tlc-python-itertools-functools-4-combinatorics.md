---
id: tlc-python-itertools-functools-4-combinatorics
node: python.itertools-functools
type: qa
step: 4
---
## Q
**Python 工具箱｜`product`、`combinations`、`permutations`**

笛卡尔积、组合、排列在 `itertools` 里各是哪个函数？输出的顺序和个数怎样？输入有重复元素时会怎样，面试里什么时候能用它们代替回溯？

## A
```python
from itertools import product, combinations, permutations, combinations_with_replacement
print(list(product("ab", repeat=2)))            # [('a','a'),('a','b'),('b','a'),('b','b')]
print(list(combinations([1, 2, 3], 2)))         # [(1,2),(1,3),(2,3)]：按位置选，不重复
print(list(permutations([1, 2, 3], 2))[:3])     # [(1,2),(1,3),(2,1)]
print(list(combinations_with_replacement("ab", 2)))   # [('a','a'),('a','b'),('b','b')]
```

| 函数 | 个数 | 说明 |
|---|---|---|
| `product(x, repeat=r)` | `len(x)^r` | 每位独立选，可重复 |
| `combinations(x, r)` | `C(n, r)` | 保持输入顺序，不重复选 |
| `permutations(x, r)` | `n! / (n-r)!` | 有顺序 |
| `combinations_with_replacement` | `C(n+r-1, r)` | 可重复选 |

- 它们按**位置**而非值判断元素：`permutations([1, 1, 2])` 产出 6 个元组，里面只有 3 种不同的，去重要 `set(...)`；LC 47 全排列 II 的回溯用「排序后跳过同层相同值」更省。
- 都是惰性生成器，空间 `O(r)`；转成 `list` 才会占 `O(个数)` 的内存。
- 用途：写**暴力解**当基准（`n <= 8` 时 `permutations` 一行枚举全部排列）；`product([0, 1], repeat=n)` 枚举子集掩码；小规模题（LC 78、46）可以直接用。
- 但面试里被要求「写回溯」时，库函数不能代替回溯模板：需要边选边剪枝（LC 39、51、79）的题，库函数只会枚举全部再过滤，复杂度失控。
