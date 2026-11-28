---
id: lct-learn-math-7-8
node: math.7.8
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 摩尔投票法**｜学习卡

套路是什么？

## A
**一句话。** 摩尔投票：保留 `k - 1` 个候选，遇到 `k` 个互不相同的数就一起抵消，出现次数 `> n/k` 的数必然留在候选里，最后再数一遍确认。

下图：LC 169，`k` 个互不相同的数一起抵消，众数一定留在候选里。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="10" y="38" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x</text>
<rect x="60" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="98" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="117.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="136" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="174" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="212" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="250" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="288" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="307.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="10" y="80" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">候选</text>
<rect x="60" y="62" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2:1</text>
<rect x="98" y="62" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="117.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2:2</text>
<rect x="136" y="62" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2:1</text>
<rect x="174" y="62" width="38" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="193.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空</text>
<rect x="212" y="62" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1:1</text>
<rect x="250" y="62" width="38" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="269.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空</text>
<rect x="288" y="62" width="38" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="307.0" y="80.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2:1</text>
<text x="170" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">新数不同于候选且候选已满：一起抵消（k = 2）</text>
<text x="170" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 n/k 次的数抵消不完；最后再数一遍确认</text>
</svg>

```python
def majority_k(nums, k):             # k=2：LC 169，k=3：LC 229
    cand = {}                        # 候选 -> 计数，至多 k-1
    for x in nums:
        if x in cand:
            cand[x] += 1
        elif len(cand) < k - 1:
            cand[x] = 1
        else:                        # k 个不同的数一起抵消
            for y in list(cand):
                cand[y] -= 1
                if cand[y] == 0:
                    del cand[y]
    need = len(nums) // k            # 再数一遍确认
    return [x for x in cand if nums.count(x) > need]
```

**要点。**
- 为什么对？：每次抵消去掉 `k` 个不同的数，一个值的出现次数超过 `n/k`，抵消 `n/k` 轮也消不完它，所以必留在候选里。
- 不要 `O(1)` 空间怎么改？：哈希计数，留下次数 `> n // k` 的值，`O(n)` 空间。

**易错点。**
- 不保证存在时直接返回候选：`[1,2,3]` 的候选是 `3`，要再扫一遍验证次数。
- 阈值写成 `>=`：`[1,1,2,2]` 每个数恰好一半，不算多数；`[1,2,3]` 的 `n // 3 = 1`，`>=` 会返回全部。

**对应题目。** LC 169 多数元素、LC 229 多数元素 II
