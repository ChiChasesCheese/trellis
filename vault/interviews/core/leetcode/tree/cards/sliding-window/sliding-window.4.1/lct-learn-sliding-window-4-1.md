---
id: lct-learn-sliding-window-4-1
node: sliding-window.4.1
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 双序列双指针 › 双指针**｜学习卡

套路是什么？

## A
**一句话。** 两个有序序列各放一个指针，只比较两个当前元素，让该前进的一边前进；被前进的元素不会再与对方剩下的部分产生新结果，所以每个元素只处理一次，`O(m+n)`。

下图：LC 986，两个指针各指一个区间，算完交集让终点更小的一方前进。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<line x1="30" y1="120" x2="306" y2="120" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="30" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="76" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="122" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="168" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="214" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="260" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="306" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<text x="10" y="34" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a</text>
<text x="10" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b</text>
<rect x="30" y="22" width="46" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="145" y="22" width="115" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="53" y="58" width="92" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="214" y="58" width="92" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="53" y="96" width="23" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="143" y="96" width="4" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="214" y="96" width="46" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="10" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">交</text>
<text x="170" y="156" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">交集 = [max 起点, min 终点]；终点小的那个前进</text>
</svg>

```python
def intersect(a, b):                # LC 986，区间闭合且各自有序
    i = j = 0
    ans = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])  # 交集 = [max 起点, min 终点]
        hi = min(a[i][1], b[j][1])
        if lo <= hi:                # 端点相碰也算
            ans.append([lo, hi])
        if a[i][1] < b[j][1]:       # 终点小的不会再与对方相交
            i += 1
        else:
            j += 1
    return ans
```

**要点。**
- 为什么对？：终点较小的区间最多只能和对方当前区间相交，已经算过；它与对方后面的区间都在右边之前结束，不相交，可以丢弃。
- LC 88 合并两个有序数组怎么改？：`nums1` 后面有空位，从后往前写，每次放两者中较大的，写入位置不会追上未读元素。
- LC 1570 两个稀疏向量的点积怎么改？：两边是按下标升序的 `(下标, 值)`；下标相同才相乘并双双前进，否则小下标的前进。

**易错点。**
- 88 从前往后写：`nums1 = [4,5,6,0,0,0]`、`nums2 = [1,2,3]` 会覆盖未读的 `nums1`。
- 88 循环条件写成 `i >= 0 and j >= 0` 漏接 `nums2` 的剩余：`nums1 = [0]`、`m = 0`、`nums2 = [1]` 应得 `[1]`，用 `while j >= 0` 即可。
- 986 把端点相碰当成无交集：`a = [[1,3]]`、`b = [[3,5]]` 应得 `[[3,3]]`，条件是 `lo <= hi`。

**对应题目。** LC 1570 两个稀疏向量的点积、LC 986 区间列表的交集、LC 88 合并两个有序数组
