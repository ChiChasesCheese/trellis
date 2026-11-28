---
id: lct-learn-math-7-10
node: math.7.10
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 这一节是杂项，没有统一套路，各题各记一招；最常考的是「下一个排列」：从右找第一个升序对，与右侧刚好更大的数交换，再把右侧反转成最小。

下图：下一个排列的三步：找最右升序对、和右侧刚好更大的数交换、右侧反转。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="50" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="30" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="130" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="170" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="210" y="30" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="250" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="110.0" y1="14" x2="110.0" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="110.0,28.0 107.0,21.7 113.0,21.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="110.0" y="10" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i：最右的升序对</text>
<line x1="130.0" y1="64" x2="130.0" y2="70" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="290.0" y1="64" x2="290.0" y2="70" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="130.0" y1="64" x2="290.0" y2="64" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="210.0" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">右侧降序</text>
<line x1="230.0" y1="14" x2="230.0" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230.0,28.0 227.0,21.7 233.0,21.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="230.0" y="10" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<rect x="50" y="110" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="110" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="130" y="110" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="170" y="110" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="190.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="210" y="110" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="230.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="250" y="110" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="270.0" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="10" y="128" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结果</text>
<text x="170" y="158" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">交换 a[i]、a[j]（右侧刚好更大的），再把右侧反转成升序</text>
</svg>

```python
def next_permutation(a):
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:   # 最右的升序对
        i -= 1
    if i >= 0:
        j = len(a) - 1
        while a[j] <= a[i]:              # 右侧从右数第一个比 a[i] 大的
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])      # 右侧本是降序，反转成升序
    return a                             # i = -1 时整体反转
```

**要点。**
- 为什么对？：`a[i+1:]` 是降序，已是这段的最大排列，要变大只能动 `a[i]`；换上刚好更大的数，右侧再取最小（升序），就是下一个。
- LC 60 怎么改？：阶乘进制：固定首位后每块有 `(n-1)!` 个排列，`divmod(k-1, (n-1)!)` 得首位在剩余数字里的排名，余数继续往下。
- LC 1823 怎么改？：约瑟夫环：列表存人，淘汰下标是 `(idx + k - 1) % 人数`，弹出后同一下标就是下一轮起点。
- LC 1073 / 2145 怎么改？：1073 像二进制竖式从低位加，进位改为 `-(sum >> 1)`，最后去前导零；2145 的前缀和固定了形状，起点能平移的个数是 `(upper - lower) - (max - min) + 1`，不足则为 `0`。

**易错点。**
- 比较写成 `a[i] > a[i+1]` 才停：重复元素 `[1,1,5]` 需要 `>=` 跳过相等，否则找错位置。
- 已是最大排列：`[3,2,1]` 应回到 `[1,2,3]`，`i = -1` 时别漏掉整体反转。
- 60 的 `k` 从 `1` 起算：先 `k -= 1` 再 `divmod`。

**对应题目。** LC 1073 负二进制数相加、LC 2145 统计隐藏数组数目、LC 1823 找出游戏的获胜者、LC 31 下一个排列、LC 60 排列序列
