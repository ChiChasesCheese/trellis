---
id: lct-learn-binary-search-1-1
node: binary-search.1.1
type: qa
step: 1
---
## Q
**二分算法 › 二分查找 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 有序数组上的一切查找都化成 `lower_bound(x)` = 第一个 `>= x` 的下标；用“红蓝染色 + 开区间”写，不变量替你管好所有加一减一。

下图：`lower_bound(8)` 结束时的开区间：`left` 停在最后一个红，`right` 停在第一个蓝。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<rect x="57" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="94" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="131" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="149.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="168" y="50" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="186.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<rect x="205" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="223.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="242" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="260.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="279" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="38.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="75.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="112.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="149.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="186.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="223.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="260.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="297.5" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<line x1="57" y1="44" x2="57" y2="38" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="168" y1="44" x2="168" y2="38" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="57" y1="44" x2="168" y2="44" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="112.5" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">红：&lt; 8</text>
<line x1="168" y1="44" x2="168" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="279" y1="44" x2="279" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168" y1="44" x2="279" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="223.5" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">蓝：≥ 8</text>
<line x1="149.5" y1="116" x2="149.5" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.5,102.0 152.5,108.3 146.5,108.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="149.5" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">left</text>
<line x1="186.5" y1="116" x2="186.5" y2="102" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="186.5,102.0 189.5,108.3 183.5,108.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="186.5" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right</text>
<text x="38.5" y="66" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哨兵</text>
<text x="297.5" y="66" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哨兵</text>
<text x="230" y="128" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">left + 1 == right 时停</text>
<text x="230" y="144" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">答案 = right = 3</text>
</svg>

```python
def lower_bound(nums, x):
    # 开区间 (left, right)：左红右蓝，红 < x，蓝 >= x
    left, right = -1, len(nums)     # 两端是哨兵，从不访问
    while left + 1 < right:         # 区间内还有未染色的数
        mid = (left + right) // 2
        if nums[mid] >= x:
            right = mid             # mid 是蓝
        else:
            left = mid              # mid 是红
    return right                    # 第一个蓝


def search_range(nums, target):     # LC 34
    i = lower_bound(nums, target)
    if i == len(nums) or nums[i] != target:     # 不存在
        return [-1, -1]
    return [i, lower_bound(nums, target + 1) - 1]
```

**要点。**
- 为什么对？：不变量是 `nums[left] < x <= nums[right]`（哨兵视为红、蓝）；每轮区间缩小，结束时 `left + 1 == right`，`right` 就是第一个蓝。
- 其他查询怎么改？：`> x` 的第一个是 `lb(x+1)`；`< x` 的最后一个是 `lb(x)-1`；`<= x` 的最后一个是 `lb(x+1)-1`；个数是两个 `lb` 之差。
- LC 704、LC 35 怎么改？：704 取 `i = lb(x)` 再验证 `nums[i] == x`；35 答案就是 `lb(x)`，不存在时 `n` 即插到末尾。

**易错点。**
- 忘了验证存在：`nums = [1,3]`、`x = 2`，`lb = 1`，但 `nums[1] = 3`，应返回 `-1`。
- 负下标陷阱：`nums = [5,6]` 找最后一个 `<= 4`，`lb(5) - 1 = -1`，`nums[-1]` 是 `6`，先判 `>= 0`。
- 初始 `right = n - 1`：`nums = [1,2,3]`、`x = 4` 应返回 `3`，会返回 `2`。

**对应题目。** LC 704 二分查找、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置
