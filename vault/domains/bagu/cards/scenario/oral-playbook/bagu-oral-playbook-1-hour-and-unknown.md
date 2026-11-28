---
id: bagu-oral-playbook-1-hour-and-unknown
node: b.scenario.oral-playbook
type: qa
step: 1
---
## Q
**八股面的节奏 · 一小时怎么走、答不出来怎么说**｜追问

面试官：「咱们先聊聊你简历上的 Redis，你们是怎么用的？」之后一路追问，直到你答不上来。这一段八股占技术面前 20 到 30 分钟，或单独一场约 45 分钟。你怎么安排回答，遇到不会的怎么办？

## A
**基本回答。** 约一小时这样走：
- 0 到 5 分钟：面试官挑简历上的组件问怎么用，先答用法和规模（用在哪、数据量、QPS），再准备被追问原理；别一上来背原理，对方想先知道你真的用过。
- 5 到 25 分钟：沿一个主题深挖 4 到 6 层，每个主题准备到四层：机制、为什么、数字或取舍、追问。链条如 Redis 分布式锁 → 锁过期 → 看门狗 → 主从切换丢锁 → RedLock 及批评；Kafka 分区 → 顺序 → 不丢消息 → 重平衡 → 积压。
- 25 到 40 分钟：场景题（QPS 涨 10 倍、磁盘满了、订单重复扣款），没有标准答案，先说判断顺序（看什么指标、怎么缩小范围），再说命令和手段。
- 40 到 50 分钟：语言运行时，只准备自己的主语言，其余了解到能比较；最后 5 分钟是你提问。
被问「为什么用 A」按四步说：A 的特点，同类产品的特点，我的场景，所以选 A。答不出来别编：说「我的理解是……，不确定的是……」，再说怎么查（文档、指标、实验），能用已知原理推就推，并说明如何验证；编错一个细节会让后面的回答都失去可信度。复习顺序：先 Redis、MySQL、缓存、消息队列（占大部分时间，题互相接着问），再幂等与事务、服务保护（支付订单类设计题几乎都落到这里），然后语言运行时，最后网络与 Linux；速记表盖住答案、用一句话说出来，说不出就回去看。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 274">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约一小时：0 到 50 分钟，最后留给提问</text>
<rect x="10" y="24" width="32" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">简历</text>
<rect x="42" y="24" width="128" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="106.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">深挖 4~6 层</text>
<rect x="170" y="24" width="96" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="218.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">场景题</text>
<rect x="266" y="24" width="64" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">运行时</text>
<text x="10" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="42" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="170" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">25</text>
<text x="266" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">40</text>
<text x="330" y="72" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">50</text>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">0–5：答用法和规模，准备被追问原理</text>
<text x="8" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5–25：沿一个主题深挖 4 到 6 层</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">25–40：场景题，先说判断顺序</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">40–50：只准备自己的主语言运行时</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">答不出来：三步，不要编</text>
<rect x="6" y="192" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="218.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我的理解是…</text>
<rect x="122" y="192" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172.0" y="218.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不确定的是…</text>
<rect x="238" y="192" width="96" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="286.0" y="218.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我会这样查</text>
<line x1="106" y1="214" x2="120" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,214.0 113.0,217.2 113.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="222" y1="214" x2="236" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,214.0 229.0,217.2 229.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">给出排查思路也算分</text>
</svg>
上半部分是一小时的节奏：简历切入、深挖、场景题、语言运行时、最后提问；下面是答不出来的三步：先说理解，再说不确定的地方，最后说怎么查。
**举个例子。** 简历写「用 Redis 做打赏防重」：开场答 SET NX 加过期做防重锁，并补上真实 QPS 和数据量；机制层：原子设置、带过期，释放用 Lua 校验持有者；为什么层：锁过期业务没跑完怎么办，看门狗续期；取舍层：主从切换丢锁，异步复制会丢，最终靠数据库唯一键兜底；追问层：RedLock 的争议，时钟和 GC 停顿的批评。答不出时：「我的理解是 RedLock 靠多数派加锁，不确定的是它对时钟漂移的处理，我会去看官方文档和对它的批评。」转场景题「打赏扣款重复」：先说看流水号是否重复、对账单对不对，再说唯一索引和条件更新兜底。
**容易错。**
- **只准备到机制一层：** 追问很快到第三、第四层。
- **平均用力复习：** 先练占大头的主题。
