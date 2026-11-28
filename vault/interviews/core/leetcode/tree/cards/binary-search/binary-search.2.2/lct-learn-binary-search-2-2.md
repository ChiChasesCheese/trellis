---
id: lct-learn-binary-search-2-2
node: binary-search.2.2
type: qa
step: 1
---
## Q
**二分算法 › 二分答案 › 求最大**｜学习卡

套路是什么？

## A
**一句话。** 求最大的可行答案是求最小的镜像：虚拟数组 `check` 是 `真…真假…假`，要最后一个真；口诀是 `check(mid)` 为真时更新谁，最后就返回谁。

下图：求最大是求最小的镜像，虚拟数组是「真…真假…假」，要最后一个真。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="50" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="35.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T</text>
<rect x="50" y="50" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="65.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T</text>
<rect x="80" y="50" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T</text>
<rect x="110" y="50" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="125.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T</text>
<rect x="140" y="50" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<rect x="170" y="50" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<rect x="200" y="50" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<rect x="230" y="50" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<rect x="260" y="50" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<rect x="290" y="50" width="30" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="305.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<line x1="20" y1="44" x2="20" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="44" x2="170" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="44" x2="170" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="95.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">真：可行</text>
<line x1="170" y1="44" x2="170" y2="38" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="320" y1="44" x2="320" y2="38" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="44" x2="320" y2="44" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="245.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">假</text>
<line x1="155.0" y1="96" x2="155.0" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="155.0,82.0 158.0,88.3 152.0,88.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="155.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">left = 最后一个真</text>
<line x1="305.0" y1="96" x2="305.0" y2="82" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="305.0,82.0 308.0,88.3 302.0,88.3" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="305.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">right 哨兵</text>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">check(mid) 真时更新 left，最后就返回 left</text>
</svg>

```python
def max_value(n, index, max_sum):   # LC 1802
    def side(x, cnt):               # 一侧 cnt 个数，递减到 1
        if x - 1 >= cnt:
            return (x - 1 + x - cnt) * cnt // 2
        return x * (x - 1) // 2 + cnt - (x - 1)     # 触底补 1

    def check(x):                   # 峰值 x 时总和是否 <= max_sum
        total = x + side(x, index) + side(x, n - 1 - index)
        return total <= max_sum

    left, right = 1, max_sum + 1    # left 真，right 假
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            left = mid              # 真时更新 left，返回 left
        else:
            right = mid
    return left
```

**要点。**
- 为什么对？：峰值越小总和越小，`check` 单调；总和最小的构造是两侧每步少 `1`、最低为 `1`，用等差数列 `O(1)` 算。
- 为什么 `right = max_sum + 1`？：`right` 必须是一定不可行的值；写成 `max_sum` 会让答案取不到 `max_sum`（如 `n = 1`）。
- 和求最小怎么对照？：求最小真时 `right = mid`、返回 `right`；求最大真时 `left = mid`、返回 `left`。

**易错点。**
- 返回了 `right`：`n = 4`、`index = 2`、`max_sum = 6` 应得 `2`，返回 `right` 会得到 `3`。
- 触底时漏掉剩下的 `1`：`n = 3`、`index = 0`、`max_sum = 3` 应得 `1`，漏了会得到 `2`。
- `right` 取 `max_sum`：`n = 1`、`max_sum = 10**9` 应得 `10**9`，会得到 `10**9 - 1`。

**对应题目。** LC 1802 有界数组中指定下标处的最大值
