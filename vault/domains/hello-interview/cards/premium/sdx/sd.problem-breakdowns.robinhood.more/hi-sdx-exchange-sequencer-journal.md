---
id: hi-sdx-exchange-sequencer-journal
node: sd.problem-breakdowns.robinhood.more
type: qa
step: 1
---
## Q
**定序器挂了：停，不绕过**｜补充 · 股票交易（Robinhood） · 追问

面试官：「交易所撮合引擎前面有一层定序器（sequencer），给每个订单事件发序号、写进复制日志。现在某支股票的定序器挂了，你会让这支股票的订单先绕过定序、直接进撮合引擎，保住可用性吗？」

## A
**结论。** 不会。停掉这支股票的新单，等定序器恢复；只停这一个分片，其他股票照常交易。

**要点。**
- **绕过会丢掉顺序：** 绕过定序的订单没有序号、没进日志，撮合引擎按它碰巧收到的顺序处理。
- **再崩一次就无法恢复：** 撮合引擎这时再崩，备机重放日志重建的订单簿缺了这些订单，主备悄悄分叉，而且事后查不出来。
- **可用性让位正确性：** 对交易所，成交顺序错了比停几分钟严重得多：成交是对外的、不可撤回的承诺。
- **影响面按股票控制：** 定序器按股票（symbol）分片，一个分片挂了只停这一组股票，所以「停」的代价可控。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 370">
<rect x="20" y="8" width="150" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="95.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单网关</text>
<polyline points="95,44 95,78" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95,78 91.8,71 98.2,71" style="fill:var(--accent,#3b6fd4)"/>
<text x="103" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新单 / 撤单</text>
<rect x="20" y="78" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="95.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 定序器</text>
<text x="95.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Sequencer · 发序号</text>
<polyline points="170,100 214,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214,100 207,96.8 207,103.2" style="fill:var(--accent,#3b6fd4)"/>
<rect x="214" y="78" width="108" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="268.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">复制日志</text>
<text x="268.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先落盘 ×3</text>
<polyline points="95,122 95,158" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95,158 91.8,151 98.2,151" style="fill:var(--accent,#3b6fd4)"/>
<text x="103" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 按序号送入</text>
<rect x="20" y="158" width="150" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="95.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 撮合引擎</text>
<text x="95.0" y="192.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单线程 · 内存订单簿</text>
<polyline points="95,202 95,236" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95,236 91.8,229 98.2,229" style="fill:var(--accent,#3b6fd4)"/>
<rect x="20" y="236" width="150" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="95.0" y="258.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成交回报</text>
<polyline points="268,122 268,158" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="268,158 264.8,151 271.2,151" style="fill:var(--accent,#3b6fd4)"/>
<rect x="214" y="158" width="108" height="44" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="268.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">备机引擎</text>
<text x="268.0" y="192.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重放日志接管</text>
<text x="8" y="302" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定序器挂了：停这支股票的新单，</text>
<text x="8" y="318" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不让订单绕过定序直接撮合。</text>
<text x="8" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">顺序不唯一，日志就不能重放，</text>
<text x="8" y="358" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">备机重建出来的订单簿就和主机不一样。</text>
</svg>

**面试里这样说。** 「每支股票的权威顺序只由定序器决定。它挂了我就停这支股票的新单，而不是绕过去，因为没有序号的事件无法重放，备机接管后会和主机分叉。定序器按股票分片，所以只停受影响的那一组。」

**易错。**
- **为可用性绕过定序：** 看起来没停机，其实丢掉了唯一能重放的顺序，之后每一次故障转移都不可信。
- **整个交易所一起停：** 没想到按股票分片，把局部故障变成全局停机。
- **把券商和交易所混为一谈：** 券商（Robinhood）那一侧可以降级（比如延迟下单、提示稍后再试）；不能降级的是交易所的撮合顺序。
