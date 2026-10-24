---
id: tlc-stickers-to-spell-word-0-whole
node: a.stickers-to-spell-word
type: qa
---
## Q
**LC 691 贴纸拼词**｜Hard · TikTok 高频

有 `n` 种贴纸，每张贴纸上是一个小写英文单词，每种贴纸数量无限。要拼出字符串 `target`：从贴纸上剪下单个字母，再任意重排。返回拼出 `target` 所需的最少贴纸数；做不到返回 `-1`。`n == stickers.length`，`1 <= n <= 50`，`1 <= stickers[i].length <= 10`，`1 <= target.length <= 15`，所有字符串只含小写英文字母。例：`stickers = ["with","example","science"]`，`target = "thehat"` → `3`（两张 `"with"` 加一张 `"example"`）；`stickers = ["notice","possible"]`，`target = "basicbasic"` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 状态压缩 DP：`dp[mask]` 表示盖住 `target` 中 `mask` 这些位置所需的最少贴纸数；每次只处理最低的未覆盖位置，只尝试含这个字母的贴纸，一张贴纸能盖多少盖多少。`O(2^m * n * m)`，`m = len(target)`。

**识别。** `target.length <= 15` 是明确的状态压缩信号（`2^15 = 32768` 个状态）；「最少张数、每种无限」是最短路 / 完全背包型的最优化；字母可重排、数量有限，所以每张贴纸要当字母多重集合（`Counter`）来用。

**推导。** 暴力：每一步从 `n` 种贴纸里任选一张，直到盖满，`n^k` 级 → 浪费 1：贴纸的使用顺序无关，却被当成不同序列反复搜索；浪费 2：同一个「还没盖住的字母集合」被重复到达 → 洞察 1：状态就是 `target` 里哪些位置已被盖住，共 `2^m` 个，用整数位掩码表示；洞察 2：任何方案都必须盖住最低的那个未覆盖位置，而贴纸顺序可以任意交换，所以不妨规定下一张贴纸必须含这个字母，分支从 `n` 缩到含该字母的那几种；洞察 3：盖得多不会更差，一张贴纸对未覆盖位置能盖多少就盖多少。

```python
from collections import Counter, defaultdict
from math import inf


def min_stickers(stickers: list[str], target: str) -> int:
    n = len(target)
    full = (1 << n) - 1
    has_letter: defaultdict[str, list[Counter[str]]] = defaultdict(list)
    for s in stickers:
        cnt = Counter(s)
        for ch in cnt:
            has_letter[ch].append(cnt)          # 按字母索引：含该字母的贴纸

    dp = [inf] * (1 << n)                       # dp[mask]：凑出 target 中 mask 这些位置所需的最少贴纸
    dp[0] = 0
    for mask in range(full):
        if dp[mask] == inf:
            continue
        low = (~mask & (mask + 1)).bit_length() - 1      # 最低的未覆盖位置
        for cnt in has_letter[target[low]]:              # 只试能盖住它的贴纸
            left, new = cnt.copy(), mask
            for i, ch in enumerate(target):              # 贴纸字母能盖多少盖多少
                if not new >> i & 1 and left[ch] > 0:
                    left[ch] -= 1
                    new |= 1 << i
            dp[new] = min(dp[new], dp[mask] + 1)
    return -1 if dp[full] == inf else dp[full]
```

运行：`["with","example","science"]`，`"thehat"` → `3`；`["notice","possible"]`，`"basicbasic"` → `-1`；`["a"]`，`"aaaa"` → `4`；`["ab"]`，`"a"` → `1`；`["ab"]`，`"aa"` → `2`。

**复杂度。** 时间 `O(2^m * k * m)`，`k` 是含最低未覆盖字母的贴纸数（最坏 `n`），实际可达状态远少于 `2^m`；空间 `O(2^m)`。

**易错点。**
- 每次选覆盖字母最多的贴纸（贪心）：`["cf","bf","fffb","aaef"]`，`"ffccfc"` 会先选 `"fffb"`，共 `4` 张，正确是 `3`（三张 `"cf"`）。
- 同一字母出现多次时只用「是否包含」判断：`["ab"]`，`"aa"` 会得到 `1`，正确是 `2`，必须按个数消耗 `left[ch]`。
- 忘了 `cnt.copy()`：贴纸的 `Counter` 被消耗后，下一个状态再用同一张贴纸时字母已经变成 `0`，结果偏大甚至误判 `-1`。

**追问。**
- 剪枝：若一张贴纸的字母多重集是另一张的子集，它永远不会更优，先删掉。
- 要返回具体用了哪几张：给 `dp[new]` 同时记录前驱状态和贴纸下标，最后回溯。
- 记忆化 DFS（状态是剩余字母的有序字符串）只访问可达状态，常数小；位掩码版上界更稳定。

**同模式。** LC 464 我能赢吗、LC 698 划分为k个相等的子集、LC 847 访问所有节点的最短路径、LC 1125 最小的必要团队、LC 526 优美的排列。
