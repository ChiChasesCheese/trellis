---
id: hi-mock-uber-04-entities
node: sd.problem-breakdowns.uber.mock
type: qa
step: 4
---
## Q
**网约车 · 第 4 步 · 核心实体**｜模拟面试

面试官：「好，接下来说数据：你打算存哪些核心实体？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先报清单：** 「五个：乘客（Rider）、司机（Driver）、估价（Fare）、行程（Ride）、位置（Location）。」
- **Fare：** 「起点、终点、估价、预计到达时间。我把它单独拿出来，因为乘客是对着某个估价叫车的；并进行程里也行，没有对错。」
- **Ride：** 「从乘客确认估价到行程结束的一条记录：乘客、司机、状态、实际费用、上下车时间。状态先是 requested，接单后 accepted。」
- **Location：** 「司机的实时经纬度和最后更新时间，匹配和行程跟踪都靠它。」
- **字段先不展开：** 「具体字段我用到时再补，现在先把实体和关系定下来。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 392">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">核心实体（箭头 = 用 id 指向）</text>
<rect x="8" y="28" width="140" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">乘客 Rider</text>
<text x="78" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">姓名 · 联系方式</text>
<text x="78" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">支付方式</text>
<rect x="192" y="28" width="140" height="90" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">估价 Fare</text>
<text x="262" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">起点 · 终点</text>
<text x="262" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">估价 · ETA</text>
<text x="262" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">riderId</text>
<rect x="8" y="168" width="140" height="90" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">司机 Driver</text>
<text x="78" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">姓名 · 车辆信息</text>
<text x="78" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可接单状态</text>
<text x="78" y="239.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">偏好</text>
<rect x="192" y="168" width="140" height="106" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">行程 Ride</text>
<text x="262" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fareId · riderId</text>
<text x="262" y="225" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">driverId · 状态</text>
<text x="262" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实际费用</text>
<text x="262" y="255" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上下车时间</text>
<rect x="8" y="304" width="140" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="330" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">位置 Location</text>
<text x="78" y="345" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">driverId</text>
<text x="78" y="360" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">经纬度 · 更新时间</text>
<polyline points="148,65 192,65" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="192,65 185.0,68.2 185.0,61.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="262,118 262,168" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,168 258.8,161.0 265.2,161.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="268" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fareId</text>
<polyline points="192,221 148,221" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="148,221 155.0,217.8 155.0,224.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="78,258 78,304" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="78,304 74.8,297.0 81.2,297.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="84" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">driverId</text>
<text x="192" y="312" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Fare 单独成一个实体，</text>
<text x="192" y="328" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">因为乘客是对着某个</text>
<text x="192" y="344" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">估价叫车的；也可以</text>
<text x="192" y="360" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并进 Ride，没有对错</text>
</svg>
白板上新增：五个实体框，箭头表示用 id 指向：乘客 → 估价 → 行程 → 司机 → 位置。
**为什么这样说。** （约 2 分钟，累计第 7 分钟。）面试官看你能不能快速列出支撑功能需求的实体，并说清它们怎么连。每个功能至少对应一个实体：估价对应 Fare，叫车对应 Ride，匹配对应 Location 和 Driver。弱的回答是画满字段的 ER 图，花了五分钟，或者漏掉 Location。
**面试官可能接着问。**
- Fare 为什么单独存？ → 乘客确认的是一个具体估价，叫车时我按 fareId 回库读价格，不信客户端传来的数字。单独存还方便给估价设过期时间。并进 Ride 也行，取舍是少一张表还是语义更清楚。
- 行程有哪些状态？ → requested、accepted、进行中、完成，再加 cancelled。状态只往前走，每次变更用条件更新，防止并发写乱。
- Location 放主库吗？ → 先画在库里，保持简单；等讲到每秒 200 万次写入，我会把它挪出去。
**常见失分。**
- **字段写满：** 实体阶段列十几个字段，既耗时间又容易写错，字段留到用时再补。
- **漏掉位置：** 匹配靠位置，缺了 Location，后面的近邻搜索没有数据来源。
- **实体之间不说关系：** 只列名词，不说谁指向谁，面试官看不出你理解数据怎么流动。
