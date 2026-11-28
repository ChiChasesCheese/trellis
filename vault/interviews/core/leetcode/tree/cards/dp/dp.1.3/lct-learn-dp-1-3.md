---
id: lct-learn-dp-1-3
node: dp.1.3
type: qa
step: 1
---
## Q
**动态规划 › 入门 DP › 最大子数组和（最大子段和）**｜学习卡

套路是什么？

## A
**一句话。** Kadane：以 `i` 结尾的最优子段只有「接在前一段后面」或「自己重开」两种，一遍扫描滚动；乘积要同时维护最大和最小。

下图：`cur` 是以当前位置结尾的最大和；前面的段为负就丢掉重开。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="4" y="38" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x</text>
<rect x="26" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="60" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="94" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="128" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="162" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="196" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="213.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="230" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="264" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-5</text>
<rect x="298" y="20" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="315.0" y="38.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<text x="4" y="82" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cur</text>
<rect x="26" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="60" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="94" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="128" y="64" width="34" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="162" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="196" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="213.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="230" y="64" width="34" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="247.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<rect x="264" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="298" y="64" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="315.0" y="82.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<text x="145" y="108" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">前面 -2 &lt; 0：重开</text>
<text x="247" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">best = 6</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cur = max(cur, 0) + x</text>
</svg>

```python
def max_subarray(nums):
    best = cur = nums[0]         # cur：以当前位置结尾的最大和
    for x in nums[1:]:
        cur = max(cur, 0) + x    # 前面为负就丢掉，自己重开
        best = max(best, cur)
    return best

def max_product(nums):
    best = hi = lo = nums[0]     # 以当前位置结尾的最大/最小积
    for x in nums[1:]:
        c = (x, hi * x, lo * x)  # 重开 / 接最大 / 接最小
        hi, lo = max(c), min(c)
        best = max(best, hi)
    return best
```

**要点。**
- 为什么对？：以 `i` 结尾的最优只取决于以 `i-1` 结尾的最优：前面的和为负就是拖累，丢掉重开；答案是所有结尾位置里的最大值。
- LC 152 怎么改？：负数会让最小积翻成最大积，所以同时记 `hi`、`lo`，每步从「重开 / 接最大 / 接最小」三选。
- LC 918 怎么改？：不跨首尾就是普通 Kadane，跨首尾等于总和减去中间最小子段，两者取大；全为负时最小子段就是全数组，要直接返回 Kadane 的结果。
- LC 1186 怎么改？：多一维状态：`keep` 没删过的最大和，`skip` 至多删一个：`skip = max(skip + x, 旧 keep)`（删掉 `x`），`keep = max(keep, 0) + x`。

**易错点。**
- `best` 初值写 `0`：`[-2]` 应得 `-2`，子段不能为空。
- LC 918 全负不特判：`[-3,-2,-3]` 的 `总和 - 最小段` 是空段，得 `0`，应为 `-2`。
- LC 1186 先更新 `keep` 再算 `skip`：「删 `x`」用到了含 `x` 的 `keep`，`[1,-5,1]` 得 `1`，应为 `2`。

**对应题目。** LC 152 乘积最大子数组、LC 918 环形子数组的最大和、LC 1186 删除一次得到子数组最大和
