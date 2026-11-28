---
id: hi-fix-component-cost-01-mechanism
node: fix.component-cost
type: qa
step: 1
---
## Q
**加组件 · 职责与新问题**｜补强

面试官：「你为什么要加这个组件？它会带来什么新问题？」

你会怎么回答？白板上画到哪一步？

## A
**要防的故障。**
- **名字不是机制：** 说「加个队列、加个 Redis」，面试官听到的只是工具名。队列会重发，自增会执行两次，名字本身不保证总额正确。
- **新问题没人负责：** 每个组件把原来的问题搬到一个新地方，新地方有自己的出错方式；不说出来，就没有人去处理它。
- **典型后果：** 下图，队列重发了一条完成事件，Redis 把同一笔捐款加了两次，总额多出 25。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 272">
<rect x="16" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="126" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作进程</text>
<rect x="236" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="64" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="60,84 170,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INCRBY total 25</text>
<polyline points="170,118 280,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,118 273.0,121.2 273.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">确认丢了 · 队列重发</text>
<text x="64" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="60,180 170,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,180 163.0,183.2 163.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INCRBY total 25</text>
<polyline points="170,214 280,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,214 273.0,217.2 273.0,210.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d42 被加了两次：total 多出 25</text>
<text x="8" y="260" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只说「加个队列」，没说重发怎么办</text>
<line x1="60" y1="48" x2="60" y2="229" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="244" x2="60" y2="249" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="264" x2="60" y2="268" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="135" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="150" x2="170" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="172" x2="170" y2="229" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="244" x2="170" y2="249" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="264" x2="170" y2="268" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="48" x2="280" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="110" x2="280" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="206" x2="280" y2="268" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="142" x2="101.72" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="238.28" y1="142" x2="332" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
**机制。**
- **职责和新问题成对说：** 职责回答「为什么需要它」，新问题回答「它出错时数据会怎样」。
- **处理是一个具体的记录或规则：** 比如 applied 表的唯一键、数据库的条件更新；不是「加监控」「重试一下」。
- **修好之后：** 下图，同一条事件重发，在 applied 的唯一键上被挡住，总额只加一次。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 314">
<rect x="16" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="126" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作进程</text>
<rect x="236" y="8" width="88" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="64" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="60,84 170,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="276" y="106" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(d42); total += 25</text>
<polyline points="170,118 280,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,118 273.0,121.2 273.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="240.6" y="132" width="78.8" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一个事务</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">确认丢了 · 队列重发</text>
<text x="64" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="60,208 170,208" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,208 163.0,211.2 163.0,204.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(d42)</text>
<polyline points="170,242 280,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,242 273.0,245.2 273.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">唯一冲突：已加过</text>
<polyline points="280,276 170,276" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,276 177.0,272.8 177.0,279.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="302" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跳过，total 只多 25 一次</text>
<line x1="60" y1="48" x2="60" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="110" x2="60" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="306" x2="60" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="110" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="185" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="200" x2="170" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="306" x2="170" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="48" x2="280" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="154" x2="280" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="234" x2="280" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="268" x2="280" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="170" x2="101.72" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="238.28" y1="170" x2="332" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
**一句话。**
- **模板：** 「我加 X 是为了 Y，新问题是 Z，我这样处理。」每加一个组件说一遍，每格一句，十来秒。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每加一个组件，说完这四格再往下</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 加什么</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我加 X」</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个具体的组件，不是一类</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 它的职责</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「为了 Y」</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个数字或一个需求撑着它</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 新问题</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「新问题是 Z」</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重发、过期、不一致、写放大……</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">④ 怎么处理</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">「我这样处理」</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个具体的记录或规则</text>
</svg>
**怎么认出需要它。**
- **你正要说「加个缓存、队列、事务、分片」：** 先停一下，把四格说完再往下画。
- **面试官问「崩了呢、重放呢、过期呢」：** 他在等第三格。
- **同一个事实写在两个地方：** 数据库和 Redis，数据库和队列。两处之间一定有不一致的窗口，要说谁是真相。
- **组件自带生命周期：** 锁会过期，位置会过期，缓存会被淘汰，说清过期之后发生什么。
**面试官可能接着问。**
- 能不能不加这个组件？ → 先说不加的版本，再说为什么不够：要有一个数字撑着，比如每秒几千次读、几万次写。
- 新问题我想不出来怎么办？ → 问自己四件事：它会重发吗，会过期吗，会和别处不一致吗，会放大写吗。答案是「是」的那一个，就是 Z。
**常见失分。**
- **只报工具名：** 没有职责，也没有新问题。
- **新问题说得太泛：** 「可能不一致」没说谁和谁、怎么收敛。
- **处理是「加监控」：** 监控只能发现，不能保证对。
- **每个组件讲太久：** 四格各一句；时间紧就挑最容易出错的那个讲透。
