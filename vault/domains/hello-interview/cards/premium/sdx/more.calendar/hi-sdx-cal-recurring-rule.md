---
id: hi-sdx-cal-recurring-rule
node: more.calendar
type: qa
step: 1
---
## Q
**重复事件：存一条规则，查询时展开**｜补充 · 日历与排期（Google Calendar） · 必会

「每周一、周三上午 10 点站会，一直开到年底」。日历里应该存 100 多行事件，还是只存一条？之后有人把其中一次改到周四，又取消了另一次，怎么存？如果有人说「以后都改到 11 点」呢？

## A
**结论。** 只存一条主事件加一条重复规则，需要显示某个时间窗口时，才按规则现场展开成一个个实例。改动或取消其中某一次，另存一条例外记录，用「原定开始时间」指出是哪一次。

**要点。**
- **为什么不存成多行：** 没有结束日期的重复根本存不完；「以后都改到 11 点」要改成百上千行，还容易改漏。
- **规则的标准写法：** iCalendar 的 RRULE，用 FREQ（频率）、INTERVAL（间隔）、BYDAY（星期几）描述，再用 UNTIL（截止日期）或 COUNT（次数）二选一结束，例如 `FREQ=WEEKLY;BYDAY=MO,WE;UNTIL=20261231T000000Z`。
- **展开只做窗口内的：** 用户看哪几周，就只算哪几周的实例，不预先生成。
- **例外覆盖规则：** 改某一次，存一条例外（标准里用 RECURRENCE-ID 标识那一次）；取消某一次，登记排除日期 EXDATE。展开时先按规则算，再用例外覆盖或剔除。
- **「此次及以后」：** 常见做法是把原系列的 UNTIL 截到这一次之前，另建一个新系列从这一次开始。
- **时区要跟着事件：** 规则按事件自己的时区计算，夏令时切换后「每周一 10 点」仍是当地 10 点；存成一串固定的 UTC 时刻就会错一小时。

**为什么。** 把「会重复」当作数据（规则）存下来，而不是存展开后的结果，存储和「改整个系列」的成本都是常数。代价是读的时候要展开，所有需要日程的功能（忙闲查询、提醒）都要走同一个展开逻辑。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="50" y="8" width="240" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">规则 FREQ=WEEKLY;BYDAY=MO,WE</text>
<polyline points="170,38 30,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="5" y="88" width="50" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="30.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">周一</text>
<polyline points="170,38 86,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="61" y="88" width="50" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">周三</text>
<polyline points="170,38 142,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="117" y="88" width="50" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="142.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改周四</text>
<polyline points="170,38 198,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="173" y="88" width="50" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<text x="198" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已取消</text>
<polyline points="177,92 219,114" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polyline points="170,38 254,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="229" y="88" width="50" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">周一</text>
<polyline points="170,38 310,88" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="285" y="88" width="50" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="310.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">周三</text>
<text x="142" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①</text>
<text x="198" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">②</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 改某一次：另存一条例外，指向原定时间</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 取消某一次：登记排除日期（EXDATE）</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">展开：只算用户正在看的那段时间</text>
</svg>

**面试里这样说。** 「重复事件我存一条主事件加 RRULE，读的时候只展开用户正在看的窗口。改某一次存一条例外，取消某一次记 EXDATE，改『此次及以后』就截断旧系列、新建一个。规则按事件时区算，避免夏令时错一小时。」

**易错。**
- **预先展开成 N 行：** 无限重复存不下，改整个系列要改一大批行。
- **例外不记原定时间：** 找不到它对应规则里的哪一次，改过的那次会重复出现。
- **把时间存成固定的 UTC 点：** 夏令时切换后整串事件偏移一小时。
