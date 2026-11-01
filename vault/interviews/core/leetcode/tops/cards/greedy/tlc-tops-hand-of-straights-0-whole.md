---
id: tlc-tops-hand-of-straights-0-whole
node: greedy.hand-of-straights
type: qa
---
## Q
**LC 846 一手顺子**｜Medium · 全公司热度第 778 名 · NeetCode 150

Alice 手里有一把牌，她想把牌重新排列分成若干组，每组恰好 `groupSize` 张，并且每组由 `groupSize` 张**连续**的牌（数值依次加 `1`）组成。给你整数数组 `hand`（`hand[i]` 是第 `i` 张牌上的数值）和整数 `groupSize`，能做到就返回 `true`，否则返回 `false`。`1 <= hand.length <= 10^4`，`0 <= hand[i] <= 10^9`，`1 <= groupSize <= hand.length`。例：`hand = [1,2,3,6,2,3,4,7,8]`, `groupSize = 3` → `true`（`[1,2,3]`、`[2,3,4]`、`[6,7,8]`）；`hand = [1,2,3,4,5]`, `groupSize = 4` → `false`。（与 LC 1296 相同。）

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 贪心（greedy）+ 计数表（`Counter`）：最小的牌必须是某一组的起点。

**一句话。** 从小到大处理每个数值，若它还有 `c` 张，就必须以它为起点开 `c` 组，一次性把 `x..x+groupSize-1` 每个数值都扣掉 `c` 张，扣不够就失败。

**识别。** 「分成若干组连续的 / 等长的」「顺子」= 最小元素只能做某组的开头，从最小处贪心；`n = 10^4`，`O(n log n)`。

**推导。** 暴力：回溯尝试各种分组，指数级。观察：当前最小的牌 `x` 不可能出现在任何一组的中间或末尾（那样同组里还要有比它更小的牌），所以它必然是某个顺子的起点，该顺子被唯一确定为 `x, x+1, ..., x+groupSize-1`。有 `c` 张 `x` 就要开 `c` 个这样的顺子，每个数值都要扣掉 `c` 张；由于处理顺序是升序，先处理的数值不会受后面的影响，贪心成立。

```python
from collections import Counter


def is_n_straight_hand(hand: list[int], groupSize: int) -> bool:
    if len(hand) % groupSize:  # 牌数不是组大小的整数倍，直接失败
        return False
    cnt = Counter(hand)
    for x in sorted(cnt):  # 升序处理：当前 x 是剩余牌里最小的数值
        c = cnt[x]
        if c == 0:  # 已经被前面的顺子用完
            continue
        for y in range(x, x + groupSize):  # x 开头的 c 个顺子，每个数值都要扣 c 张
            if cnt[y] < c:  # 缺牌（Counter 对不存在的键返回 0）
                return False
            cnt[y] -= c
    return True
```

运行：示例 1 → `True`；示例 2 → `False`；`([1,3,5,7], 2)` → `False`；`([2,3,4,1,2,3], 3)` → `True`；`([1,2,2,3], 2)` → `True`。

**复杂度。** 时间 `O(n log n)`（排序主导；内层循环总共不超过 `n / groupSize * groupSize`），空间 `O(n)`。

**拓展优化。**
- 一个数值一次扣 `c` 张，而不是一张一张建组，避免了 `cnt[x]` 很大时的重复循环；若牌是流式到来或需要小根堆，可以用堆顶当最小值，逻辑相同。

**易错点。**
- 只判断 `len(hand) % groupSize == 0`：`hand = [1,3,5,7]`, `groupSize = 2` 返回 `True`，正确是 `False`（没有连续的对）。
- 按字典插入顺序而不是升序处理：`hand = [2,3,4,1,2,3]`, `groupSize = 3` 先从 `2` 开一组 `2,3,4`，后面的 `3` 找不到 `4` 返回 `False`，正确是 `True`（`[1,2,3]`、`[2,3,4]`）。
- 扣牌后不检查 `cnt[y] < c`，直接 `cnt[y] -= c`：计数会变成负数而不报错，`hand = [1,3]`, `groupSize = 2` 返回 `True`，正确是 `False`。

**同模式。** LC 1296 划分数组为连续数字的集合、LC 659 分割数组为连续子序列、LC 1743 从相邻元素对还原数组、LC 128 最长连续序列。
