---
id: hi-sdx-tinder-gate-margin
node: sd.problem-breakdowns.tinder.more
type: qa
step: 1
---
## Q
**匹配判定的单个 Redis 够不够**｜补充 · 约会应用（Tinder） · 追问

面试官：「滑动峰值每秒约 5.2 万次，其中 20% 是右滑，每次右滑都要在 Redis 里做一次原子的『对方右滑过吗』判定。单个 Redis 按官方文档 redis-benchmark 的示例（SET）约每秒 18 万次，够吗？日活涨 10 倍呢？」

## A
**结论。** 现在够：右滑峰值约 1.04 万次/秒，余量约 17 倍，单实例即可。涨到 10 倍，峰值约 10.4 万次/秒，余量只剩约 1.7 倍，抖动或慢命令就会吃光，要改成按用户对（排序后的两个 ID）哈希分片的 Redis 集群。

**要点。**
- **现在：** 峰值 5.2 万次/秒（约为日均 2.3 万次/秒的 2.25 倍）× 20% ≈ 1.04 万次/秒，18 万 ÷ 1.04 万 ≈ 17.3 倍余量。
- **10 倍：** 峰值 10.4 万次/秒，余量 18 万 ÷ 10.4 万 ≈ 1.73 倍。
- **不要过度拆分：** 余量接近 1 的单个热点键才需要特殊处理；17 倍余量的匹配判定不需要，不是所有单键原子操作都要拆分。
- **分片依据：** 键本来就是排序后的用户对，同一对用户永远落在同一分片，原子性不受影响。
- **别忘了脚本更重：** 判定是写加读的 Lua 脚本，比基准里的单纯 SET 重；而且基准数字随硬件和命令而变，只能当量级，实际余量比算出来的小，要再留余量。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单个 Redis 能力：约 18 万次/秒</text>
<rect x="10" y="24" width="300" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="160.0" y="39.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">容量 180,180</text>
<text x="10" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">现在：右滑峰值约 1.04 万次/秒（余量 17.3 倍）</text>
<rect x="10" y="78" width="17" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 倍：约 10.4 万次/秒（余量只有 1.73 倍）</text>
<rect x="10" y="132" width="173" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">余量 1.7 倍时抖动、GC、慢命令都会吃光，</text>
<text x="10" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以改成按用户对分片的 Redis 集群。</text>
<text x="10" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">判定脚本比单纯 SET 更重，要再留余量。</text>
</svg>

**为什么。** 用负载除以单实例能力，得到余量；余量大就别过度设计，余量接近 1 就必须分摊。

**面试里这样说。** 「右滑峰值约 1.04 万次每秒，单个 Redis 基准约 18 万，余量 17 倍，所以现在一个实例就够。涨到 10 倍余量只剩 1.7 倍，我按排序后的用户对做哈希分片，同一对用户总在同一分片，原子判定不受影响；而且脚本比 SET 重，我会再留余量。」

**易错。**
- **一上来就分片：** 17 倍余量时分片只增加复杂度。
- **拿 SET 基准当脚本能力：** 脚本做一次写一次读，实际吞吐更低。
- **按单个用户分片：** 一对用户的两次滑动会落在两个分片，失去原子性。
