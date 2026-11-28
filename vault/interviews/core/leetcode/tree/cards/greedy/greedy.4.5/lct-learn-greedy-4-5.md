---
id: lct-learn-greedy-4-5
node: greedy.4.5
type: qa
step: 1
---
## Q
**贪心算法 › 数学贪心 › 中位数贪心**｜学习卡

套路是什么？

## A
**一句话。** 中位数贪心：把所有数变成同一个值，到各点距离之和最小的目标就是中位数。

下图：LC 462，目标每偏离中位数一步，较多的一侧总距离都增加。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<line x1="30" y1="60" x2="327" y2="60" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<circle cx="57" cy="60" r="6" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="57" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<circle cx="84" cy="60" r="6" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="84" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<circle cx="111" cy="60" r="6" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="111" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="273" cy="60" r="6" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="273" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<circle cx="300" cy="60" r="6" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="300" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<path d="M 57 52 Q 84.0 36 111 52" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<path d="M 84 52 Q 97.5 38 111 52" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<path d="M 273 52 Q 192.0 28 111 52" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<path d="M 300 52 Q 205.5 26 111 52" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="111" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">中位数</text>
<text x="170" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">目标往右挪 1：左边 3 个点各 +1，右边 2 个各 -1</text>
<text x="170" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两边点数相等处（中位数）距离和最小</text>
</svg>

```python
def min_moves(nums):             # 每次 +1 或 -1，使全部相等
    nums.sort()
    mid = nums[len(nums) // 2]   # 中位数：偶数长度取哪个都行
    return sum(abs(x - mid) for x in nums)
```

**要点。**
- 为什么对？：首尾配对，每一对至少要花两数之差的代价；中位数落在每一对之间，所以对每一对都取到下界。
- LC 3086 怎么改？：先吃脚下及紧挨着的连续 `1`（至多 3 个），再用 `maxChanges` 造 `1`（每个 `2` 步）；不够的部分枚举长 `need` 的已有 `1` 的窗口，代价是向窗口中位数靠拢的距离和，用前缀和 `O(1)` 算。
- 能更快吗？：用快速选择找中位数，期望 `O(n)`。

**易错点。**
- 目标取平均数：`[1,0,0,8,6]` 得 `16`，应为 `14`（目标取 `1`）。
- 没排序就取中间下标：`[3,1,2]` 取到 `1`，得 `3`，应为 `2`。
- LC 3086 里 `c` 不对 `k` 取最小：`k = 1` 时答案应为 `0`。

**对应题目。** LC 462 最小操作次数使数组元素相等 II、LC 3086 拾起 K 个 1 需要的最少行动次数
