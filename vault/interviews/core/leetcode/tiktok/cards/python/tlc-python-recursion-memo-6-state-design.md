---
id: tlc-python-recursion-memo-6-state-design
node: python.recursion-memo
type: qa
step: 6
---
## Q
**Python 递归｜记忆化的状态怎么设计才合法**

`@cache` 函数的参数里能放列表吗？记忆化搜索与回溯里「边走边改」的 `path` 能混用吗？状态选得太大会怎样？

## A
缓存键由**全部参数**组成，要求可哈希，且函数结果**只依赖这些参数**。

```python
from functools import cache
@cache
def count_subsets(i: int, rem: int) -> int:      # 用前 i 个数凑出 rem 的方案数，数是 1..i
    if i == 0:
        return 1 if rem == 0 else 0
    skip = count_subsets(i - 1, rem)
    take = count_subsets(i - 1, rem - i) if rem >= i else 0
    return skip + take
print(count_subsets(5, 7))     # 3：{2,5}、{3,4}、{1,2,4}
@cache
def total(a: tuple[int, ...]) -> int:
    return sum(a)
try:
    total([1])
except TypeError as e:
    print(e)                   # unhashable type: 'list'
print(total((1, 2)))           # 3：换成 tuple 就能做缓存键
```

- 传**下标**代替切片 / 列表，传 `tuple` 或 `frozenset` 代替可变集合；位掩码 `int` 是最紧凑的集合状态（LC 473 火柴拼正方形的状态压缩）。
- 缓存和 `path` 不能混：一旦函数结果依赖闭包里会变的外部变量（`path`、`visited`），同样的参数在不同时刻结果不同，缓存就返回了过期值。要么把它放进参数，要么这是回溯题、不该缓存。
- 状态数决定一切：`(i, rem)` 是 `n * target` 个；加上不必要的参数（比如把已走过的路径整个传进去）会把状态数炸成指数级，缓存命中率为 0。
- 缓存里的返回值如果是列表（LC 140 单词拆分 II 返回所有方案），调用方修改它会污染缓存；返回元组，或每次拷贝。
- 检查办法：`f.cache_info()` 看 `hits` 和 `currsize`；`hits` 为 0 说明状态设计错了。
