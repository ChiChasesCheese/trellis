---
id: tlc-zui-xiao-tiao-yue-ci-shu-2-code
node: b.zui-xiao-tiao-yue-ci-shu
type: qa
step: 2
---
## Q
**LCP 09 最小跳跃次数**｜写出 Python 实现

`N` 个弹簧（`1 <= N <= 10^6`，`1 <= jump[i] <= 10000`），在 `i` 按一次可向右到 `i + jump[i]`（`>= N` 即弹出）或向左到 `0..i-1` 任意位置，求从 `0` 号弹出机器的最少按动次数。要求 `O(n)`。

## A
**思路。** 按层 BFS，`frontier` 是当前层，`steps` 是到达下一层要按的次数。对层内每个 `i`：向右的目标出界就返回；没访问过就入下一层。向左用指针 `lo` 只扫 `lo..i-1` 这段新前缀。

```python
def minimum_jump(jump: list[int]) -> int:
    n = len(jump)
    seen = [False] * n
    seen[0] = True
    frontier, lo, steps = [0], 1, 0      # lo：下标 < lo 的弹簧都已经入队过
    while frontier:
        steps += 1                       # 这一层的每个点再按一次
        nxt: list[int] = []
        for i in frontier:
            j = i + jump[i]
            if j >= n:                   # 向右弹出了机器
                return steps
            if not seen[j]:
                seen[j] = True
                nxt.append(j)
            while lo < i:                # 向左能到 0..i-1，只扫还没扫过的那一段
                if not seen[lo]:
                    seen[lo] = True
                    nxt.append(lo)
                lo += 1
        frontier = nxt
    return -1                            # 到不了这里：一直向右弹总能出界
```

运行：`[2,5,1,1,1,1]` → `3`（`0 → 2 → 1 → 出界`），`[1]` → `1`，`[4,1,1,1]` → `1`，`[3,1,1,1]` → `2`，`[1,1,1,1]` → `4`；`10^6` 个 `1` → `1000000`。

**复杂度。** 时间 `O(n)`：每个下标最多入队一次；`lo` 只增不减，向左的扫描总共 `n` 步。空间 `O(n)`：`seen` 和队列。

**写法要点。** 用两个列表按层推进，`steps` 就是层号，不必给每个点存距离；`seen = [False] * n` 比 `set` 省内存、访问更快（`10^6` 个元素时差别明显）；**入队时**就标记 `seen`，每个下标只进队一次；`frontier, lo, steps = [0], 1, 0` 一次初始化多个变量。
