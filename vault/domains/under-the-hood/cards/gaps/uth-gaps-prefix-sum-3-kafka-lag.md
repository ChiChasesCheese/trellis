---
id: uth-gaps-prefix-sum-3-kafka-lag
node: gaps.prefix-sum
type: qa
step: 3
---
## Q
**消费延迟 lag 为什么是一次减法**｜Kafka · 4.0 kafka-consumer-groups

`kafka-consumer-groups.sh --describe` 里的 LAG 是怎么算的？分区里积压了上百万条消息，要逐条数吗？

## A
**结构。** 分区是只追加的日志，每条消息有个递增编号，叫偏移量（offset）：0、1、2……「写到哪了」是末尾偏移量（log end offset）；「读到哪了」是消费组提交的偏移量（committed offset，即下一条要读的编号）。两者都是累计位置，和计数器同理：积压 = 末尾 − 已提交。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 168">
<text x="170" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">一个分区 只追加的日志</text>
<rect x="30" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0</text>
<rect x="58" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">1</text>
<rect x="86" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">2</text>
<rect x="114" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">3</text>
<rect x="142" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="156" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4</text>
<rect x="170" y="44" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">5</text>
<rect x="198" y="44" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<rect x="226" y="44" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="240" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">7</text>
<rect x="254" y="44" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="268" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">8</text>
<rect x="282" y="44" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="296" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">9</text>
<line x1="198" y1="104" x2="198" y2="80" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M198,74 L194.5,81 L201.5,81 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="310" y1="104" x2="310" y2="80" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M310,74 L306.5,81 L313.5,81 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="198" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已提交 6</text>
<text x="304" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">末尾 10</text>
<line x1="198" y1="138" x2="310" y2="138" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="198" y1="133" x2="198" y2="143" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="310" y1="133" x2="310" y2="143" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">lag = 10 - 6 = 4</text>
</svg>
```

**细节。**

- 工具源码 `getLag` 就是 `logEndOffset - offset`
- 从没提交过（偏移量 -1）时不算 lag，该列显示 `-`
- 每个分区一行，整个消费组的积压要自己相加

**坑。** 偏移量是编号，不是条数。日志压缩（log compaction）删掉旧消息后编号留下空洞，相减得到的是位置差，可能比真正待读的条数大。

**例题：** LC 724 寻找数组的中心下标（同类：LC 303 区域和检索）

给整数数组 `nums`，找一个下标，使它左边所有元素之和等于右边所有元素之和（下标本身不计入）；有多个返回最靠左的，没有返回 -1。例：`nums = [1,7,3,6,5,6]` → 3（左 1+7+3 = 11，右 5+6 = 11）。

```python
def find_pivot_index(nums: list[int]) -> int:
    total = sum(nums)
    left_sum = 0
    for i, x in enumerate(nums):
        if left_sum == total - left_sum - x:
            return i
        left_sum += x
    return -1
```
