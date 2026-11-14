---
slug: high-five
---
## Q
**LC 1086 前五科的均分**｜Easy

给 `items[i] = [id, score]`，每个学生至少 5 个分数。按 `id` 升序返回每人最高 5 个分数的平均分（整数除法）。

## A
**一句话。** 按学生分组，每人维护大小为 5 的小顶堆，超过 5 个就弹出最小的，剩下的就是最高的 5 个。

```python
def high_five(items):
    top = defaultdict(list)    # id -> 大小为 5 的小顶堆
    for sid, score in items:
        heappush(top[sid], score)
        if len(top[sid]) > 5:
            heappop(top[sid])  # 踢掉当前最小的
    return [[sid, sum(h) // 5]
            for sid, h in sorted(top.items())]
```

**复杂度。** 时间 `O(n log 5 + k log k)`，`k` 是学生数；空间 `O(k)`。

**易错点。**
- 用大顶堆：要的是「最大的 5 个」，留下它们得用小顶堆，堆顶才是要淘汰的。
- 忘了按 `id` 排序输出：字典遍历顺序不是 `id` 顺序。

**追问。**
- 分数范围只有 0–100？：每人一个计数数组，从 100 往下取 5 个，`O(n)`。
- 数据流不断到达？：堆就是在线结构，每来一个分数 `O(log 5)` 更新。

**同模式。** LC 215 数组中的第K个最大元素、LC 703 数据流中的第 K 大元素、LC 347 前 K 个高频元素
