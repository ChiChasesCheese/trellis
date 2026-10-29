---
id: tlc-minimum-cost-good-caption-5-alt
node: a.minimum-cost-good-caption
type: qa
step: 5
---
## Q
**LC 3441 变成好标题的最少代价**｜另一种解法

如果只需要最少操作数，有没有更直接的 DP？它为什么不能直接给出字典序最小的串，什么时候用它？

## A
**思路。** 把标题切成若干块，每块是同一个字母且长度 `>= 3`。长度更长的块总能拆成长度 3、4、5 的块，代价不变，所以每块只试这三种长度。一块内把所有字符改成同一个字母，代价最小的字母是块内字符的中位数。`f[i]` 是把 `caption[i:]` 变好的最小代价。

```python
def min_cost_blocks(caption: str) -> int:
    n = len(caption)
    if n < 3:
        return -1
    cap = [ord(ch) - 97 for ch in caption]
    INF = float("inf")
    f = [INF] * (n + 1)                          # f[i]：把 caption[i:] 变成好标题的最小操作数
    f[n] = 0
    for i in range(n - 3, -1, -1):
        for size in (3, 4, 5):                   # 更长的块总能拆成 3、4、5 长的同字母块，代价不变
            if i + size <= n and f[i + size] < INF:
                block = sorted(cap[i : i + size])
                mid = block[size // 2]           # 把一段数变成同一个数，改成中位数最省
                f[i] = min(f[i], sum(abs(x - mid) for x in block) + f[i + size])
    return int(f[0])
```

`"cdcd"` → `2`；`"aca"` → `2`；`"bc"` → `-1`。

**取舍。** 时间 `O(n)`，空间 `O(n)`，比主解法小一个 26 倍的常数，也更容易想到。缺点：块的边界不是由已选前缀唯一决定的（同一个字符串可以切成不同的块），所以不能像主解法那样「逐位贪心」重建字典序最小的串；若硬要，得在每个位置保存最优串并比较，复杂度失控。**什么时候用哪个：** 只问最少操作数，或想在小数据上验证主解法的代价，用块 DP；要返回字典序最小的标题，必须用「连续长度状态加正向贪心」。
