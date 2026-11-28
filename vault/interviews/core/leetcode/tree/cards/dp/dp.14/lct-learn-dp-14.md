---
id: lct-learn-dp-14
node: dp.14
type: qa
step: 1
---
## Q
**动态规划 › 博弈 DP**｜学习卡

套路是什么？

## A
**一句话。** 博弈 DP：`f(状态)` 表示轮到的人在最优对弈下的结果（必胜与否，或净胜分），对手那一步的结果取反或相减。

下图：LC 486，轮到的人取一端后对手变成先手，对手的结果要减掉；`-2 < 0`，先手输。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="68.0" y="9.5" width="203.9" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f(0,2) = max(1-3, 2-4) = -2</text>
<rect x="14.7" y="72.0" width="140.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取左端 1</text>
<text x="85" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对手面对 f(1,2) = 3</text>
<rect x="184.7" y="72.0" width="140.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取右端 2</text>
<text x="255" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对手面对 f(0,1) = 4</text>
<path d="M 68.0 22.0 L 85.0 22.0 L 85.0 72.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,72.0 82.0,65.7 88.0,65.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 272.0 22.0 L 255.0 22.0 L 255.0 72.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,72.0 252.0,65.7 258.0,65.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums = [1, 5, 2]；f = 当前先手的净胜分</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我拿的分 − 对手在剩余局面下的净胜分</text>
</svg>

```python
def predict_winner(nums):
    @cache
    def f(i, j):                     # 只剩 nums[i..j]：先手的净胜分
        if i == j:
            return nums[i]
        # 取一端后对手成为先手，他的净胜分要减掉
        return max(nums[i] - f(i + 1, j),
                   nums[j] - f(i, j - 1))

    return f(0, len(nums) - 1) >= 0  # 平局算先手赢
```

**要点。**
- 为什么对？：双方都最优，我选使自己净胜分最大的一步，对手面对剩下的局面也一样，所以一个函数加「减掉对手的」就描述了轮换。
- LC 294 怎么改？：状态是整个字符串，只问输赢：`win(s)` 为真当且仅当存在一步翻转使 `win(新局面)` 为假；无步可走即必败。

**易错点。**
- 递推里「加」对手的分差：变成区间和，永远非负，`[1,5,2]` 误判 `true`。
- 平局判成输：写成 `> 0`，`[3,3]` 应返回 `true`。
- 贪心取两端较大的：`[1,5,233,7]` 得 `false`，应为 `true`。

**对应题目。** LC 294 翻转游戏 II、LC 486 预测赢家
