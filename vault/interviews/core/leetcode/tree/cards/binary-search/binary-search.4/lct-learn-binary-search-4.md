---
id: lct-learn-binary-search-4
node: binary-search.4
type: qa
step: 1
---
## Q
**二分算法 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 二分不要求数组有序，只要有一个能 `O(1)` 判断的谓词把区间染成 `红…红蓝…蓝`；难点只在找谓词，以及右端哨兵为什么一定是蓝。

下图：数组不必有序，只要一个谓词把区间分成前红后蓝。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="10" y="22" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LC 153：a[i] ≤ a[-1] 为蓝</text>
<rect x="20" y="30" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="62" y="30" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="104" y="30" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="146" y="30" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="188" y="30" width="42" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="209.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="230" y="30" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="251.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="272" y="30" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="293.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="10" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LC 69（n = 8）：x² &gt; 8 为蓝</text>
<rect x="20" y="100" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="62" y="100" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="104" y="100" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="146" y="100" width="42" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="167.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="188" y="100" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="209.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="230" y="100" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="251.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<rect x="272" y="100" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="293.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="209.0" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第一个蓝 = 最小值</text>
<text x="170" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">不必有序：谓词把区间染成「红…红蓝…蓝」即可；答案 3 - 1 = 2</text>
</svg>

```python
def first_true(left, right, blue):  # 开区间 (left, right)
    while left + 1 < right:
        mid = (left + right) // 2
        if blue(mid):
            right = mid
        else:
            left = mid
    return right                    # 第一个蓝

def my_sqrt(n):                     # LC 69：n+1 必蓝
    return first_true(-1, n + 1, lambda x: x * x > n) - 1

def find_peak(a):                   # LC 162：n-1 必蓝
    return first_true(-1, len(a)-1, lambda i: a[i] > a[i+1])

def rotated_min(a):                 # LC 153：与末尾比
    i = first_true(-1, len(a) - 1, lambda i: a[i] <= a[-1])
    return a[i]
```

**要点。**
- 怎么找谓词？：问“`mid` 左右有没有区别，能用 `a[mid]` 加邻居、端点或奇偶位置立刻判出来”；旋转数组比较末尾，山峰比较邻居，成对元素比较 `i ^ 1`。
- LC 33 搜索旋转排序数组怎么改？：用 `last = nums[-1]` 分段；`x > last` 在前半段，蓝是 `target > last and x >= target`；`x <= last` 在后半段，蓝是 `target > last or x >= target`；最后验证 `nums[i] == target`。
- LC 154、LC 81 有重复怎么改？：`nums[i] == nums[-1]` 无法判断落在哪段，154 相等时 `right -= 1`，81 先裁掉末尾等于 `nums[0]` 的元素，最坏 `O(n)`。
- LC 4 两个正序数组的中位数怎么改？：在较短数组上二分切点 `i`，另一边 `j = (m+n+1)//2 - i`，谓词 `a[i] >= b[j-1]`。

**易错点。**
- 153 用 `nums[0]` 作参照：`[1,2,3]` 应得 `1`，会得到 `3`；154 `[3,3,1,3]` 应得 `1`。
- 69 右哨兵给 `n`：`n = 1` 应得 `1`，会得到 `0`，要给 `n + 1`。
- 540 用 `a[i] != a[i+1]` 当谓词：`[1,1,2,3,3]` 应得 `2`，颜色变成 `假真真假`，不单调。

**对应题目。** LC 154 寻找旋转排序数组中的最小值 II、LC 153 寻找旋转排序数组中的最小值、LC 162 寻找峰值、LC 278 第一个错误的版本（First Bad Version）、LC 1539 第 k 个缺失的正整数、LC 4 寻找两个正序数组的中位数、LC 852 山脉数组的峰顶索引、LC 81 搜索旋转排序数组 II、LC 33 搜索旋转排序数组、LC 540 有序数组中的单一元素、LC 69 x 的平方根
