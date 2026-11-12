---
slug: stickers-to-spell-word
---
## Q
**LC 691 贴纸拼词**｜Hard

每种贴纸数量无限，可剪下单个字母任意重排。求拼出 `target` 的最少贴纸数，做不到返回 `-1`（`len(target) <= 15`）。

## A
**一句话。** 状态压缩 DP：`dp[mask]` 是盖住 `target` 中 `mask` 位置的最少贴纸数，每次只处理最低的未覆盖位置。

```python
def min_stickers(stickers, target):
    n = len(target)
    full = (1 << n) - 1
    has = defaultdict(list)        # 字母 -> 含它的贴纸
    for s in stickers:
        cnt = Counter(s)
        for ch in cnt:
            has[ch].append(cnt)
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(full):
        if dp[mask] == inf:
            continue
        low = (~mask & (mask + 1)).bit_length() - 1
        for cnt in has[target[low]]:    # 只试能盖住 low 的
            left, new = cnt.copy(), mask
            for i, ch in enumerate(target):
                if not new >> i & 1 and left[ch] > 0:
                    left[ch] -= 1       # 能盖多少盖多少
                    new |= 1 << i
            dp[new] = min(dp[new], dp[mask] + 1)
    return -1 if dp[full] == inf else dp[full]
```

**复杂度。** 时间 `O(2^m·n·m)`，空间 `O(2^m)`（`m = len(target)`）。

**易错点。**
- 贪心选覆盖最多的贴纸：`["cf","bf","fffb","aaef"]`、`"ffccfc"` 贪心得 `4`，正确是 `3`。
- 忘了 `cnt.copy()`：原 `Counter` 被消耗，下次再用这张贴纸字母已是 `0`。

**追问。**
- 为什么只处理最低未覆盖位？：每个位置迟早要被盖，固定顺序避免重复枚举。
- 怎么剪枝？：若一张贴纸的字母是另一张的子集，永远不更优，先删掉。

**同模式。** LC 464 我能赢吗、LC 698 划分为k个相等的子集、LC 847 访问所有节点的最短路径、LC 1125 最小的必要团队
