---
id: problems-unique-id-generator-sign-bit-boundary
node: problems.foundations.unique-id-generator
type: qa
step: 8
tags: [grown]
---
## Q
In a 64-bit ID packed as 41 timestamp bits + 13 worker-id bits + 10 sequence bits (summing to exactly 64, with no bit reserved as an explicit sign bit), why does this layout only guarantee the ID reads as a non-negative signed 64-bit integer for about 34.9 years after the custom epoch, rather than for the full ~69.7-year life of the 41-bit timestamp field?

## A
With all 64 bits consumed by timestamp, worker id, and sequence, there is no bit left to reserve explicitly as a sign bit the way a design with a separate 1-bit sign field (like the original Twitter Snowflake's 1+41+10+12 layout) would. Instead, non-negativity depends entirely on the top bit of the 41-bit timestamp field (which is also the top bit of the full 64-bit value) staying 0 — true only while elapsed milliseconds since the epoch stay under 2^40, or about 34.9 years, exactly half of the timestamp field's full 2^41-millisecond (~69.7-year) range. After that point, the same 64-bit value could be interpreted as negative by languages using signed 64-bit integers unless it is explicitly treated as unsigned, making this an earlier practical constraint than the timestamp field's full exhaustion.

## Q zh
在一个由 41 位时间戳 + 13 位 worker id + 10 位序列号拼成、恰好用满 64 位（没有额外预留符号位）的 ID 布局里，为什么这个方案只能保证 ID 在自定义纪元之后约 34.9 年内被解读为非负的有符号 64 位整数，而不是覆盖 41 位时间戳字段约 69.7 年的全部寿命？

## A zh
因为 64 位已经被时间戳、worker id 和序列号全部用完，没有位可以像原版 Twitter Snowflake（1+41+10+12 布局）那样显式预留一个符号位。非负性完全依赖 41 位时间戳字段的最高位（同时也是整个 64 位值的最高位）保持为 0——这只在自纪元以来经过的毫秒数小于 2^40（约 34.9 年，正好是时间戳字段 2^41 毫秒即约 69.7 年全部寿命的一半）时成立。过了这个时间点，同一个 64 位数值在使用有符号 64 位整数的语言里可能被解读为负数，除非显式按无符号处理——这是一个比时间戳字段完全耗尽更早到来的现实约束。
