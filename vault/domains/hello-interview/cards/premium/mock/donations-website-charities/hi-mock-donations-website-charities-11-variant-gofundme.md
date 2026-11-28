---
id: hi-mock-donations-website-charities-11-variant-gofundme
node: qb.sd.donations-website-charities.mock
type: qa
step: 11
---
## Q
**限时捐款网站 · 第 11 步 · 如果题目是 Design GoFundMe：只说变化**｜模拟面试

面试官：「如果换成设计 GoFundMe 这样的众筹网站，哪些会变？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说不变：** 「捐款这条流程原样搬过来：donationId、三层防重复、UNKNOWN 与对账、发件箱回执都不变。变的是活动的生命周期和钱的去向。」
- **变一，活动长期、由用户创建：** 「多一个活动（Campaign）实体：campaignId、组织者、目标金额、状态、截止日期；Donation 多一个 campaignId。要登录，组织者要通过身份核验（KYC）。活动可以开几个月，不再是 3 天后整站拆除。」
- **变二，钱要付给组织者：** 「3 天站的钱归我们一个账户；GoFundMe 是平台，要把钱付给每个组织者。我用 PSP 的市场方案（connected accounts，子账户）：组织者绑定收款账户并通过 KYC；捐款先收进平台账户，持有一段时间；满足条件，比如活动结束或到达里程碑、风控期过、没有拒付，再由付款任务（payout job）转到组织者的子账户，最后到银行。账本（ledger）记每一步，平台手续费也在这里扣。」
- **变三，活动页读流量暴增：** 「病毒传播的活动页读远多于写。用 CDN 缓存活动页，累计金额用几秒的短 TTL。假设一个热门活动 1 万读/秒、命中率 99%，源站只剩 10,000 × 1% = 100 次/秒。」
- **变四，必须实时展示总额：** 「捐款成功事件经发件箱和队列，由计数器消费者更新。数据库行 +1 在热门活动上是热点行，要用分片计数器：N 个子行，写时随机选一个，读时求和；用 Redis 的话，INCRBY 单键能扛很高的写入，事件喂入就够，真不够再分片。Redis 只管展示，真相是 donations 表求和，定时校正。」
- **变五，退款：** 「捐款人要退款、被拒付、活动被判欺诈，都要退款。退款也是一笔有状态的资金操作：Refund 实体加状态机加幂等键加对账，同样会超时变成 UNKNOWN；钱已经转给组织者的，还要从账本追回。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 476">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读路径：活动页 + 实时累计</text>
<rect x="12" y="26" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">访客浏览器</text>
<text x="82" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">海量读</text>
<rect x="188" y="26" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组织者</text>
<text x="258" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">登录 · 建活动</text>
<rect x="12" y="94" width="316" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CDN · 缓存活动页 + 累计金额（TTL 几秒）</text>
<polyline points="82,66 82,94" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,94 78.8,87.0 85.2,87.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="88" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET /campaigns/:id</text>
<rect x="12" y="168" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">活动服务</text>
<text x="82" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Campaign</text>
<polyline points="82,130 82,168" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,168 78.8,161.0 85.2,161.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="88" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">未命中</text>
<polyline points="328,46 334,46 334,188 152,188" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="152,188 159.0,184.8 159.0,191.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="160" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">建 / 改活动</text>
<path d="M12,242 a70,6 0 0 1 140,0 v64 a70,6 0 0 1 -140,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M12,242 a70,6 0 0 0 140,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="82" y="260" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="20" y="276" width="124" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="291" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">campaigns 表</text>
<polyline points="60,208 60,236" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,236 56.8,229.0 63.2,229.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="60,208 63.2,215.0 56.8,215.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M188,242 a70,6 0 0 1 140,0 v64 a70,6 0 0 1 -140,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M188,242 a70,6 0 0 0 140,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="260" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="196" y="276" width="124" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="291" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">total:{id}</text>
<polyline points="152,208 188,250" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="188,250 181.0,246.8 185.9,242.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="12" y="340" width="140" height="36" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="20" y="363" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="44.8" y="363" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="69.6" y="363" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="94.4" y="363" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="119.2" y="363" width="21.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<text x="82" y="355" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 · 捐款成功事件</text>
<polyline points="82,312 82,340" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="82,340 78.8,333.0 85.2,333.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="88" y="332" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">outbox</text>
<rect x="188" y="340" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="356.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数器消费者</text>
<text x="258" y="371.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">INCRBY 金额</text>
<polyline points="152,358 188,358" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="188,358 181.0,361.2 181.0,354.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="258,340 258,312" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258,312 261.2,319.0 254.8,319.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="264" y="330" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">累加</text>
<text x="8" y="404" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">假设热门活动 1 万读/秒，命中 99%：</text>
<text x="8" y="422" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">源站 1 万 × 1% = 100/秒</text>
<text x="8" y="440" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis 只管展示，真相 = donations 表求和，</text>
<text x="8" y="458" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定时校正；DB 行计数才需要分片</text>
</svg>
白板上新增（读路径）：CDN、活动服务、campaigns 表、Redis 累计金额和计数器消费者。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 430">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱的路径：持有、放款、退款</text>
<rect x="12" y="26" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款人浏览器</text>
<text x="82" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">流程同 3 天站</text>
<rect x="12" y="94" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款 API</text>
<text x="82" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三层防重复照旧</text>
<polyline points="82,66 82,94" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="82,94 78.8,87.0 85.2,87.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="188" y="94" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP · 平台账户</text>
<text x="258" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先收进来，持有</text>
<polyline points="152,114 188,114" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,114 181.0,117.2 181.0,110.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="12" y="168" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">账本 Ledger</text>
<text x="82" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">捐款 · 手续费 · 放款</text>
<polyline points="82,134 82,168" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,168 78.8,161.0 85.2,161.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="88" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一事务</text>
<rect x="188" y="168" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">付款任务 Payout</text>
<text x="258" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持有期满 + 条件满足</text>
<rect x="188" y="240" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="258.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组织者子账户</text>
<text x="258" y="273.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Connected · 已 KYC</text>
<polyline points="258,212 258,240" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258,240 254.8,233.0 261.2,233.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="264" y="231" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">转账</text>
<rect x="188" y="312" width="140" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="334" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">组织者银行账户</text>
<polyline points="258,284 258,312" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258,312 254.8,305.0 261.2,305.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="264" y="303" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放款</text>
<rect x="12" y="240" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="258.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退款 Refund</text>
<text x="82" y="273.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态机 + 幂等键</text>
<polyline points="82,240 82,212" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,212 85.2,219.0 78.8,219.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="88" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">冲回</text>
<polyline points="152,262 170,262 170,124 188,124" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="188,124 181.0,127.2 181.0,120.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="376" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">放款条件：活动结束或里程碑、风控期过、</text>
<text x="8" y="394" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">组织者通过身份核验、无拒付；</text>
<text x="8" y="412" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">退款同样会超时 → UNKNOWN → 对账</text>
</svg>
白板上新增（钱的路径）：账本、付款任务、组织者子账户和银行、退款。
**为什么这样说。** （约 3 分钟；面试官追问或时间有余时再讲。）面试官看你是不是只会背一套答案，还是能区分「什么不变」和「什么要变」。强的回答先说核心流程原样复用，再只讲变化：长期活动、钱的去向、读流量、实时总额、退款。弱的回答是把整个设计推倒重画。
**面试官可能接着问。**
- 持有期为什么需要？ → 为了留出风控和拒付的窗口：钱一旦转给组织者，再追回很难。持有多久取决于风险和合规，我会按活动类型分级。
- 总额一定要精确吗？ → 展示数字允许几秒延迟；对账和放款用的是 donations 表和账本，不依赖 Redis。
- CDN 缓存的金额会不会旧？ → 会旧几秒，可以接受；用户自己刚捐完时，前端用本次金额本地加上去，避免他觉得没生效。
- 组织者没通过 KYC 怎么办？ → 活动可以发布、可以收款，但付款任务不放款，直到核验通过；超期就退款给捐款人。
**常见失分。**
- **推倒重来：** 捐款流程明明可以原样复用，却从头设计。
- **忽略钱的去向：** 只讲捐款进来，没讲怎么付给组织者，等于只做了一半。
- **Redis 当账本：** 计数器只是展示，账目真相必须在数据库和账本里。
- **漏掉退款：** 众筹一定会遇到退款和拒付，不提会被追问。
