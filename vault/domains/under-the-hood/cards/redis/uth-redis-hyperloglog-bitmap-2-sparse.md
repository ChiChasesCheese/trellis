---
id: uth-redis-hyperloglog-bitmap-2-sparse
node: redis.hyperloglog-bitmap
type: qa
step: 2
---
## Q
**HyperLogLog 刚创建时有多大**｜Redis · HyperLogLog

只加了几百个元素的 HLL，也要占 12KB 吗？

## A
**背景。** 刚创建的 HLL 里，16384 个寄存器几乎全是 0，白白占 12KB 很浪费。办法：不逐个记，把“连续一长串相同的值”合并成一条，比如“连续 3000 个 0”写成一条记录。这叫游程编码（run-length encoding）。

**结构。** 先用稀疏编码（sparse）：对寄存器做游程编码。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">稀疏编码: 对 16384 个寄存器做游程压缩</text>
<text x="8" y="38" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空的 HLL:</text>
<rect x="10" y="46" width="310" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="165" y="61.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">XZERO 16384</text>
<text x="8" y="92" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加了几个元素后 (示意):</text>
<rect x="10" y="100" width="90" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="55" y="115.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">XZERO 3000</text>
<rect x="100" y="100" width="46" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="123" y="115.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">VAL 3</text>
<rect x="146" y="100" width="56" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="174" y="115.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">ZERO 20</text>
<rect x="202" y="100" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="232" y="115.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">VAL 5 ×2</text>
<rect x="262" y="100" width="58" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="291" y="115.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">XZERO ...</text>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ZERO: 连续 1 到 64 个 0; XZERO: 最多 16384 个 0</text>
<text x="8" y="164" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">VAL: 值 1 到 32, 重复 1 到 4 次</text>
<text x="8" y="186" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 3000 字节或寄存器值 &gt; 32, 转稠密</text>
</svg>
```

**细节。**

- 三种操作码：`ZERO`（连续 1 到 64 个 0）、`XZERO`（最多 16384 个 0）、`VAL`（值 1 到 32，重复 1 到 4 次）
- 空的 HLL 就是一条 `XZERO:16384`
- 平均占用：100 个元素约 267 字节，1000 个约 1882，10000 个约 10591
- 超过 `hll-sparse-max-bytes`（默认 3000）或寄存器值大于 32，转成稠密编码

**为什么。** 小基数时绝大多数寄存器还是 0，压缩划算；基数大了，稀疏的读写开销不值得。

**例题：** LC 443 压缩字符串

给字符数组 `chars`，把每一段连续重复的字符压缩成“字符 + 次数”（次数为 1 时只留字符），原地写回并返回新长度。例：`["a","a","b","b","c","c","c"]` → 长度 `6`，内容 `["a","2","b","2","c","3"]`。这就是游程编码。

```python
def compress(chars: list[str]) -> int:
    write = read = 0
    n = len(chars)
    while read < n:
        char = chars[read]
        run = 0
        while read < n and chars[read] == char:
            read += 1
            run += 1
        chars[write] = char
        write += 1
        if run > 1:
            for digit in str(run):
                chars[write] = digit
                write += 1
    return write
```
