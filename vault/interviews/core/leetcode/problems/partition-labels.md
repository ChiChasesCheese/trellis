---
slug: partition-labels
---
## Q
**LC 763 划分字母区间（Partition Labels）**｜Medium

把小写字符串 `s` 划分成尽可能多的片段，使每个字母只出现在一个片段中，返回各片段长度。

## A
**一句话。** 先记每个字母最后出现的下标，扫描时用贪心把片段右边界 `end` 不断推远，走到 `end` 就切一刀。

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    ans = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])   # 片段要延伸到 c 最后出现处
        if i == end:              # 里面的字母不会再出现，切
            ans.append(end - start + 1)
            start = i + 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `end` 不取 `max`：直接赋成当前字母的最后位置，边界会被拉回去，`"abab"` 得 `[3,1]`，应为 `[4]`。
- 切完忘了 `start = i + 1`：之后每段长度都从 0 号位置算起，偏大。

**追问。**
- 为什么贪心对？：第一个字母的最后位置是片段的下界，片段内每个新字母只会把右边界推远，不会推近；边界稳定时切最早。
- 和合并区间什么关系？：每个字母的 `[首次, 最后]` 是一个区间，答案就是合并后各区间的长度。

**同模式。** LC 56 合并区间、LC 55 跳跃游戏、LC 45 跳跃游戏 II、LC 435 无重叠区间
