---
slug: continuous-subarray-sum
---
## Q
**LC 523 连续的子数组和**｜Medium

判断是否存在长度至少为 `2`、和为 `k` 的倍数的连续子数组。

## A
**一句话。** 前缀和对 `k` 取余，同余数的两个前缀之间就是 `k` 的倍数，字典只记余数第一次出现的下标。

**图解。** 前缀和对 `k` 取余，同一余数第二次出现时，两次之间的子数组和是 `k` 的倍数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 150">
<text x="128.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="164.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="200.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="236.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="272.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="92.0" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<rect x="110" y="20" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">23</text>
<rect x="146" y="20" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="164.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="182" y="20" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="218" y="20" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="236.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="254" y="20" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="74" y="58" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="92.0" y="75.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="110" y="58" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="128.0" y="75.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="146" y="58" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="164.0" y="75.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="182" y="58" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="75.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="218" y="58" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="254" y="58" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="37" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<text x="68" y="75" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前缀 % 6</text>
<line x1="148" y1="50" x2="216" y2="50" stroke-width="1.6" style="stroke:var(--accent,#3b6fd4)"/>
<text x="20" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">余数 5 第一次在下标 0，又在下标 2 出现</text>
<text x="20" y="134" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 − 0 = 2 ≥ 2：中间 2 + 4 = 6 是 k 的倍数</text>
</svg>

```python
def check_subarray_sum(nums, k):
    first = {0: -1}     # 余数 -> 最早下标；空前缀余数 0
    prefix = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k
        j = first.setdefault(prefix, i)
        if i - j >= 2:  # 子数组长度 i - j
            return True
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(min(n, k))`。

**易错点。**
- 漏掉 `{0: -1}`：`[2,4]`、`k=6` 得 `false`，应为 `true`。
- 忘了长度至少 `2`：`[6,1]`、`k=6` 下标差为 `1` 就返回会得 `true`，应为 `false`。
- 每次都覆盖下标：丢了最早位置，`[5,0,0]`、`k=7` 得 `false`，应为 `true`。

**追问。**
- `k` 可以为 `0` 吗？：倍数只有 `0`，改成前缀和相等，取余那行写成 `prefix + x`。
- 统计个数（LC 974）？：字典换成计数，`ans += cnt[prefix]`，没有长度限制。

**同模式。** LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组、LC 525 连续数组、LC 437 路径总和 III
