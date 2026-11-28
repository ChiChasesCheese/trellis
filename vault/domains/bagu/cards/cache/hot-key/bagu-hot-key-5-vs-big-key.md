---
id: bagu-hot-key-5-vs-big-key
node: a.cache.hot-key
type: qa
step: 5
---
## Q
**热 key 与大 key · 区别与处理差异**｜追问

面试官：「热 key 和大 key 有什么区别？处理方法一样吗？」

## A
**基本回答。** 热 key 是访问次数过多，处理思路是把读分摊出去；大 key 是单个值体积过大，处理思路是拆小，并且异步删除。大 key 的经验阈值：String 超过 10KB，Hash、List、Set、ZSet 元素超过 5000 个或总体超过 1MB 就要警惕，超过 10MB 必须处理。两者经常同时出现，但病因不同：一个是「人太多」，一个是「东西太大」。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="86" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">热 key</text>
<text x="254" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大 key</text>
<line x1="64" y1="28" x2="64" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,100.0 60.8,93.0 67.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78" y1="28" x2="78" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,100.0 74.8,93.0 81.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="92" y1="28" x2="92" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92.0,100.0 88.8,93.0 95.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="106" y1="28" x2="106" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="106.0,100.0 102.8,93.0 109.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="120" y1="28" x2="120" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,100.0 116.8,93.0 123.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="56" y="102" width="76" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="94.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">小的值</text>
<line x1="235" y1="28" x2="235" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="235.0,74.0 231.8,67.0 238.2,67.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="275" y1="28" x2="275" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="275.0,74.0 271.8,67.0 278.2,67.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="190" y="76" width="128" height="96" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个很大的值</text>
<text x="254.0" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">String >10KB</text>
<text x="254.0" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或 >5000 元素</text>
<text x="254.0" y="150.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或 >1MB</text>
<text x="86" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">访问次数太多</text>
<text x="86" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分摊读</text>
<text x="254" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单个值体积太大</text>
<text x="254" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拆小、UNLINK 异步删</text>
</svg>
左边：很多请求指向一个小值，问题在次数；右边：只有少量请求，但一个值本身巨大，问题在体积。
**容易错。**
- **以为热 key 和大 key 是一回事：** 热是次数多，大是体积大；一个小而热的 key 不是大 key，一个大而冷的 key 也不是热 key。
- **用 DEL 删大 key：** 会同步释放内存阻塞主线程，要用 `UNLINK` 异步删，集合类用 `HSCAN`、`SSCAN` 分批取出再 `HDEL`、`SREM`，ZSet 可用 `ZREMRANGEBYRANK` 分段删。
- **只拆不分流：** 拆成小 key 解决了体积，但某个分片仍然很热时，还要做读分流。
- **让集合无限增长：** 不设元素上限，迟早自己制造出大 key。
**举个例子。** 头部主播的粉丝 Set 有 100 万成员，既热又大：`SMEMBERS` 一次取 100 万个会阻塞单线程。按 `hash(用户ID) % 256` 拆成 256 个小 Set，每个约 3900 个，低于 5000 的阈值，判断是否粉丝先算分片再 `SISMEMBER`；热的读走几秒本地缓存或 key 副本。
