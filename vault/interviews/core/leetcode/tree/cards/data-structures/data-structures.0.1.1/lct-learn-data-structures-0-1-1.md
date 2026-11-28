---
id: lct-learn-data-structures-0-1-1
node: data-structures.0.1.1
type: qa
step: 1
---
## Q
**常用数据结构 › 常用枚举技巧 › 枚举右，维护左 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 双变量 `i < j` 的题只枚举右边的 `j`，把左边所有 `i` 的有用信息压成一个哈希表或变量，先查后存，一次遍历完成。

下图：`j` 左边的元素都已压进摘要；`j` 先查摘要结算答案，再把自己存进去。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="20" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="60" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="100" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="140" y="40" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="160.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x</text>
<rect x="180" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="220" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="260" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x</text>
<line x1="20" y1="34" x2="20" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140" y1="34" x2="140" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="34" x2="140" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="80.0" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已放进摘要（j 左边）</text>
<text x="240" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还没看</text>
<text x="160.0" y="82" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<rect x="20" y="110" width="120" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">摘要：哈希表 / 变量</text>
<line x1="160.0" y1="88" x2="112" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112.0,108.0 116.7,102.8 119.0,108.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="165" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 先查：左边有能配对的吗</text>
<text x="165" y="130" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">② 再存：把 x 放进摘要</text>
<text x="165" y="148" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">然后 j 右移一格</text>
</svg>

```python
def two_sum(nums, target):           # LC 1：摘要 = 值 -> 下标
    idx = {}                         # 只存 j 左边的元素
    for j, x in enumerate(nums):
        if target - x in idx:        # 左边有没有 target - x
            return [idx[target - x], j]
        idx[x] = j                   # 先查后存，不会自己配自己
def max_profit(prices):              # LC 121：摘要 = 左边最低价
    ans, low = 0, prices[0]
    for p in prices:
        ans = max(ans, p - low)      # 先结算（今天卖）
        low = min(low, p)            # 再把今天放进摘要
    return ans
def nearby_dup(nums, k):             # LC 219：摘要 = 最近下标
    last = {}
    for j, x in enumerate(nums):
        if x in last and j - last[x] <= k:
            return True
        last[x] = j                  # 覆盖成最近的
    return False
```

**要点。**
- 为什么对？：一对 `(i, j)` 只在遍历到较大下标 `j` 时被考虑一次，不重不漏；摘要只保留回答所需的最少信息，`O(n²)` 降成 `O(n)`。
- 摘要怎么选？：存在性用集合，个数用 `Counter`，值到下标用字典，最值用一个变量。
- 为什么 LC 219 覆盖旧下标？：同值只有最近的一个离 `j` 最近，旧的被覆盖不丢答案。

**易错点。**
- 先存后查：`[3,2,4]`、`target = 6` 应得 `[1,2]`，先存 `3` 会把它和自己配成 `[0,0]`。
- LC 121 的 `low` 初值设成 `0`：`[7,6,4,3,1]` 应得 `0`，会得到 `7`。
- 用 `idx.get(...)` 的真假判断：下标 `0` 为假，`[2,7]`、`target = 9` 会漏掉。

**对应题目。** LC 1 两数之和、LC 121 买卖股票的最佳时机、LC 219 存在重复元素 II
