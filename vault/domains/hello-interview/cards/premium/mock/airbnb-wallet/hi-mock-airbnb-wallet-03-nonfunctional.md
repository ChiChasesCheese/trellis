---
id: hi-mock-airbnb-wallet-03-nonfunctional
node: fix.airbnb-wallet-mock
type: qa
step: 3
---
## Q
**Airbnb Wallet · 第 3 步 · 非功能需求**｜模拟面试

面试官：「再说说非功能需求。你最看重什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **正确性第一：** 「可用余额永远不为负；同一笔钱不能被两笔提现同时花掉；平台的每一次结果，在钱包里只生效一次。」
- **不丢：** 「事务提交之后的钱包和交易不能丢。主库带一台同步备库，故障时切换。」
- **平台不拖慢读：** 「读余额、读状态只读本地表。平台慢或者挂了，读不受影响。读余额的 p99 小于 200 毫秒；提现的受理 p99 小于 3 秒，因为请求里含一次约 1 秒的平台调用，我给它设 2 秒超时，超时也返回 pending；完成是异步的。」
- **对平台的调用有上限：** 「平台额度是 100 次/秒。用户能触发的调用必须有新鲜度窗口和全局限速，我不让用户的刷新直接变成平台的流量。」
- **丢回调有上限：** 「回调是常态路径，但它会丢。我要一条扫描路径，让没收到回调的转账约一天内收敛：每天扫一次，只扫超过 1 小时的，所以最坏等 24 + 1 = 25 小时，超过 26 小时就告警。这个一天是我的假设，您有更紧的要求我就改。」
- **不追求的：** 「不做多区域多活，不追求毫秒级完成；完成是异步的。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非功能需求 → 逼出的设计</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">钱不多花：可用余额永不为负</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 一条条件 UPDATE，行锁排队</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每笔平台结果只生效一次</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 幂等键 · 先写 pending · 条件改状态</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">平台慢不拖慢读：读只读本地表</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 新鲜度窗口 30 秒，后台刷新</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">丢回调有上限：25 小时内收敛</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 每天一次扫描 + 告警 pending 年龄</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟：读余额 p99 &lt; 200 毫秒；</text>
<text x="8" y="268" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提现受理 &lt; 3 秒（含平台调用），完成异步</text>
</svg>
白板上新增：四张便签，每张两行：需求、它逼出的设计。深入问题从这四张里选。
**为什么这样说。** （约 3 分钟，累计第 8 分钟。）面试官看你能不能把非功能需求写成可检验的句子：一条不变量，或一个数字加单位。强的回答每一条后面都跟着「所以我会……」，让需求变成设计决定；弱的回答是「要高可用、高并发、低延迟」，没有数字，也不知道哪一条最硬。
**面试官可能接着问。**
- 为什么余额不能是最终一致？ → 余额决定能不能再花。允许暂时算多，两个并发的提现就会都成功，钱已经转出去，追不回来。所以余额这一条必须强一致，别的读可以松。
- 25 小时是怎么来的？ → 假设业务可以接受一天：每天扫一次，间隔 24 小时；扫描只看超过 1 小时的（正常在途的不查），所以最坏等 24 + 1 = 25 小时。您给更紧的要求，我就把扫描改成每小时，最坏变成 2 小时，代价是对卡住的转账调用最多 ×24。
- 读余额 p99 小于 200 毫秒怎么定的？ → 单行主键读在数据库里是几毫秒，200 毫秒是给网络和应用留的预算，不是预测。关键是读不依赖平台。
- 为什么不做多区域多活？ → 题目没要求，而且它会把单行条件更新变成跨区域冲突。我先在一个区域做到正确，再谈扩展。
**常见失分。**
- **只说空话：** 「要高可用、高并发」没有数字，面试官无法判断你要的是什么系统。
- **漏掉对外调用的上限：** 不把平台额度写进需求，后面的刷新和扫描就没有预算可依。
- **把完成当同步：** 提现要几分钟才完成，却写成请求内等结果，用户和连接都会被拖住。
- **需求不变成设计：** 说了「不能透支」，却没有说它逼出一条条件更新。
