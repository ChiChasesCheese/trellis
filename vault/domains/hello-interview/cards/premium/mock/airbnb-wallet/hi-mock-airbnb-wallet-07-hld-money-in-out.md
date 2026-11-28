---
id: hi-mock-airbnb-wallet-07-hld-money-in-out
node: fix.airbnb-wallet-mock
type: qa
step: 7
---
## Q
**Airbnb Wallet · 第 7 步 · 高层设计：充值与提现**｜模拟面试

面试官：「好。现在画高层设计：充值和提现各怎么走？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先画两个盒子：** 「无状态的钱包服务，加一个 Postgres 主库；支付平台在外面。别的组件，等我说出它的作用、代价和触发条件再加。」
- **为什么是 Postgres：** 「作用：钱包和交易要在同一个事务里一起改，读要按时间有序。代价：写只能落在一个主库。触发条件：写持续超过 10,000 行/秒或存储超过 10 TB 才要换，我们是 250 行/秒、3.6 TB。」
- **提现，五步：** 「① 一个事务里：写 pending 交易，并且用条件 UPDATE 把金额从可用挪到冻结，提交。② 事务之外，调平台 createTransfer，幂等键是 transaction_id。③ 把返回的 vendor_transfer_id 存回这一行。④ 返回 202 pending。⑤ 平台完成时发 webhook，服务在一个事务里改状态并改余额。」
- **为什么先写后调：** 「如果平台收下了请求而本地没有记录，之后的回调和重试都对应不到我们的账。先写 pending 行，平台一接触到钱，本地就已经有记录可以对账。」
- **为什么不在事务里调平台：** 「一个 1 秒的外部调用放进事务，会占着连接和钱包行的锁；平台一慢，所有人的钱包行都被锁住。所以调用在事务之外，崩溃的缝隙由后面的对账补。」
- **充值，方向相反：** 「先写 pending，调平台发起收款；平台确认之后，一个事务里把状态改成 completed 并给 ready_to_use 加钱。确认之前不动余额。」
- **现在不画的：** 「队列、缓存、Kafka、扫描。我讲到需要它们的那个问题时再加，并且说明它的作用、代价和触发条件。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 272">
<rect x="8" y="8" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">App · 网页</text>
<text x="58" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">attempt_id</text>
<rect x="120" y="8" width="212" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">钱包服务（无状态 · 多实例）</text>
<text x="226" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">含 webhook 入口</text>
<polyline points="108,28 120,28" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="120,28 113.0,31.2 113.0,24.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M8,102 a75,6 0 0 1 150,0 v84 a75,6 0 0 1 -150,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M8,102 a75,6 0 0 0 150,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Postgres 主库</text>
<text x="83" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">wallets</text>
<text x="83" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">transactions</text>
<rect x="192" y="96" width="140" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="262" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台（vendor）</text>
<text x="262" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">外部 · 慢 · 会丢</text>
<polyline points="140,48 140,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140,96 136.8,89.0 143.2,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="140,48 143.2,55.0 136.8,55.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="134" y="76" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SQL</text>
<polyline points="262,48 262,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,96 258.8,89.0 265.2,89.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="262,48 265.2,55.0 258.8,55.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="256" y="76" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">createTransfer</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">● 同步路径：写本地事务 → 调平台 → 返回 pending</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">● 异步路径：平台 webhook 回到同一个服务</text>
<text x="8" y="260" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">● 现在只有两个盒子，别的等讲到再加</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 326">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">钱包服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提现（先扣后确认）</text>
<text x="48" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST {attempt_id}</text>
<polyline points="44,104 128,104" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,104 121.0,107.2 121.0,100.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 一个事务：冻结 + pending</text>
<polyline points="128,138 212,138" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,138 205.0,141.2 205.0,134.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="294" y="160" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② createTransfer(key = txn_id)</text>
<polyline points="128,172 298,172" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,172 291.0,175.2 291.0,168.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 存 vendor_transfer_id</text>
<polyline points="128,206 212,206" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,206 205.0,209.2 205.0,202.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202 pending</text>
<polyline points="128,240 44,240" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,240 51.0,236.8 51.0,243.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ webhook：completed / failed</text>
<polyline points="298,274 128,274" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,274 135.0,270.8 135.0,277.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="296" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑤ 同一事务：改状态 + 改余额</text>
<polyline points="128,308 212,308" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,308 205.0,311.2 205.0,304.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="80" x2="44" y2="322" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="81" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="96" x2="128" y2="149" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="164" x2="128" y2="322" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="115" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="130" x2="212" y2="149" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="164" x2="212" y2="183" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="198" x2="212" y2="251" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="266" x2="212" y2="285" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="300" x2="212" y2="322" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="115" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="130" x2="298" y2="251" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="266" x2="298" y2="285" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="300" x2="298" y2="322" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 237">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">充值与提现：钱的方向相反，规则相反</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">提现：先扣后确认</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发起时 ready → on_hold（已提交）</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">确认后 on_hold 减；失败再退回</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">充值：先确认后加</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发起时只写 pending，不动余额</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">平台确认后 ready_to_use 加</text>
<rect x="8" y="164" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">共同点：都先写本地 pending 行</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">平台一接触到钱，本地就有记录</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后结果走同一个状态转换</text>
</svg>
白板上新增：钱包服务、Postgres、平台三个盒子，提现的五步时序，和充值提现方向相反的对照。
**为什么这样说。** （约 6 分钟，累计第 24 分钟。）面试官看你的第一版是不是最小的、能跑通的，以及关键顺序有没有说对：先冻结、先写 pending、事务之外调平台、返回 pending。强的回答在画每个盒子时说出它的作用、代价、触发条件；弱的回答是一口气画出队列、缓存、Kafka，却讲不出任何一个的理由。
**面试官可能接着问。**
- 为什么 POST 不等平台完成再返回？ → 平台完成要几分钟，同步等会占着连接，用户也看不到中间状态。返回 pending，用户随时读状态。
- 平台调用超时了怎么办？ → 行留在 pending，不当失败、不退回冻结。怎么查清，放在深入二里讲。
- 冻结为什么发生在调平台之前？ → 之后每一步都可能失败或卡住；钱先被圈住，才不会被另一笔提现花掉。
- 要不要用消息队列把提现异步化？ → 现在不用。峰值 50 笔/秒，每次调用约 1 秒，只有 50 个在飞，同步调用够。队列的作用是削峰，代价是多一个要运维的组件和重复消息，触发条件是在飞的调用逼近平台额度，或平台长时间变慢。
**常见失分。**
- **在数据库事务里调平台：** 占着锁和连接，平台一慢就拖垮整个钱包。
- **先调平台再写库：** 平台收了钱而本地没有记录，之后无法对账。
- **充值立刻加余额：** 用户会花掉还没到账的钱。
- **一上来就画 Kafka：** 说不出它的作用、代价和触发条件，后面被追问时没有地方退。
