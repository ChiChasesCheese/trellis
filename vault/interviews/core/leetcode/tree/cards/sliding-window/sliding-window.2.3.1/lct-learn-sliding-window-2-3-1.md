---
id: lct-learn-sliding-window-2-3-1
node: sliding-window.2.3.1
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 求子数组个数 › 越短越合法**｜学习卡

套路是什么？

## A
**一句话。** 数“越短越合法”的子数组个数：每个右端点缩到窗口合法，以 `right` 结尾的合法子数组恰有 `right - left + 1` 个，逐个累加。

下图：缩到合法后，左端点取 `left..right` 中任意一个都合法，一次加上 `right - left + 1`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<rect x="30" y="40" width="46" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="53.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<rect x="76" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="99.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="122" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="168" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="191.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<rect x="214" y="40" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="237.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="191.0" y1="24" x2="191.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="191.0,38.0 188.0,31.7 194.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="191.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right</text>
<line x1="99.0" y1="24" x2="99.0" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,38.0 96.0,31.7 102.0,31.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="99.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<line x1="173.0" y1="84" x2="209.0" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="173.0" y1="80" x2="173.0" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="209.0" y1="80" x2="209.0" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="127.0" y1="102" x2="209.0" y2="102" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="127.0" y1="98" x2="127.0" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="209.0" y1="98" x2="209.0" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="81.0" y1="120" x2="209.0" y2="120" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="81.0" y1="116" x2="81.0" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="209.0" y1="116" x2="209.0" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">以 right 结尾的合法子数组 = right - left + 1 = 3 个</text>
<text x="170" y="172" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LC 713，k = 100：窗口合法，它的每个后缀也合法</text>
</svg>

```python
def count_product_less(nums, k):    # LC 713，nums[i] >= 1
    if k <= 1:                      # 乘积至少是 1，不可能 < k
        return 0
    ans = left = 0
    prod = 1                        # 窗口内乘积
    for right, x in enumerate(nums):
        prod *= x                   # 入
        while prod >= k:            # 不合法：缩
            prod //= nums[left]     # 出：整除是精确的
            left += 1
        ans += right - left + 1     # 左端点 left..right
    return ans
```

**要点。**
- 为什么对？：元素都 `>= 1`，乘积随窗口变长不减，合法左端点是 `[left, right]`；更短的 `[left+1, right]` 等也合法。
- 和“求最长”相比怎么改？：只改答案那一行，`max(ans, right - left + 1)` 换成 `ans += right - left + 1`。

**易错点。**
- 不特判 `k <= 1`：`nums = [1,1,1]`、`k = 1` 乘积永远 `>= 1`，`left` 会走出数组，应返回 `0`。
- 用 `/=` 还原乘积：得到浮点数，大数有误差，用 `//=`。
- 每个右端点只算一个：`nums = [10,5,2,6]`、`k = 100` 应得 `8`，只加 `1` 会得到 `4`。

**对应题目。** LC 713 乘积小于 K 的子数组
