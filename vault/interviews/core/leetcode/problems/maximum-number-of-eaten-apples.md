---
slug: maximum-number-of-eaten-apples
---
## Q
**LC 1705 吃苹果的最大数目**｜Medium

第 `i` 天长出 `apples[i]` 个苹果，在第 `i + days[i]` 天腐烂。每天最多吃一个，`n` 天后也能继续吃。求最多能吃几个。

## A
**一句话。** 每天先把当天的苹果按「腐烂日」放进最小堆，丢掉已烂或吃完的堆顶，再吃最早烂的那一个。

```python
def eaten_apples(apples, days):
    h, ans, i = [], 0, 0       # h：[腐烂日, 剩余个数]
    while i < len(apples) or h:
        if i < len(apples) and apples[i]:
            heappush(h, [i + days[i], apples[i]])
        while h and (h[0][0] <= i or h[0][1] == 0):
            heappop(h)         # 已经烂了或吃完了
        if h:
            h[0][1] -= 1       # 吃最早烂的一个
            ans += 1
        i += 1
    return ans
```

**复杂度。** 时间 `O((n + D) log n)`（`D` 为最晚腐烂日），空间 `O(n)`。

**易错点。**
- 过期判断用 `<`：第 `i + days[i]` 天当天已经烂了，要 `<=`。
- 第 `n` 天后就停：堆里还有没烂的苹果，要一直吃到堆空。

**追问。**
- `n` 天之后能加速吗？：不再有新苹果，堆顶一批可一次吃 `min(剩余个数, 腐烂日 - i)` 个，直接跳天数。
- 为什么吃最早烂的？：交换论证，晚烂的留到以后还能吃，早烂的错过就没了。

**同模式。** LC 502 IPO、LC 1353 最多可以参加的会议数目、LC 630 课程表 III
