---
id: bagu-penetration-2-null-bloom
node: a.cache.penetration
type: qa
step: 4
---
## Q
**缓存穿透 · 空值与布隆过滤器的局限**｜追问

面试官：「缓存空值有什么缺点？布隆过滤器的局限又是什么？1 亿个 ID 要多大？」

## A
**基本回答。** 空值缓存的缺点：攻击者用大量不同的 key，仍会把内存撑满。布隆过滤器（Bloom filter）的局限：有误判、标准版不能删除、数据变化要同步加入或重建。大小 m = −n·ln p / (ln2)² 位，哈希个数 k = (m/n)·ln2：1 亿个 ID、误判率 1%，每元素约 9.6 位，共约 9.6 亿位，约 120MB，k ≈ 7。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 亿个 ID、误判率 1%</text>
<rect x="8" y="28" width="90" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="53.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">n = 1 亿</text>
<text x="53.0" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">个元素</text>
<line x1="98" y1="45" x2="118" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,45.0 111.0,48.2 111.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="28" width="100" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="168.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每个元素</text>
<text x="168.0" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 9.6 位</text>
<line x1="218" y1="45" x2="238" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,45.0 231.0,48.2 231.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="238" y="28" width="94" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="285.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9.6 亿位</text>
<text x="285.0" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≈ 120MB</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希函数个数 k ≈ 7</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">空值缓存：随机 key 越多，空标记越多</text>
<rect x="8" y="122" width="60" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="38.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a1: 空</text>
<rect x="74" y="122" width="60" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="104.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x9: 空</text>
<rect x="140" y="122" width="60" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">q7: 空</text>
<text x="212" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">……撑满内存</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新用户没进过滤器：</text>
<rect x="8" y="186" width="100" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="204.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新 ID 登录</text>
<line x1="108" y1="200" x2="128" y2="200" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,200.0 121.0,203.2 121.0,196.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="128" y="186" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="178.0" y="204.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过滤器说没有</text>
<line x1="228" y1="200" x2="248" y2="200" stroke-width="1.2" stroke="currentColor"/>
<polygon points="248.0,200.0 241.0,203.2 241.0,196.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="248" y="186" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="290.0" y="204.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">被误拒绝</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">注册成功后要同步写进过滤器</text>
</svg>
上半部分是 1 亿个 ID 怎么算出 120MB；中间是空值缓存被随机 key 撑大；下半部分是新用户没进过滤器就被误拒绝。
**容易错。**
- **以为过滤器大小跟请求量有关：** 大小只由元素个数 n 和目标误判率 p 决定，攻击再猛，过滤器大小不变；空值缓存才会随攻击增长。
- **以为能直接删除一个 ID：** 标准布隆过滤器不能删（多个元素共用位），只能换计数型（每位换成计数器）、布谷鸟（Cuckoo filter）或定期重建。
- **只建一次不再更新：** 新注册用户的 ID 没写进过滤器，第一次登录就被判「不存在」而误拒绝，这是业务错，不只是误判；注册成功后要同步 `add`，过滤器放在进程内存（Guava）或 Redis 位图（RedisBloom）时，多个实例都要收到新增，否则名单不一致。
- **忘了空值也要控制内存：** 空值 key 单独设前缀便于监控，TTL 短，入口先做参数校验。

