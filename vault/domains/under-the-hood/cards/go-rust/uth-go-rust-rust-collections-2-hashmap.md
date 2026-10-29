---
id: uth-go-rust-rust-collections-2-hashmap
node: go-rust.rust-collections
type: qa
step: 2
---
## Q
**Rust 的 HashMap 为什么既快又防攻击**｜Rust · hashbrown 0.17

标准库 `HashMap` 底下用什么表？默认哈希函数是哪个？

## A
**背景。** 哈希表要快，哈希函数要便宜；但如果它可预测，攻击者就能构造一批全冲突的 key，让每次操作退化成 O(n)（哈希洪泛，HashDoS）。Rust 既要快，又要默认就安全。

**结构。** 直接用 hashbrown 的瑞士表（SwissTable）：控制字节数组加槽位数组，开放寻址，二次探测。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">hashbrown: 控制字节 + 槽位, 一次扫一整组</text>
<rect x="10" y="26" width="32" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="26" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2a</text>
<rect x="46" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="62" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<rect x="82" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="98" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7b</text>
<rect x="118" y="26" width="32" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="134" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2a</text>
<rect x="154" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="170" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<rect x="190" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="206" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">05</text>
<rect x="226" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="242" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">80</text>
<rect x="262" y="26" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="278" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<text x="8" y="66" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ff = 空, 80 = 已删除, 其余 = 哈希高 7 位</text>
<text x="8" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">x86 SSE2 一次扫 16 个, aarch64 NEON 一次扫 8 个</text>
<text x="8" y="104" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">组内没找到, 二次探测 (步长 1, 2, 3 ...) 去下一组:</text>
<rect x="10" y="124" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="40" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组 0</text>
<rect x="80" y="124" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="110" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组 1</text>
<rect x="150" y="124" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="180" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组 2</text>
<rect x="220" y="124" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="250" y="140.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组 3</text>
<path d="M40 124 C 40 116 105 116 105 124" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="105,124 102.3,118.0 107.7,118.0" style="fill:var(--accent,#3b6fd4)"/>
<path d="M110 150 C 110 170 250 170 250 150" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="250,150 252.7,156.0 247.3,156.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="198" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">负载因子 7/8; 默认哈希 SipHash 1-3, 每个 map 随机种子</text>
</svg>
```

**细节。**

- 每个槽对应 1 个控制字节：空、已删除，或哈希高 7 位
- x86 的 SSE2 一次扫 16 个控制字节，aarch64 的 NEON 一次扫 8 个
- 负载因子 7/8，实测容量依次为 `3 7 14 28 56 112`
- 默认哈希是 SipHash 1-3，每个 map 随机种子，实测两个 map 遍历顺序不同

**为什么。** SipHash 对整数等短键不是最快，但能抵御哈希洪泛；要速度可换哈希器。

**例题：** LC 560 和为 K 的子数组（同类：LC 1 两数之和）

给整数数组 `nums` 和整数 `k`，统计和为 `k` 的连续子数组个数。例：`[1,1,1]`、`k = 2` → `2`。用哈希表记下每个前缀和出现过几次，每走一步就查一次 `前缀和 - k`。

```python
from collections import Counter

def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```
