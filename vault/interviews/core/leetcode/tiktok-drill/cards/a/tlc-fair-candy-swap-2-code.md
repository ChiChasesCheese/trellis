---
id: tlc-fair-candy-swap-2-code
node: a.fair-candy-swap
type: qa
step: 2
---
## Q
**LC 888 公平的糖果交换**｜写出 Python 实现

两个数组 `aliceSizes`、`bobSizes`（长度各在 `[1, 10^4]`，元素在 `[1, 10^5]`，两人总数不同，保证有解），各选一盒交换使两人总数相同，返回 `[爱丽丝给出的, 鲍勃给出的]`，多个答案返回任意一个。

## A
**思路。** 令 `delta = (sumA - sumB) // 2`，合法交换满足 `y = x - delta`。把鲍勃的数量放进集合，遍历爱丽丝的每个 `x`，第一个让 `x - delta` 在集合里的就是答案。

```python
def fair_candy_swap(alice_sizes: list[int], bob_sizes: list[int]) -> list[int]:
    delta = (sum(alice_sizes) - sum(bob_sizes)) // 2   # 爱丽丝要比鲍勃多拿出这么多
    bob = set(bob_sizes)
    for x in alice_sizes:
        if (y := x - delta) in bob:                    # 交换 x 和 y 后两人总数相等
            return [x, y]
    return []                                          # 题目保证有解，这里不会执行
```

运行：`[1,1], [2,2]` → `[1,2]`，`[1,2], [2,3]` → `[1,2]`，`[2], [1,3]` → `[2,3]`，`[1,2,5], [2,4]` → `[5,4]`。

**复杂度。** 时间 `O(n + m)`；空间 `O(m)`。

**写法要点。** `set(bob_sizes)` 把成员查询变成 `O(1)`；`sum` 对列表求和是 C 实现的快路径；海象运算符 `(y := x - delta) in bob` 把「算目标」和「查成员」合在一行，同时保留 `y` 供后面返回；`//` 保证结果是整数。
