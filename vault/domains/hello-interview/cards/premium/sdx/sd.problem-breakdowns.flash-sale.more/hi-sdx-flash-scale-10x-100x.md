---
id: hi-sdx-flash-scale-10x-100x
node: sd.problem-breakdowns.flash-sale.more
type: qa
step: 1
---
## Q
**抢购规模再涨 10 倍、100 倍**｜补充 · 限时抢购 · 追问

面试官：「你的抢购系统有准入控制，放行速率压在下游能承受的几千次/秒。买家从 100 万涨到 1000 万，库存还是 1000 件，库存热键的压力怎么变？再涨到全平台大促、几千个商品同时开抢，瓶颈又在哪？」

## A
**结论。** 买家涨 10 倍，热键的负载不变：放行速率由下游存储的容量决定，和排队的人数无关，增长全部落在无状态、可水平扩展的准入层和候场室。涨到几千个商品同时开抢，单个热键不会更热，瓶颈转到共享的入口：边缘限流、CDN、令牌验签。

**要点。**
- **10 倍：热键不变：** 准入把进入库存的请求压到固定速率，买家再多也只是排队更长，每人中签概率更低。
- **10 倍：候场室变重：** 轮询状态的请求变成 10 倍，候场室独立部署，按用户分片、水平扩。
- **100 倍：计数器天然分散：** 几千个商品的库存计数器按键哈希落到集群的不同分片，没有哪个分片同时承担多个爆款。
- **100 倍：入口是共享的：** 边缘限流器、CDN、令牌验签要按全平台总流量配置容量。
- **逐商品限速：** 识别特别热的商品，单独限速，避免一个爆款占满共享的放行额度，挤掉其他商品。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="10" y="8" width="320" height="50" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100 万买家，1 千件库存</text>
<text x="170.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">热键速率 = 下游容量，约数千次/秒</text>
<polyline points="170,58 170.0,65.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,72 166.8,65.0 173.2,65.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="72" width="320" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="93.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000 万买家（10 倍）</text>
<text x="170.0" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">热键速率不变；候场室轮询 ×10</text>
<polyline points="170,122 170.0,129.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,136 166.8,129.0 173.2,129.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="136" width="320" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">平台级 100 倍：数千个 SKU</text>
<text x="170.0" y="172.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">计数器分散到各分片，瓶颈在入口</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入口按总流量配置；逐个 SKU 限速，</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">防止一个爆款占满共享的放行额度</text>
</svg>

**为什么。** 热键是不能靠分片消除的单点，所以必须在它前面把速率压住；压住之后，流量增长只会改变排队的人数，不再改变热键的负载。真正随规模增长的是入口这一层。

**面试里这样说。** 「买家涨十倍我不动库存那一层，放行速率由数据库容量定，只扩候场室和准入层；做成平台级大促，每个商品的计数器落在不同分片，我要加的是边缘和 CDN 的容量，以及按商品限速，免得一个爆款吃掉全站的放行额度。」

**易错。**
- **以为买家多热键就更热：** 准入之后热键速率与买家数无关。
- **放行速率按买家数定：** 应该按下游容量定，再留余量。
- **平台级大促只盯库存分片：** 库存分得开，入口分不开。
