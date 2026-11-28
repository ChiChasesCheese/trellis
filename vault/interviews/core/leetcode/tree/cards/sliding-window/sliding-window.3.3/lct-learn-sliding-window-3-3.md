---
id: lct-learn-sliding-window-3-3
node: sliding-window.3.3
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 单序列双指针 › 同向双指针**｜学习卡

套路是什么？

## A
**一句话。** 枚举保留的前缀末端 `l`，后缀起点 `r` 的最优位置随 `l` 单调不减，所以 `r` 只前进不回头，两个指针同向走，`O(n)`。

下图：LC 1574，枚举保留的前缀末端 `l`，后缀起点 `r` 跟着单调右移，从不回头。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="20" y="46" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="38.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="57" y="46" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="75.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="94" y="46" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="112.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="131" y="46" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="149.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="168" y="46" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="186.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="205" y="46" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="223.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="242" y="46" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="260.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="279" y="46" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="297.5" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="20" y1="40" x2="20" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168" y1="40" x2="168" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="40" x2="168" y2="40" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="94.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非降前缀</text>
<line x1="205" y1="40" x2="205" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="316" y1="40" x2="316" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="205" y1="40" x2="316" y2="40" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="260.5" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非降后缀</text>
<line x1="75.5" y1="92" x2="75.5" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="75.5,78.0 78.5,84.3 72.5,84.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="75.5" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">l</text>
<line x1="223.5" y1="92" x2="223.5" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="223.5,78.0 226.5,84.3 220.5,84.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="223.5" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">r</text>
<text x="170" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">l 右移时，能衔接的后缀起点 r 只会右移</text>
<text x="170" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">删掉 arr[l+1 : r]，长度 r - l - 1</text>
</svg>

```python
def shortest_removal(arr):          # LC 1574
    n = len(arr)
    r = n - 1
    while r and arr[r - 1] <= arr[r]:   # 最长非降后缀 arr[r:]
        r -= 1
    if r == 0:                      # 整个数组本来就有序
        return 0
    ans = r                         # 只留后缀：删掉 arr[:r]
    for l in range(n):              # 保留前缀 arr[:l+1]
        if l and arr[l - 1] > arr[l]:
            break                   # 前缀不再有序
        while r < n and arr[r] < arr[l]:
            r += 1                  # 衔接不上：后缀起点右移
        ans = min(ans, r - l - 1)   # 删除 arr[l+1:r]
    return ans
```

**要点。**
- 为什么对？：`l` 变大时 `arr[l]` 不减，之前因 `arr[r] < arr[l]` 被跳过的 `r` 仍然不合格，所以 `r` 不用回退。
- LC 581 最短无序连续子数组怎么改？：正着扫维护前缀最大值，比它小的最后一个位置是右端；倒着扫维护后缀最小值，比它大的最后一个位置是左端；没标出就返回 `0`。

**易错点。**
- 整个数组已有序没有提前返回：`arr = [1,2,3]` 应得 `0`，否则 `r` 退到 `0`，得到 `-1`。
- 衔接比较写成 `<=`：保留部分允许相等；`arr = [1,2,3,10,4,2,3,5]` 应得 `3`，写成 `<=` 得到 `4`。
- 581 把相等也当成需要排序：`nums = [1,2,2,3]` 应得 `0`。

**对应题目。** LC 1574 删除最短的子数组使剩余数组有序、LC 581 最短无序连续子数组
