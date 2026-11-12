---
slug: most-popular-video-creator
---
## Q
**LC 2456 最流行的视频创作者**｜Medium

`creators[i]`、`ids[i]`、`views[i]` 描述第 `i` 个视频。流行度是创作者全部播放量之和。返回流行度最高（可并列）的创作者及其播放量最大的视频 id，并列取字典序最小。

## A
**一句话。** 哈希表聚合总播放量，最佳视频用元组 `(-播放量, id)` 取最小，一次比较处理两个规则。

```python
def most_popular_creator(creators, ids, views):
    pop = defaultdict(int)
    best = {}                      # 创作者 -> (-播放量, id)
    for c, vid, v in zip(creators, ids, views):
        pop[c] += v
        cand = (-v, vid)
        if c not in best or cand < best[c]:
            best[c] = cand
    top = max(pop.values())
    return [[c, best[c][1]] for c in pop if pop[c] == top]
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 并列只比播放量用 `>`：保留先出现的 id，`["x","x"]`, `["c","b"]`, `[2,2]` 得 `c`，应为 `b`。
- 只返回一个创作者：流行度并列要全部返回。
- 拿单个视频播放量当流行度：流行度是总和。

**追问。**
- 返回前 `k` 个创作者？：`heapq.nlargest(k, ...)`，`O(n log k)`。
- 数据流式到来？：额外维护当前最大流行度和创作者集合，新视频只会增大某人的流行度。

**同模式。** LC 692 前 K 个高频单词、LC 347 前 K 个高频元素、LC 1636 按频率排序
