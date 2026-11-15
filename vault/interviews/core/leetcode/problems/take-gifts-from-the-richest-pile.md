---
slug: take-gifts-from-the-richest-pile
---
## Q
**LC 2558 从数量最多的堆取走礼物**｜Easy

整数数组 `gifts`，`gifts[i]` 是第 `i` 堆礼物的数量。每秒选出礼物最多的一堆，留下它的平方根（向下取整），其余拿走。重复 `k` 秒，返回剩下的礼物总数。

## A
**一句话。** 大根堆（Python 里存负数）：每次取堆顶、开方后放回，共 `k` 次。

```python
def pick_gifts(gifts, k):
    h = [-g for g in gifts]
    heapify(h)
    for _ in range(k):
        g = -h[0]
        heapreplace(h, -isqrt(g))      # 一次弹出加压入
    return -sum(h)
```

**复杂度。** 时间 `O(n + k log n)`，空间 `O(n)`。

**易错点。**
- 开方用浮点：大数会有精度误差，用整数开方 `isqrt`。
- 用 `heappop` 再 `heappush`：功能一样，`heapreplace` 少一次上浮。

**追问。**
- `k` 很大怎么办？：每堆最多开方 `5` 次就变成 `1`，堆顶为 `1` 时可以提前结束。

**同模式。** LC 1046 最后一块石头的重量、LC 2530 执行 K 次操作后的最大分数、LC 1962 移除石子使总数最小
