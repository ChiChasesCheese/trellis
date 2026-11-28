---
id: lct-learn-greedy-2-5
node: greedy.2.5
type: qa
step: 1
---
## Q
**贪心算法 › 区间贪心 › 合并区间**｜学习卡

套路是什么？

## A
**一句话。** 合并区间：按起点排序，只和结果里最后一个区间比较，重叠就延长终点，否则另起一个；同一思路还管插入、求空闲、字符串划分。

下图：LC 56，按起点排序后，每个区间只和结果里最后一个区间比较。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="55" y="20" width="30" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="51" y="32" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,3]</text>
<rect x="70" y="44" width="60" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="66" y="56" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,6]</text>
<rect x="160" y="68" width="30" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="156" y="80" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[8,10]</text>
<rect x="265" y="92" width="45" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="261" y="104" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[15,18]</text>
<rect x="55" y="120" width="75" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="160" y="120" width="30" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="265" y="120" width="45" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="10" y="131" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结果</text>
<line x1="40" y1="142" x2="310" y2="142" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="40" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="85" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="130" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="175" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<text x="220" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<text x="265" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">15</text>
<text x="310" y="156" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">18</text>
<text x="230" y="52" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">只和结果最后一个比</text>
<text x="230" y="68" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">重叠就延长终点</text>
</svg>

```python
def merge(intervals):
    ans = []
    for l, r in sorted(intervals):       # 按起点排序
        if ans and l <= ans[-1][1]:      # 端点相接也算重叠
            ans[-1][1] = max(ans[-1][1], r)
        else:
            ans.append([l, r])
    return ans
```

**要点。**
- 为什么对？：起点有序，后来的区间只可能与「当前合并段」重叠，所以只看最后一段；终点要取 `max`，因为被包含的区间不能把终点拉回去。
- LC 57 怎么改？：列表已有序，不用排序：线性扫三段，终点 `< 新起点` 的原样放，重叠的并入新区间（取 `min` 起点、`max` 终点），其余原样放。
- LC 759、616 怎么改？：759：所有员工的区间摊平排序，下一段起点 `> reach`（目前最晚结束）就是共同空闲；616：先标出每个字符是否被某个单词覆盖，连续被覆盖的一段首尾放标签。
- LC 55、763 怎么改？：都是「维护最远边界」：55 扫描时 `reach = max(reach, i + nums[i])`，`i > reach` 就卡住；763 记每个字母最后位置，`end = max(end, last[c])`，`i == end` 时切一刀。

**易错点。**
- 重叠条件写 `<`：`[[1,4],[4,5]]` 得两段，应为 `[[1,5]]`。
- 延长终点不取 `max`：`[[1,4],[2,3]]` 得 `[[1,3]]`，应为 `[[1,4]]`。
- LC 759 的 `reach` 直接赋成当前终点：`[[1,10]]` 与 `[[2,3],[5,6]]` 会错误产生空闲 `[3,5]`。

**对应题目。** LC 56 合并区间、LC 57 插入区间、LC 759 员工空闲时间、LC 616 给字符串添加加粗标签、LC 55 跳跃游戏、LC 763 划分字母区间
