---
slug: block-placement-queries
---
## Q
**LC 3161 物块放置查询**｜Hard

数轴上有两种操作：`[1, x]` 在 `x` 处加障碍物；`[2, x, sz]` 问 `[0, x]` 内能否放下长度 `sz` 的物块（可贴着障碍物，不真放）。按序返回每个类型 2 的结果。

## A
**一句话。** 线段树按坐标存「以该障碍物结尾的空隙长度」，查询取 `[0, p]` 的最大值再比较最后一段 `x - p`。

```python
def get_results(queries):
    size = max(q[1] for q in queries) + 1
    tree = [0] * (2 * size)   # 叶子 x = 以 x 结尾的空隙长度

    def update(pos, val):
        pos += size
        tree[pos] = val
        while pos > 1:
            pos >>= 1
            tree[pos] = max(tree[2*pos], tree[2*pos+1])

    def query_max(r):         # 下标 [0, r] 的最大值
        res, lo, hi = 0, size, r + 1 + size
        while lo < hi:
            if lo & 1:
                res = max(res, tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = max(res, tree[hi])
            lo >>= 1
            hi >>= 1
        return res

    obs = [0]                 # 有序障碍物，原点当哨兵
    ans = []
    for op, x, *rest in queries:
        if op == 1:
            k = bisect_left(obs, x)
            update(x, x - obs[k - 1])        # x 的左空隙
            if k < len(obs):                 # 后继的空隙被截短
                update(obs[k], obs[k] - x)
            obs.insert(k, x)
        else:
            p = obs[bisect_right(obs, x) - 1]  # [0,x] 内最右障碍
            ans.append(max(query_max(p), x - p) >= rest[0])
    return ans
```

**复杂度。** 时间 `O(q log M)`，空间 `O(M)`。

**易错点。**
- 漏掉最后一段 `[p, x]`：`[[1,2],[2,5,3]]` 得 `False`，应为 `True`。
- 插入后不缩短后继的空隙：`[[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]` 得 `[T,T,T]`，应为 `[T,T,F]`。
- 不放原点哨兵：空列表时 `obs[k-1]` 抛 `IndexError`，最靠左时 `k-1=-1` 悄悄取到最右元素。

**追问。**
- 为什么是 `>= sz`？：物块可以恰好接触障碍物。
- 坐标到 `10^9`？：线段树动态开点或离线离散化，有序列表换 `SortedList`。

**同模式。** LC 307 区域和检索 - 数组可修改、LC 218 天际线问题、LC 699 掉落的方块、LC 729 我的日程安排表 I
