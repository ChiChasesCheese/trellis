---
id: lct-learn-greedy-5-3
node: greedy.5.3
type: qa
step: 1
---
## Q
**贪心算法 › 思维题 › 等价转化**｜学习卡

套路是什么？

## A
**一句话。** 等价转化：把操作、排序或分组换成一个等价但更简单的描述，贪心就缩成求和、计数或排序。

下图：左边的原描述都等价于右边更简单的描述，贪心随之变成求和、计数或排序。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="10" y="14" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="32" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">n-1 个数各 +1</text>
<rect x="200" y="14" width="130" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="32" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 个数 -1</text>
<line x1="146" y1="28" x2="194" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194.0,28.0 187.7,31.0 187.7,25.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="146.0,28.0 152.3,25.0 152.3,31.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="10" y="52" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">分成 k 段</text>
<rect x="200" y="52" width="130" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">选 k-1 个切点</text>
<line x1="146" y1="66" x2="194" y2="66" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194.0,66.0 187.7,69.0 187.7,63.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="146.0,66.0 152.3,63.0 152.3,69.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="10" y="90" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">排序后的下标</text>
<rect x="200" y="90" width="130" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数比 t 小的个数</text>
<line x1="146" y1="104" x2="194" y2="104" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194.0,104.0 187.7,107.0 187.7,101.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="146.0,104.0 152.3,101.0 152.3,107.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="10" y="128" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">互为异位词</text>
<rect x="200" y="128" width="130" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">排序后相同</text>
<line x1="146" y1="142" x2="194" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="194.0,142.0 187.7,145.0 187.7,139.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="146.0,142.0 152.3,139.0 152.3,145.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>

```python
def min_moves(nums):             # LC 453：n-1 个加 1 ≡ 1 个减 1
    return sum(nums) - min(nums) * len(nums)

def put_marbles(w, k):           # LC 2551：切点贡献 w[i]+w[i+1]
    cuts = sorted(a + b for a, b in pairwise(w))
    m = len(cuts) - (k - 1)
    return sum(cuts[m:]) - sum(cuts[:k - 1])   # 最大 - 最小

def target_indices(nums, t):     # LC 2089：排序后的位置靠数数
    less = sum(x < t for x in nums)
    return list(range(less, less + nums.count(t)))

def group_anagrams(strs):        # LC 49：异位词 ≡ 排序后相同
    g = defaultdict(list)
    for s in strs:
        g["".join(sorted(s))].append(s)
    return list(g.values())
```

**要点。**
- 为什么这么转？：改写后的问题里要决定的东西更少：453 只剩「每个数降到最小值」，2551 只剩「选哪 `k-1` 个切点」，2089 的位置由比它小的个数决定。
- LC 2551 为什么首尾能抵消？：每个背包价格是首尾之和，`w[0]` 和 `w[-1]` 一定各算一次；最大与最小分数的差只来自 `k-1` 个切点，取最大 `k-1` 个减最小 `k-1` 个。
- LC 49 的键怎么选？：面试先写排序键（`O(L log L)`）；字符集小的话换成 26 个计数的元组；`frozenset` 会丢重复次数。

**易错点。**
- LC 2551 写 `cuts[-(k - 1):]`：`k = 1` 时变成 `cuts[-0:]`，是整个列表，应为 `0`。
- LC 2089 起点用 `x <= t` 计数：`[1,2,5,2,3]`、`t = 2` 得 `[3,4]`，应为 `[1,2]`。
- LC 453 与 LC 462 混淆取中位数：`[1,2,3]` 得 `2`，应为 `3`。

**对应题目。** LC 453 最小操作次数使数组元素相等、LC 2551 将珠子放入背包中、LC 2089 找出数组排序后的目标下标、LC 49 字母异位词分组
