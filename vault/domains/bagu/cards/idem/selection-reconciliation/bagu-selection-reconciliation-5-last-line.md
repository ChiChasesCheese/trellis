---
id: bagu-selection-reconciliation-5-last-line
node: a.idem.selection-reconciliation
type: qa
step: 5
---
## Q
**对账 · 为什么说对账是最后一道防线**｜追问

面试官：「你前面讲了幂等、重试、补偿，都做了，为什么还说必须有对账？它能发现什么是前面发现不了的？」

## A
**基本回答。** 幂等、重试、补偿都依赖代码正确和消息不丢，它们出错是无声的：代码 bug、人工改库、对方更正账单、消息被误确认，都会让数据悄悄不一致。对账拿独立来源的记录比对，不依赖前面的路径，所以能发现所有其他环节漏掉的问题。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">幂等 / 重试 / 补偿：都靠代码正确、消息不丢</text>
<rect x="8" y="26" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务代码</text>
<line x1="98" y1="41" x2="118" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="125.0,41.0 118.0,44.2 118.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="125" y="26" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息</text>
<line x1="215" y1="41" x2="235" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="242.0,41.0 235.0,44.2 235.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="242" y="26" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">补偿重试</text>
<text x="8" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">代码 bug、人工改库、误确认 → 悄悄不一致</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对账：独立来源，不走前面的路径</text>
<rect x="8" y="118" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内部账本</text>
<line x1="58" y1="146" x2="58" y2="157" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,164.0 54.8,157.0 61.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="118" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道文件</text>
<line x1="170" y1="146" x2="170" y2="157" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,164.0 166.8,157.0 173.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="118" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">银行流水</text>
<line x1="282" y1="146" x2="282" y2="157" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,164.0 278.8,157.0 285.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="164" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="183" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">逐笔比对（对账）</text>
<line x1="170" y1="194" x2="170" y2="205" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,212.0 166.8,205.0 173.2,205.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="212" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="231" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">差异为零 → 才放款</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">没对平不放款</text>
</svg>
第一行是幂等、重试、补偿这几道防线：它们都走同一条代码路径，路径里出错，数据就悄悄错了。第二部分是对账：从三个独立来源各自取数，逐笔比对，差异为零才放款。
**举个例子。** 一次上线 bug 让部分退款在渠道成功了，但没有记入内部账本：
1. **前面的防线：** 消息都正常投递、没有积压，接口返回都是成功，幂等和重试都没触发，所有监控是绿的。
2. **日终对账：** 把内部账本和渠道文件按交易号逐笔比，发现「渠道退款多于账本」。
3. **按案例聚合：** 这批差异的原因码一致（同一个 bug），聚合后批量补记，用追加调整分录的方式，原记录不动。
4. **放款：** 差异处理完、对平之后，对账完成状态才放行打款，没有扩大为资金差错。
**容易错。**
- **以为做了幂等、重试、补偿就够了：** 它们依赖代码正确，出错是无声的。
- **以为消息不积压数据就一致：** 传递正常不等于数据一致。
- **把对账当报表：** 它应当是放款的门槛，不是事后看看。
- **发现差异直接改原记录：** 要追加带原因码的调整分录，才能追溯。
