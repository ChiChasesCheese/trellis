---
id: bagu-penetration-1-penetration
node: a.cache.penetration
type: qa
step: 1
---
## Q
**缓存穿透 · 是什么、怎么挡**｜必会

面试官：「接口被人用随机 userId 狂刷，缓存里永远没有，每次都打到数据库。这叫什么？怎么解决？」

## A
**基本回答。** 这是缓存穿透（Cache Penetration）：查的数据在缓存和数据库里都不存在，缓存永远建不起来，每次请求都落到数据库。要用三道防线：入口参数校验（ID 格式、范围非法的在网关直接拒绝，成本最低）、缓存空值（库里查不到也写一个空标记，TTL 设短 30–60 秒）、布隆过滤器（Bloom filter，预先放进所有真实 ID，说「不存在」一定对）。分工：参数校验挡明显非法的，布隆挡格式合法但数量巨大的随机 ID，空值缓存兜住漏过来的（如布隆误判放行、已经查过一次的 ID）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="6" width="150" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求：userId=随机值</text>
<line x1="85" y1="36" x2="85" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,58.0 81.8,51.0 88.2,51.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="58" width="150" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关：参数校验</text>
<line x1="85" y1="88" x2="85" y2="110" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,110.0 81.8,103.0 88.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="172" y="77" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">格式非法 → 直接拒绝</text>
<rect x="10" y="110" width="150" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">布隆过滤器</text>
<line x1="85" y1="140" x2="85" y2="162" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,162.0 81.8,155.0 88.2,155.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="172" y="129" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说「不存在」→ 直接返回</text>
<rect x="10" y="162" width="150" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis：空值缓存</text>
<line x1="85" y1="192" x2="85" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,214.0 81.8,207.0 88.2,207.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="172" y="181" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中空标记 → 返回空</text>
<rect x="10" y="214" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="233.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="172" y="233" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有真实 ID 会到这里</text>
</svg>
请求从上往下一关一关过：每一关都能把「不存在的 ID」挡掉，只有真实 ID 才会走到数据库。
**容易错。**
- **以为穿透是缓存过期：** 过期是数据存在、缓存暂时失效（那叫击穿）。穿透是数据本来就不存在。
- **以为只缓存空值就够了：** 随机 ID 每次都不一样，每个都要落库一次再写一条空标记，数据库照样被打满，内存也被空标记撑大。
- **把布隆的「存在」当成真的存在：** 它可能误判，只能用来挡「不存在」。误判的请求只是正常去查缓存和库，不会出错。
- **空值 TTL 越长越好：** 太长会占内存，数据后来被创建时还会一直查到空，所以只设 30–60 秒。

