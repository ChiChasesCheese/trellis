---
id: hi-sdx-cal-freebusy-boundary
node: more.calendar
type: qa
step: 4
---
## Q
**忙闲查询：只给时段，不给内容**｜补充 · 日历与排期（Google Calendar） · 追问

面试官：「排会议时要同时看 5 个人什么时候有空，但不能让你看到他们日程的标题。接口怎么设计？底层用什么索引，不要逐人扫描事件表？」

## A
**结论。** 忙闲是独立于「读事件」的接口，只返回忙碌的时间区间，不含标题、地点。底层是每个用户一份按时间排序的忙碌区间索引，查询时取窗口内的区间、合并，再求大家都空的时段。权限边界在接口层，而不是性能优化。

**要点。**
- **两个接口两种权限：** 读事件需要日程的查看权限；忙闲查询只暴露忙或闲，没有日程权限也能查。这是 CalDAV 里 calendar-query 与 free-busy-query 两个 REPORT 方法的区别。
- **忙碌区间索引：** 键是 (user_id, 开始时间)，值是结束时间，不含事件详情；事件变化时更新，重复事件展开成近期窗口内的区间。
- **查询怎么算：** 对每个人取窗口内的区间，合并重叠，取并集，再取补集得到共同空闲时段。
- **哪些算忙：** 标成「空闲」（透明）的事件不占用时间；私密事件照样算忙，但不暴露内容。
- **分片：** 索引按用户分片，一次查询只访问被查的几位用户所在的分片。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">9 点到 17 点，每人只有忙碌区间</text>
<text x="8" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<line x1="44" y1="38" x2="332" y2="38" stroke="currentColor" opacity="0.25"/>
<rect x="44" y="28" width="72" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="188" y="28" width="36" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="8" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<line x1="44" y1="68" x2="332" y2="68" stroke="currentColor" opacity="0.25"/>
<rect x="80" y="58" width="72" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="260" y="58" width="36" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<line x1="44" y1="98" x2="332" y2="98" stroke="currentColor" opacity="0.25"/>
<rect x="44" y="88" width="36" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="224" y="88" width="36" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">合</text>
<line x1="44" y1="128" x2="332" y2="128" stroke="currentColor" opacity="0.25"/>
<rect x="44" y="118" width="108" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="188" y="118" width="108" height="20" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="152" y="118" width="36" height="20" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="296" y="118" width="36" height="20" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合并重叠的忙碌区间，剩下的缝就是共同空闲：</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12-13 点、16-17 点；响应里没有任何标题。</text>
</svg>

**为什么。** 把权限做在返回的字段上：忙闲接口天然拿不到标题。如果为了快直接扫事件表再抹掉标题，一次疏忽就泄露内容，而且人数一多就慢。

**面试里这样说。** 「忙闲单独成接口，返回的只有忙碌区间。底层每个用户一份 (user_id, start) 的区间索引，查五个人就是取五段区间、合并后取补集。事件里标成空闲的不算忙，私密事件算忙但不带标题。」

**易错。**
- **响应里带事件标题：** 优化做对了，隐私边界却破了。
- **逐个扫事件表：** 重复事件还要现场展开，参会人多了就慢。
- **把透明事件当忙：** 用户明明标了「空闲」，别人却看到他忙。
