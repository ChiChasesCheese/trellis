---
id: hi-fix-apply-once-05-ad-click
node: fix.apply-once
type: qa
step: 5
---
## Q
**广告点击聚合 · 只应用一次**｜补强

面试官：「Flink 作业重启后会从上一个检查点重放 Kafka。聚合表里的点击数会不会被多算？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先分两层说：** 「去重和聚合是两件事。去重已经在进流之前用 impression_id 做完了：同一次展示最多一条点击进 Kafka。这里问的是聚合结果写进库时的重放。」
- **聚合表的主键就是已应用记录：** 「`ad_clicks_minute(ad_id, minute, clicks)`，主键 `(ad_id, minute)`。」
- **写绝对值，不写增量：** 「Flink 每个窗口发出的是这个窗口的累计点击数，我用 `INSERT … ON CONFLICT (ad_id, minute) DO UPDATE SET clicks = EXCLUDED.clicks` 写进去。重放同一个窗口，算出来是同一个数，写一百次结果一样。」
- **什么写法是错的：** 「`clicks = clicks + EXCLUDED.clicks`。重放一次，多算一次。」
- **前提：** 「流处理发出的必须是窗口的累计值，不能是自上次发出以来的增量。如果有提前触发（每 10 秒发一次），每次发的仍然是到现在为止的累计。」
- **迟到的点击：** 「窗口又收到迟到的点击，重新发出更大的累计，同一个主键覆盖旧值。为防止旧结果在重放里晚到、盖掉新结果，写 `SET clicks = GREATEST(ad_clicks_minute.clicks, EXCLUDED.clicks)`。」
- **如果非得写增量：** 「那就要有已应用记录：每次写增量带一个 (窗口, 分区, 偏移范围) 的 id，先插已应用表再加。所以我选绝对值：不需要额外的表。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 316">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Flink</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">聚合表</text>
<text x="282" y="72" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">UPSERT (ad5, 10:01) = 120</text>
<polyline points="170,84 286,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="286,84 279.0,87.2 279.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="237.24" y="98" width="97.52" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">clicks = 120</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">作业重启，从检查点重放</text>
<text x="58" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重放 10:01 的点击</text>
<polyline points="54,174 170,174" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,174 163.0,177.2 163.0,170.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="282" y="196" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPSERT (ad5, 10:01) = 120</text>
<polyline points="170,208 286,208" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,208 279.0,211.2 279.0,204.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="252.12" y="222" width="67.76" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="236" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍是 120</text>
<text x="174" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">迟到点击后重发 = 123</text>
<polyline points="170,270 286,270" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,270 279.0,273.2 279.0,266.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="237.24" y="284" width="97.52" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="298" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">clicks = 123</text>
<line x1="54" y1="48" x2="54" y2="312" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="144" x2="170" y2="151" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="166" x2="170" y2="185" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="200" x2="170" y2="312" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="96" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="120" x2="286" y2="220" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="244" x2="286" y2="247" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="262" x2="286" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="306" x2="286" y2="312" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="136" x2="92.72" y2="136" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="247.28" y1="136" x2="332" y2="136" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：重启后重放，同一个窗口再写一次，值没变；迟到点击之后值变大。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">怎么写进聚合表</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">增量写 clicks = clicks + n</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重放一次，多算一次</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">绝对写 clicks = 窗口累计值</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重放写同一个值，结果不变</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">前提</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">流处理发出的是窗口累计，不是增量</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">乱序保险</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DO UPDATE SET clicks = GREATEST(旧, 新)</text>
</svg>
白板上：绝对写和增量写的差别，以及绝对写的前提。

**为什么这样说。** 面试官要听到：你没有把正确性押在「sink 只写一次」上，而是让写多少次结果都一样。弱的回答是「Flink 有 exactly-once」：这只管流处理内部的状态，不管外部库里被写了几次。强的回答把写入改成对窗口主键的绝对值覆盖。
**面试官可能接着问。**
- Flink 的 exactly-once 不够吗？ → 它保证内部状态；写外部库要靠幂等写入或两阶段提交，我选前者，更简单。
- 窗口怎么定义？ → 按事件时间的一分钟滚动窗口，主键里的 minute 就是窗口起点。
- 要查一小时的点击数怎么办？ → 对 60 个分钟行求和，一个读的聚合，不是写。
- 重复点击的去重和这个有什么区别？ → 去重挡的是用户重复点击，这里挡的是我们自己的重放，两层各管一件事。
**常见失分。**
- **`clicks = clicks + n`：** 重放一次多算一次。
- **发出的是增量不是累计：** 绝对写就失效了，反而会覆盖掉之前的值。
- **把 Flink 的 exactly-once 当整条链路的保证：** 外部库的写入仍可能重复。
- **没有处理乱序到达：** 旧结果盖掉新结果。
