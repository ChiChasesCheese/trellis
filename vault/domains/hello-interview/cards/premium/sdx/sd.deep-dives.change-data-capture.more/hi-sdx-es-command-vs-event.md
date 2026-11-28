---
id: hi-sdx-es-command-vs-event
node: sd.deep-dives.change-data-capture.more
type: qa
step: 3
---
## Q
**命令何时变成事件**｜补充 · 变更数据捕获（CDC） · 加分

面试官：「事件溯源里，`ReserveSeat` 是命令，`SeatReserved` 是事件，为什么必须分开？它们在哪个精确的时刻转换？」

## A
**结论。** 命令是请求，可能被拒绝；事件是已被接受的不可变事实。转换点是追加时刻的同步校验：检查不变量（座位还空着吗，余额够吗），只有通过才原子地追加事件。用户能被告知「不行」，也只有在这一刻。

**要点。**
- **命令：** 表达意图，要对照当前状态校验，可以被拒绝。
- **事件：** 一旦追加，永不修改、永不删除；投影、下游服务、几年后的重放，都要能无条件把它当真。
- **校验与追加要串行：** 例如借助日志自身的顺序或条件追加，否则两个命令能同时通过校验。
- **为什么不能让消费者去校验：** 消费者说「不行」，撤销不了别人已经处理的事实，只能再发补偿事件，还要处理消费者之间的分歧。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">命令是请求，事件是事实</text>
<rect x="8" y="26" width="118" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="67.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">命令 ReserveSeat</text>
<polyline points="126,43 139.0,43.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="146,43 139.0,46.2 139.0,39.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="146" y="26" width="186" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="239.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">校验当前状态：座位空吗？</text>
<polyline points="239,60 239.0,77.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="239,84 235.8,77.0 242.2,77.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="247" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">通过</text>
<rect x="146" y="84" width="186" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="239.0" y="105.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">追加事件 SeatReserved</text>
<polyline points="239,118 239.0,135.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="239,142 235.8,135.0 242.2,135.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="146" y="142" width="186" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="239.0" y="163.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">投影 / 下游 / 重放</text>
<polyline points="60,60 60.0,141.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,148 56.8,141.0 63.2,141.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不通过</text>
<rect x="8" y="184" width="118" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="67.0" y="205.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝，告诉用户</text>
<line x1="8" y1="236" x2="332" y2="236" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">校验和追加必须一起串行，否则两个命令都能通过</text>
</svg>

**面试里这样说。** 「命令先在写入侧对当前状态校验，通过才追加成事件；事件一旦写入就是事实。我不会把原始命令写进日志，让每个读者各自校验。」

**易错。**
- **把命令写进日志：** 每个读者都要重复实现校验，结果还会不一致。
- **校验和追加分开执行：** 两个并发命令都看到座位是空的，都通过了。
